from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,UserProfile,ArtWork,Discount,Review

class RegisterForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=["username","email","password1","password2","role"]

class SignInForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class ProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["profile_picture","phone"]

class CategoryForm(forms.Form):
    category_choices=(
        ("digitalpaint","Digital Painting"),
        ("3D model","3D model Art"),
        ("floralart","Floral Art"),
        ("fractalart","Fractal Art"),
        ("illustrations","Illustrations"),
        ("pixelart","Pixel Art"),
        ("vectorart","Vector Art")
    )
    category_type=forms.ChoiceField(choices=category_choices)

class ArtWorkForm(forms.ModelForm):
    class Meta:
        model=ArtWork
        fields=["title","description","picture","price","category_object"]
        labels={
            "category_object":"Category"
        }
        widgets={
            "title":forms.TextInput(attrs={'class':'form-control'}),
            "description":forms.Textarea(attrs={'class':'form-control'}),
            "picture":forms.FileInput(attrs={'class':'form-control'}),
            "price":forms.NumberInput(attrs={'class':'form-control'}),
            "category_object":forms.Select(attrs={'class':'form-control form-select'})

        }

class DiscountForm(forms.ModelForm):
    class Meta:
        model=Discount
        fields=['art','discount_price','start_date','end_date']
        widgets={
            'start_date':forms.DateInput(attrs={'type':'date'}),
            'end_date':forms.DateInput(attrs={'type':'date'})
        }

        def clean(self):
            cleaned_data=super().clean
            start_date=cleaned_data.get('start_date')
            end_date=cleaned_data.get('end_date')
            if start_date and end_date and start_date>end_date:
                raise forms.ValidationError("Start date cannot be after end date")
            return cleaned_data
        

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=["art_object","ratings","review_message"]
        labels={
            "art_object":"Art Works"
        }
        widgets = {
            'ratings': forms.Select(choices=[(str(i), str(i)) for i in range(1, 6)]),  
            'review_message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        }