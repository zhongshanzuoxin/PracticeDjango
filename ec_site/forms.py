from django import forms
from .models import ShippingAddress
from allauth.account.forms import SignupForm

class SignupUserForm(SignupForm):
    full_name = forms.CharField(max_length=30, label='名前')

    def save(self, request):
        user = super(SignupUserForm, self).save(request)
        user.full_name = self.cleaned_data['full_name']
        user.save()
        return user

class ProfileForm(forms.Form):
    full_name = forms.CharField(max_length=30, label='名前')

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['postal_code', 'prefectures', 'city', 'address_line1', 'address_line2', 'phone_number']
