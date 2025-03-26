from django import forms
from Movie_App.models import *

# create forms from here

class Register_Form(forms.ModelForm):

    class Meta:

        model = User

        fields = ("username","first_name","last_name","email","password")

        widgets = {
                    'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name '}),
                    'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your First Name '}),
                    'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Last Name '}),
                    'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'******@gmail.com'}),
                    'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Create a Password '})
                  }
        
        labels = {
                    'username':'User Name',
                    'first_name':'First Name',
                    'last_name':'Last Name'
                 }
        
class Login_Form(forms.Form):

    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User ID'}))

    password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}))


class Review_form(forms.ModelForm):

    class Meta:

        model = Review

        fields = ["comments","rating"]

        widgets = {
                    'comments':forms.TextInput(attrs={'class':'form-control','placeholder':'Add your comment','rows':4}),
                    'rating':forms.Select(attrs={'class':'form-control'})
                  }
        



from Movie_App.models import Review
from django.db.models import Count

# Find duplicate reviews (user-movie pairs with more than 1 review)
duplicates = (
    Review.objects.values('user_id', 'movie_id')
    .annotate(review_count=Count('id'))
    .filter(review_count__gt=1)
)

