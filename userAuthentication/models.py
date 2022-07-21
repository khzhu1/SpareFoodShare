from django.db import models
from django.contrib.auth.models import User


class UserPersonal(models.Model):
    user_form = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=100,
        choices=(("Individual", "Individual"),
                 ("Business", "Business"))
    )
    user_image = models.ImageField(blank=True,
                                   null=True,
                                   default="product_images/profilephoto.png"
                                   )

