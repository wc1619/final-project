from django import forms
from fasteat.models import OrderDetail,Order
# from fasteat.models import Payment
from django.contrib.auth.models import User
from fasteat.models import UserProfile
from django.contrib.auth.forms import UserCreationForm

# PAYMENT_CHOICES = (
#     ('S', 'Stripe'),
#     ('P', 'PayPal')
# )

class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class UserForm(UserCreationForm):
    # password = forms.CharField(widget=forms.PasswordInput())
    # phone = forms.CharField(max_length=64,null=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['phone']
