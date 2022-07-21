from django.db import models
from userAuthentication.models import UserPersonal, User


class ProductInfo(models.Model):
    # user_id = models.ForeignKey(UserProfile, default=1, verbose_name="UserID", on_delete=models.SET_DEFAULT)
    info_id = models.AutoField(primary_key=True)
    # user_id = models.ForeignKey(User, default=1, verbose_name="UserID", on_delete=models.SET_DEFAULT)
    user_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_details = models.CharField(max_length=300)
    product_expiryDate = models.CharField(max_length=100, default="2022-05-30")
    product_price = models.CharField(max_length=100)
    product_location = models.CharField(max_length=100)

    # True: show to public; False: private
    product_visibility = models.BooleanField()
    # True: in stock; False: out of stock
    product_sold = models.BooleanField()
    # True: safe food, can be shown; False: expired, take down
    product_checkExpired = models.BooleanField(default=True)


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_info = models.ForeignKey(ProductInfo, default=1, verbose_name="ProductID", on_delete=models.SET_DEFAULT)
    product_image = models.ImageField(upload_to='product_images', default='product_images/default_img.png')
    product_category = models.CharField(max_length=100, default='Others')
