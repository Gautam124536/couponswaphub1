from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
   name= models.CharField(max_length=255)

   class Meta:
      ordering=('name',)
      verbose_name_plural='Categories'

   def __str__(self):
      return self.name

class Coupon(models.Model):
   category=models.ForeignKey(Category,related_name='coupons',on_delete=models.CASCADE)
   name=models.CharField(max_length=255)
   description=models.TextField(blank=True,null=True)
   image=models.ImageField(upload_to='coupon_images',blank=True,null=True)
   is_booked=models.BooleanField(default=False)
   published_by=models.ForeignKey(User,related_name='coupon',on_delete=models.CASCADE)
   published_at=models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.name