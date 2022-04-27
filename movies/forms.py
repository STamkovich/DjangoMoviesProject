from django import forms
from  .models import Reviews


class ReviewForm(forms.ModelForm):
    '''Фома отзывов'''
    class Meta:
        model = Reviews
        fields = ("name", "email", "text")