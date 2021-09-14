from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404
from ..models import Question, Answer


def index(request):
    page = request.GET.get('page', '1')
    query = request.GET.get('query', '')
    question_list = Question.objects.filter(subject__contains=query).order_by('-create_date')
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    # 최다 조회수
    greatest_hits_list = Question.objects.order_by('-hits')[:3]

    # 최근에 답변이 달린 게시글
    temp = Answer.objects.order_by('-create_date').values('question')
    recently_answered_list = []
    duplicated = set()

    # 하나의 게시글에 여러개의 답변이 달릴 수 있으므로 중복 제거
    for answered_question in temp:
        if answered_question['question'] not in duplicated:
            duplicated.add(answered_question['question'])
            recently_answered_list.append(answered_question['question'])
            if len(recently_answered_list) == 3:
                break

    recently_answered_list = Question.objects.filter(id__in=recently_answered_list)
    context = {
        'question_list': page_obj,
        'greatest_hits_list': greatest_hits_list, 
        'recently_answered_list': recently_answered_list,
    }

    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answer_page_id = request.GET.get('page', '1')

    # 조회수 갱신
    question.hits += 1
    question.save()

    # Answer Pagination
    paginator = Paginator(Answer.objects.filter(question=question), 3)
    page_obj = paginator.get_page(answer_page_id)

    context = {'question': question, 'answer_list': page_obj}
    return render(request, 'pybo/question_detail.html', context)
