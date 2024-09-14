from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cover(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price = models.IntegerField()
    image = models.ImageField(upload_to='media',default=0)
    
class Cart(models.Model):
    cid = models.ForeignKey(Cover,db_column='cid',on_delete=models.CASCADE)
    uid = models.ForeignKey(User,db_column='uid',on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
class Order(models.Model):
    orderId=models.IntegerField()
    uid=models.ForeignKey(User,db_column='uid',on_delete=models.CASCADE)
    cid=models.ForeignKey(Cover,db_column='cid',on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)