from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,UserProfile,ArtWork

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
