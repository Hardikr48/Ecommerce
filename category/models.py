from django.db import models


class Category(models.Model):
    name = models.CharField(default="",max_length=255, null=False)

    class Meta:
        db_table = "category"

    def __str__(self):
        return "{}".format(self.name)
