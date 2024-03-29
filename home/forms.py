from django import forms
from .models import UserDetails

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'gender',
            'registration_no', 
            'institute',
            'branch',
            'campus',
            'mobile',
            'study_year',
        ]





        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'date_of_birth': 'Date of Birth',
            'gender': 'Gender',
            'registration_no': 'Registration Number',
            'institute': 'Institute (eg: GIT , GIS)',
            'branch': 'Branch',
            'campus': 'Campus',
            'mobile': 'Mobile Number',
            'study_year': 'Study Year',
            'profile_image': 'Profile Image (size less than 1Mb & optional)',
            'bio': 'Bio (optional)',
            'instagram_link': 'Instagram Link (optional)',
            'linkedin_link': 'Linkedin Link (optional)',
            'github_link': 'GitHub Link (optional)',
            'tryhackme_link': 'TryHackMe Link (optional)',
            'hackthebox_link': 'Hack The Box Link (optional)',
            'discord_link': 'Discord Link (optional)',
        }

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date' , 'placeholder': 'date of birth'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'registration_no': forms.TextInput(attrs={'placeholder': 'Registration Number'}),
            'institute': forms.TextInput(attrs={'placeholder': 'Institute (eg: GIT , GIS)'}),
            'branch': forms.TextInput(attrs={'placeholder': 'Branch'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Mobile Number'}),
            'study_year': forms.Select(attrs={'placeholder': 'Study Year'}),
        }

        error_messages = {
            'first_name': {'required': 'Please enter your first name.'},
            'last_name': {'required': 'Please enter your last name.'},
            'email': {'required': 'Please enter your email address.'},
            'date_of_birth': {'required': 'Please enter your date of birth.'},
            'gender': {'required': 'Please select your gender.'},
            'registration_no': {'required': 'Please enter your registration number.'},
            'institute': {'required': 'Please enter your institute name.'},
            'branch': {'required': 'Please enter your branch or major.'},
            'campus': {'required': 'Please enter your campus or location.'},
            'mobile': {'required': 'Please enter your mobile number.'},
            'study_year': {'required': 'Please select your study year.'},
            'profile_image': {'required': 'Please upload your profile image.'},
        }

    def __init__(self, *args, **kwargs):
        super(UserDetailsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['email'].widget.attrs['readonly'] = 'readonly'
        