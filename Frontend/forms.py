from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from Frontend.models import BloodGroup, Blood, Product, Ambulance


# class UserAdminCreationForm(forms.ModelForm):
#     """A form for creating new users. Includes all the required
#     fields, plus a repeated password."""
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#
#     class Meta:
#         model = Users
#         fields = ('phone_number',)
#
#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(UserAdminCreationForm, self).save(commit=False)
#         print(self.cleaned_data["password1"])
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#
#
# class UserAdminChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = Users
#         fields = ('phone_number', 'password', 'active', 'admin', 'staff')
#
#     def clean_password(self):
#         # Regardless of what the user provides, return the initial value.
#         # This is done here, rather than on the field, because the
#         # field does not have access to the initial value
#         return self.initial["password"]


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        )

    def clean_username(self):
        username = self.cleaned_data["username"]
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError("Username is already exists.")
        return username

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)


class BloodGroupForm(forms.ModelForm):
    BLOOD_GROUP_OPTIONS = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )
    group = forms.ChoiceField(choices=BLOOD_GROUP_OPTIONS)

    class Meta:
        model = BloodGroup
        fields = ('group',)


class BloodForm(forms.Form):
    BLOOD_GROUP_OPTIONS = (
        ('', 'Select a value'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )
    blood = forms.ChoiceField(choices=BLOOD_GROUP_OPTIONS)
    address = forms.CharField()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'image',
            'name',
            'price',
            'description',
            'material',
        )


class AmbulanceForm(forms.ModelForm):
    class Meta:
        model = Ambulance
        fields = (
            'name',
            'details',
            'contact_number',
            'image',
            'cost'
        )
