from django.shortcuts import render, redirect, reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import UpdateView

from common.forms import UserForm, UserModifyForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

class UserModifyView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserModifyForm
    template_name = 'common/signup.html'
    pk_url_kwarg = 'user_id'

    def get_success_url(self):
        return reverse('index')

    def test_func(self, user):
	    return self.request.user == user




