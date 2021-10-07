from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone

from django.urls import reverse

from django.views.generic import CreateView, UpdateView, DeleteView

from ..forms import CommentForm
from ..models import Question, Answer, Comment
from .notification_views import make_notifications


class QuestionCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'pybo/comment_form.html'
    form_class = CommentForm
    login_url = 'common:login'

    def get_success_url(self):
        return reverse('pybo:detail', kwargs={'question_id': self.object.question.id})

    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs.get('question_id'))
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.create_date = timezone.now()
        self.object.question = question
        make_notifications(self.object.question.author, "새로운 댓글이 달렸어요.", question)
        self.object.save()
        return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'pybo/comment_form.html'
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    login_url = 'common:login'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        id = 0
        if self.object.question:
            # question에 달려있는 댓글
            id = self.object.question.id
        else:
            # answer에 달려있는 댓글
            id = self.object.answer.question.id
        return reverse('pybo:detail', kwargs={'question_id': id})
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.modify_date = timezone.now()
        self.object.save()
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'
    login_url = 'common:login'

    def test_func(self):
        return self.request.user == self.get_object().author
    
    def get(self, request, *args, **kwargs):
        target_comment = self.get_object()
        id = 0
        if target_comment.question:
            # question에 달려있는 댓글
            id = target_comment.question.id
        else:
            # answer에 달려있는 댓글
            id = target_comment.answer.question.id
        target_comment.delete()
        return HttpResponseRedirect(reverse('pybo:detail', kwargs={'question_id': id}))


class AnswerCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    login_url = 'common:login'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('pybo:detail', kwargs={'question_id': self.object.answer.question.id})

    def form_valid(self, form):
        if form.is_valid():
            answer = get_object_or_404(Answer, pk=self.kwargs['answer_id'])
            form.instance.author = self.request.user
            form.instance.create_date = timezone.now()
            form.instance.answer = answer
            make_notifications(answer.author, "새로운 댓글이 달렸어요.", answer.question)
        return super().form_valid(form)

