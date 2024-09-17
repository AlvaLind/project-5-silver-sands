from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Wine
from django.contrib.auth.models import User


class Review(models.Model):
    """
    Stores a review for a wine with a rating and comment.
    """
    # Relationships 
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer')

    # Fields
    # Rating must be between 1 and 5
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    comment = models.TextField(max_length=1000, blank=True, null=True)
    approved = models.BooleanField(default=False)

    # Tracking fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review for {self.wine.name} by {self.id}'

    class Meta:
        ordering = ['-created_at']
