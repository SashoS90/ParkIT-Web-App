from django import forms

from ParkItWebApp.reviews.models import Review


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
