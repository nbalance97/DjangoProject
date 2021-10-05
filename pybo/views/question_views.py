from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.views.generic import CreateView
from django.urls import reverse

from ..forms import QuestionForm
from ..models import Question


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
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

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question_id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            if request.FILES.get('image') != None:
                question.image = request.FILES['image']
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question_id)

    question.delete()
    return redirect('pybo:index')
