from django.db import models

# Create your models here.
class StockData(models.Model):
    security = models.CharField(max_length=20)
    lastprice= models.IntegerField()
    demandqty= models.IntegerField()
    demandprice= models.IntegerField()
    supplyprice= models.IntegerField()
    supplyqty= models.IntegerField()
    lastqty= models.IntegerField()
    high= models.IntegerField()
    low= models.IntegerField()

    