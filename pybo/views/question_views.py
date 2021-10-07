from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.http import HttpResponseRedirect

from ..forms import QuestionForm
from ..models import Question


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'pybo/question_form.html'
    login_url = '/login/'

    def get_success_url(self):
        return reverse('pybo:detail', kwargs={'question_id': self.object.id})
    

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.create_date = timezone.now()
            if self.request.FILES.get('image') != None:
                self.object.image = self.request.FILES['image']
            self.object.save()
        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    pk_url_kwarg = "question_id"
    template_name = 'pybo/question_form.html'

    def get_success_url(self):
        return reverse('pybo:detail', kwargs={'question_id': self.object.id})
    
    def test_func(self):
        # UserPassesTestMixin에서 게시글 유저와 접속 유저 비교
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.modify_date = timezone.now()
            if self.request.FILES.get('image') != None:
                self.object.image = self.request.FILES['image']
            self.object.save()
        return super().form_valid(form)


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    pk_url_kwarg = "question_id"

    def get_success_url(self):
        return reverse('pybo:index')
    
    def test_func(self):
        # UserPassesTestMixin에서 게시글 유저와 접속 유저 비교
        return self.request.user == self.get_object().author

    def get(self, request, *args, **kwargs):
        # DeleteView의 확인 절차 생략
        object = self.get_object()
        object.delete()
        return HttpResponseRedirect(self.get_success_url())