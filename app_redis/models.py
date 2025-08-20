from django.db import models

# Create your models here.
class Order(models.Model):
    item_name = models.CharField(max_length=255)
    qty = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return self.item_name