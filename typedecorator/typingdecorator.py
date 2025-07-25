from dataclasses import dataclass, field, MISSING
import typing
import sys
import docstring_parser
import re


class MyTestClass:
    first: int
    second: str = "hello"

    def say(self, other: str, silent: bool = False, loud: bool = True, *args, mommy: str, **kwargs) -> str:
        return self.second



def _eval_type(type_str, module_ns):
    try:
        return eval(type_str, vars(typing), module_ns)
    except Exception:
        try:
            return eval(type_str, module_ns)
        except Exception:
            pass
    return typing.Any

def _parse_docstring_any_style(docstring):
    try:
        return docstring_parser.parse(docstring)
    except Exception:
        pass

def typingdecorator(cls, silent=True):
    doc = cls.__doc__
    if not silent and not doc:
        raise ValueError(f"Class {cls.__name__} has no docstring.")

    parsed = _parse_docstring_any_style(doc)
    if not silent and not parsed:
        raise ValueError(f"Could not parse docstring for class {cls.__name__} with any supported style.")

    module_ns = sys.modules[cls.__module__].__dict__

    if not hasattr(cls, "__annotations__"):
        cls.__annotations__ = {}

    # Accept both 'params' (Google, Sphinx, Numpy) and 'meta' (rest, legacy)
    params = { param.arg_name: param for param in getattr(parsed, "params", []) } | { param.arg_name: param for param in getattr(parsed, "meta", [])}
    # Fallback: for some styles, attributes are in .meta with args like 'attribute'

    for name, param in params.items():
        type_str = getattr(param, "type_name", None) or "typing.Any"
        description = getattr(param, "description", None) or ""
        type_obj = _eval_type(type_str, module_ns)
        if param.is_optional and not getattr(type_obj, '__origin__', None) == typing.Union:
            type_obj = typing.Optional[type_obj]
        cls.__annotations__[name] = type_obj

        default = MISSING
        if getattr(param, "default", None) is not None:
            default = param.default
        else:
            m = re.search(r"[Dd]efault is (.*?)(?:\.|\n|$)", description)
            if m:
                default_str = m.group(1).strip()
                try:
                    default = eval(default_str, module_ns)
                except Exception:
                    default = default_str
            elif param.is_optional:
                default = None
        setattr(cls, name, field(default=default) if default is not MISSING else field())

    # Enhance methods: parse their docstrings and set __annotations__
    for attr_name, attr_value in cls.__dict__.items():
        if (
            callable(attr_value)
            and not attr_name.startswith("__")
            and not isinstance(attr_value, staticmethod)
            and not isinstance(attr_value, classmethod)
        ):
            fn = attr_value
            doc = getattr(fn, "__doc__", None)
            if doc:
                method_parsed = _parse_docstring_any_style(doc)
                if method_parsed:
                    fn_annotations = {}
                    # Params
                    for p in getattr(method_parsed, "params", []):
                        param_type = getattr(p, "type_name", None) or "typing.Any"
                        fn_annotations[p.arg_name] = _eval_type(param_type, module_ns)
                    # Return
                    if method_parsed.returns:
                        fn_annotations['return'] = _eval_type(getattr(method_parsed.returns, "type_name", None) or "typing.Any", module_ns)
                    if hasattr(fn, "__annotations__"):
                        fn_annotations = {**fn.__annotations__, **fn_annotations}
                    fn.__annotations__ = fn_annotations
            setattr(cls, attr_name, fn)

    # Make into a dataclass
    cls = dataclass(cls)
    # Validate/resolve all type hints using typing.get_type_hints for robustness
    cls.__annotations__ = typing.get_type_hints(cls, globalns=module_ns)
    return cls

# Example usage for all major styles:
@typingdecorator
class Example:
    """
    Example dataclass.

    Attributes
    ----------
    foo : int
        The foo attribute. Default is 123.
    bar : str, optional
        The bar attribute.
    """

    def greet(self, who):
        """
        Greets someone.

        Args:
            who (str): Name to greet.

        Returns:
            str: The greeting message.
        """
        return f"Hello, {who or self.bar or 'World'}!"

    def add(self, x, y):
        """
        Add two numbers.

        Parameters
        ----------
        x : int
            First number.
        y : int
            Second number.

        Returns
        -------
        int
            The sum.
        """
        return x + y

    def times(self, a, b):
        """
        Multiply two numbers.

        Parameters
        ----------
        a : int
            First.
        b : int
            Second.

        Returns
        -------
        int
            Product.
        """
        return a * b

    def info(self):
        """
        Display class info.

        Returns
        -------
        str
            Some info
        """
        return f"foo={self.foo}, bar={self.bar}"

# Test
example = Example(foo=5, bar="xyz")
print(Example)
print(example)
print(example.greet.__annotations__)
print(example.add.__annotations__)
print(example.info.__annotations__)
print(Example.__annotations__)
print(example.greet("Tester"))
