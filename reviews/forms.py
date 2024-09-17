from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),  # 1 to 5 star rating
            'comment': forms.Textarea(attrs={
                'placeholder': 'Write your review here...',
                'rows': 4,
                'cols': 40,
                'class': 'form-control',
            }),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not (1 <= rating <= 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating
