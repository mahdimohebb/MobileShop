from django import forms
from captcha.fields import CaptchaField

class MyFormCaptcha(forms.Form):
    captcha = CaptchaField()