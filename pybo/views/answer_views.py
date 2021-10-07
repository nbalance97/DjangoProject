from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import View
from django.urls import reverse

from ..forms import AnswerForm
from ..models import Question, Answer
from .notification_views import make_notifications


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    template_name = 'pybo/answer_form.html'
    login_url = 'pybo:index'
    form_class = AnswerForm

    def get_success_url(self):
        return reverse('pybo:detail', kwargs={'question_id': self.kwargs["question_id"]})

    def form_valid(self, form):
        if form.is_valid():
            question = get_object_or_404(Question, pk=self.kwargs["question_id"])
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.create_date = timezone.now()
            self.object.question = question
            make_notifications(self.object.question.author, "새로운 답변이 달렸어요.", self.object.question)
            self.object.save()
        return super().form_valid(form)

class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    template_name = 'pybo/answer_form.html'
    login_url = 'pybo:index'
    pk_url_kwarg = 'answer_id'
    form_class = AnswerForm

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('pybo:detail', kwargs={'question_id': self.object.question.id})

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.modify_date = timezone.now()
            self.object.save()
        return super().form_valid(form)


class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    login_url = 'pybo:index'
    pk_url_kwarg = 'answer_id'

    def test_func(self):
        return self.request.user == self.get_object().author
    
    def get(self, request, *args, **kwargs):
        target_answer = self.get_object()
        question = target_answer.question.id
        target_answer.delete()
        return HttpResponseRedirect(reverse('pybo:detail', kwargs={'question_id': question}))


class AnswerAcceptView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'pybo:index'

    def test_func(self):
        target = get_object_or_404(Answer, pk=self.kwargs['answer_id'])
        return self.request.user == target.question.author

    def get(self, request, *args, **kwargs):
        target_answer = get_object_or_404(Answer, pk=self.kwargs['answer_id'])
        target_answer.accepted = True
        target_answer.save()
        return HttpResponseRedirect(reverse('pybo:detail', kwargs={'question_id': target_answer.question.id}))
