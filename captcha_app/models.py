from django.db import models


class CaptchaNumber(models.Model):
    # save image in database, not static files
    image = models.ImageField()
    img_value = models.CharField(max_length=4)  # use CAPITAL ROMAN NUMERALS ONLY

    def __str__(self):
        return self.img_value
