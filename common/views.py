from django.shortcuts import render, redirect, reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin, UserPassesTestMixin

from django.db.models import Count

from pybo.models import Answer, Question

from django.views.generic import UpdateView, DetailView
from django.core.paginator import Paginator

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

class UserPasswordChangeView(
    LoginRequiredMixin, UserPassesTestMixin, PasswordChangeView
    ):
    model = User
    template_name = 'common/passwordchange.html'
    pk_url_kwarg = 'user_id'

    def get_success_url(self):
        return reverse('index')

    def test_func(self, user):
        return self.request.user == user

class UserProfileView(DetailView):
    model = User
    template_name = 'common/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = "target_user"

    def get_context_data(self, **kwargs):
        queryset = super().get_context_data(**kwargs)
        target_user = self.get_object()

        questions_page = self.request.GET.get('questions_page', 1)
        answer_page = self.request.GET.get('answer_page', 1)

        question_paginator = Paginator(target_user.author_question.all().order_by('id'), 6)

        answer_question = target_user.author_answer.values('question').distinct()
        answer_question = Question.objects.filter(id__in=answer_question)
        answer_paginator = Paginator(answer_question, 6)

        queryset["total_accepted"] = Answer.objects.filter(author=target_user, accepted=True).count()
        queryset['target_questions'] = question_paginator.get_page(questions_page)
        queryset['target_answered_questions'] = answer_paginator.get_page(answer_page)
        return queryset



