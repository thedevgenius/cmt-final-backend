import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from core.utils import generate_unique_slug # From your previous code
from categories.models import Category


class Business(models.Model):
    # --- Basic Information ---
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='businesses')
    primary_category = models.ForeignKey('categories.Category', on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField('categories.Category', related_name='businesses')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    handle = models.CharField(max_length=255, null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    
    # --- Contact Information ---
    phone = models.CharField(max_length=15, null=True, blank=True)
    phone_alt = models.CharField(max_length=15, null=True, blank=True)
    whatsapp = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    
    # --- Location & Spatial Data (Maps to your Geocode endpoint) ---
    address = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=6)
    city = models.ForeignKey('addresses.City', on_delete=models.SET_NULL, null=True, blank=True)

    
    # Using DecimalField for exact precision of coordinates
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    geohash = models.CharField(max_length=12, null=True, blank=True)
    
    # --- Status & Tracking ---
    is_active = models.BooleanField(default=True, help_text="Is the business visible?")
    is_verified = models.BooleanField(default=False, help_text="Has the owner been verified?")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.CharField(max_length=255, null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Businesses"
        ordering = ['-created_at']
        # Adding indexes for fields that will be heavily searched or filtered
        indexes = [
            models.Index(fields=['name'], name='biz_name_idx'),
            models.Index(fields=['slug'], name='biz_slug_idx'),
            models.Index(fields=['locality', 'city'], name='biz_location_idx'),
            models.Index(fields=['latitude', 'longitude'], name='biz_coords_idx'),
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Auto-generate a unique slug using your custom utility if one isn't provided
        if not self.slug:
            self.slug = generate_unique_slug(self.__class__, self.name, slug_field_name='slug')
        super(Business, self).save(*args, **kwargs)