from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ImageBaseModel(models.Model):
    image = None
    image_svg = None

    @property
    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        if self.image_svg and hasattr(self.image_svg, 'url'):
            return self.image_svg.url
        else:
            return 'static/assets/imgs/net-foto.jpg'

    class Meta:
        abstract = True
