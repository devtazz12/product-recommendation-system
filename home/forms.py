from django import forms
from .models import ReviewRatingDaraz, ReviewRatingSastodeal, ReviewRatingSocheko


class ReviewFormDaraz(forms.ModelForm):
    class Meta:
        model = ReviewRatingDaraz
        fields =['review','rating']

class ReviewFormSastodeal(forms.ModelForm):
    class Meta:
        model = ReviewRatingSastodeal
        fields =['review','rating']

class ReviewFormSocheko(forms.ModelForm):
    class Meta:
        model = ReviewRatingSocheko
        fields =['review','rating']