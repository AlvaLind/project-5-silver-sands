from django.db import models


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
