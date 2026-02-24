from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='banners/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Paste an external banner image URL here")
    link = models.CharField(max_length=255, blank=True, null=True, help_text="Where should this banner lead to? (Optional)")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or f"Banner {self.id}"

    @property
    def get_image(self):
        if self.image_url:
            return self.image_url
        elif self.image:
            return self.image.url
        return "https://via.placeholder.com/1200x300?text=Nexara+Premium+Banner"
