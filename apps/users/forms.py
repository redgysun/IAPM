from django import forms
from .models import UserProfile

class UserLoginForm(forms.Form):
    username = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=8,max_length=20,error_messages={
        'required':'密码必须填写',
        'min_length':'密码至少8位',
        'max_length':'密码不能超过20位'
    })

class UserRegisterForm(forms.Form):
    username = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8, max_length=20, error_messages={
        'required': '密码必须填写',
        'min_length': '密码至少8位',
        'max_length': '密码不能超过20位'
    })


class UserChangePasswordForm(forms.Form):
    password = forms.CharField(required=True,min_length=8,max_length=20,error_messages={
        'required':'密码必须填写',
        'min_length':'密码至少8位',
        'max_length':'密码不能超过20位'
    })
    password1 = forms.CharField(required=True,min_length=8,max_length=20,error_messages={
        'required':'密码必须填写',
        'min_length':'密码至少8位',
        'max_length':'密码不能超过20位'
    })


# class UserChangeImageForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['user_image']

class UserChangeInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'user_gender', 'user_phone','user_birthday', 'user_PQ']
