from django.shortcuts import render, redirect
from django.views import View
from accounts.models import CustomUser
from accounts.forms import ProfileForm, SignupUserForm
from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)

        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
        })



class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial = {
                'site_name': user_data.site_name,
                'company': user_data.company,
                'address': user_data.address,
                'tel': user_data.tel,
                'fax': user_data.fax,
            }
        )

        return render(request, 'accounts/profile_edit.html', {
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None,)
        if form.is_valid():
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.site_name = form.cleaned_data['site_name']
            user_data.company = form.cleaned_data['company']
            user_data.address = form.cleaned_data['address']
            user_data.tel = form.cleaned_data['tel']
            user_data.fax = form.cleaned_data['fax']
            user_data.save()
            return redirect('profile')
        
        return render(request, 'accounts/profile.html', {
            'form': form
        })


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'

class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')


class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'
    form_class = SignupUserForm


