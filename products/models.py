from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Paste an external image URL here")

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def get_image(self):
        if self.image_url:
            return self.image_url
        elif self.image:
            return self.image.url
        return "https://via.placeholder.com/64"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Paste an external image URL here")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def get_image(self):
        if self.image_url:
            return self.image_url
        elif self.image:
            return self.image.url
        return "https://via.placeholder.com/200"

    def __str__(self):
        return self.name
