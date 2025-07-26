from django.db import models


# Create your models here.
class Category(models.Model):

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categorys"
        default_related_name = "categorys"

    name = models.CharField(max_length=100)


class Tag(models.Model):

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        default_related_name = "tags"

    name = models.CharField(max_length=100)


class PetQuerySet(models.QuerySet):
    pass


class Pet(models.Model):

    class Meta:
        verbose_name = "pet"
        verbose_name_plural = "pets"
        default_related_name = "pets"

    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        "Category", blank=True, null=True, on_delete=models.SET_NULL
    )
    photoUrls = models.URLField()
    tags = models.ManyToManyField("Tag", blank=True, null=True)
    status = models.CharField(
        max_length=100,
        choices=(("available", "available"), ("pending", "pending"), ("sold", "sold")),
        blank=True,
        null=True,
    )

    objects = PetQuerySet.as_manager()
