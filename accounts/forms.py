from django import forms
from allauth.account.forms import SignupForm

class ProfileForm(forms.Form):
    site_name = forms.CharField(max_length=150, label='サイト名')
    company = forms.CharField(max_length=150, label='会社名')
    address = forms.CharField(max_length=150, label='住所', required=False)
    tel = forms.CharField(max_length=150, label='電話番号', required=False)
    fax = forms.CharField(max_length=150, label='FAX', required=False)


class SignupUserForm(SignupForm):
    site_name = forms.CharField(max_length=150, label='サイト名')
    company = forms.CharField(max_length=150, label='会社名')
    address = forms.CharField(max_length=150, label='住所')
    tel = forms.CharField(max_length=150, label='電話番号')
    fax = forms.CharField(max_length=150, label='FAX')

    def save(self, request):
        user = super(SignupUserForm, self).save(request)
        user.site_name = self.cleaned_data['site_name']
        user.company = self.cleaned_data['company']
        user.address = self.cleaned_data['address']
        user.tel = self.cleaned_data['tel']
        user.fax = self.cleaned_data['fax']
        user.save()
        return user

