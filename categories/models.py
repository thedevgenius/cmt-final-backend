import uuid
from django.db import models
from django.utils.text import slugify
from core.utils import generate_unique_slug
# Create your models here.
class Category(models.Model):
    CATEGORY_TYPE = (
        ('DEF', 'Default'),
        ('DOC', 'Doctor Speciality'),
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    icon_class = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True)
    order = models.IntegerField(default=0)
    category_type = models.CharField(max_length=5, choices=CATEGORY_TYPE, default='DEF')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.CharField(max_length=255, null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        db_table = 'categories'
        indexes = [
            models.Index(fields=['name'], name='name_idx'),
            models.Index(fields=['slug'], name='slug_idx'),
            models.Index(fields=['parent'], name='parent_idx'),
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name, slug_field_name='slug')
        super(Category, self).save(*args, **kwargs)


