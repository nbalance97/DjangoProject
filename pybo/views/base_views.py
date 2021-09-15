from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404
from django.http import Http404
from ..models import Question, Answer

MAXIMUM_POSTTYPE = 2 # 최대 게시판 개수
POSTTYPE = ['자유 게시판', '파이썬 게시판', '자바 게시판']

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
        'query': query,
    }

    return render(request, 'pybo/question_list.html', context)

def board_posts(request, board_id):
    # 해당 게시판의 게시글 정보만 가져와서 진행
    query = request.GET.get('query', '')
    board_questions = Question.objects.filter(posttype=board_id, subject__icontains=query).order_by('-create_date')

    if board_id > MAXIMUM_POSTTYPE:
        raise Http404('올바르지 않은 게시판입니다.')

    page = request.GET.get('page', 1)
    paginator = Paginator(board_questions, 10)
    page_obj = paginator.get_page(page)

    context = {
        'question_list': page_obj,
        'posttype': POSTTYPE[board_id],
    }

    return render(request, 'pybo/board_question_list.html', context)

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
