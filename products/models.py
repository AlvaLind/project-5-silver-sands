from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


class Category(models.Model):
    """
    Represents a category for wines in the inventory.
    Each category has a unique name. 
    Order alphabetically based on 'name'.
    """
    # Fields 
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True, null=True, max_length=600)

    class Meta: 
        ordering =["name"]
    
    def __str__(self):
        return self.name


class Wine(models.Model):
    """
    Stores a single wine entry related to :model:'products/Category'

    Admin can add wine objects to the database via this Model.

    Order wines in queries defaults to descending order based on 'published_year'.

    Overrides the default save method to ensure each wine has a unique slug.
    Raises a ValidationError if attempting to save a wine with a non-unique slug.
    """
    # Closure options
    CLOSURE_CHOICES = [
        ('natural cork', 'Natural Cork'),
        ('synthetic cork', 'Synthetic Cork'),
        ('agglomerate cork', 'Agglomerate Cork'),
        ('screw cap', 'Screw Cap'),
        ('champagne cork', 'Champagne Cork'),
        ('capped cork', 'Capped Cork'),
    ]

    # Relationships 
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='wines')

    # Fields
    name = models.CharField(max_length=50)
    sku = models.CharField(max_length=254, null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    vintage = models.PositiveIntegerField()
    volume = models.PositiveIntegerField()  # Volume in millilitres
    closure = models.CharField(max_length=20, choices=CLOSURE_CHOICES)
    abv = models.DecimalField(max_digits=4, decimal_places=2)
    acidity = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    residual_sugar = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    image = CloudinaryField('image', blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    available = models.BooleanField(default=True)
    
    # Tracking fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        ordering =["-vintage"]

    def __str__(self):
        return self.name

    # Override the save method to auto generate the slug and check uniqueness
    def save(self, *args, **kwargs):
        # Automatically generate the slug from the name if not provided
        if not self.slug or not self.slug == slugify(self.name):
            self.slug = slugify(self.name)

        # Check if the slug is unique before saving
        if Wine.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            raise ValidationError(f"A wine with the slug '{self.slug}' already exists.")

        super(Wine, self).save(*args, **kwargs)
