from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404
from django.http import Http404

from django.db.models import Q

from ..models import Question, Answer

MAXIMUM_POSTTYPE = 2 # 최대 게시판 개수
MAXIMUM_DISPLAYED_COUNT = 3 # 최대 조회수 / 최대 답변 게시글 개수
POSTTYPE = ['자유 게시판', '파이썬 게시판', '자바 게시판']

def get_recently_answered_list():
    # 최근에 답변이 달린 게시글
    temp = Answer.objects.order_by('-create_date').values('question')
    recently_answered_question_id = set()

    # 하나의 게시글에 여러개의 답변이 달릴 수 있으므로 중복 제거
    for answered_question in temp:
        recently_answered_question_id.add(answered_question['question'])
        if len(recently_answered_question_id) == MAXIMUM_DISPLAYED_COUNT:
            break
    
    recently_answered_list = Question.objects.filter(id__in=list(recently_answered_question_id))
    return recently_answered_list


def get_question_list_result(query, type):
    if type == 'title':
        return Question.objects.filter(subject__icontains=query).order_by('-create_date')
    elif type == 'title_content':
        return Question.objects.filter(Q(subject__icontains=query) or Q(content__icontains=query)).order_by('-create_date')
    elif type == 'author':
        return Question.objects.filter(author__username__icontains=query).order_by('-create_date')

def get_question_board_list_result(board_id, query, type):
    if type == 'title':
        return Question.objects.filter(posttype=board_id).filter(subject__icontains=query).order_by('-create_date')
    elif type == 'title_content':
        return Question.objects.filter(posttype=board_id).filter(Q(subject__icontains=query) or Q(content__icontains=query)).order_by('-create_date')
    elif type == 'author':
        return Question.objects.filter(posttype=board_id).filter(author__username__icontains=query).order_by('-create_date')


def index(request):
    page = request.GET.get('page', '1')
    query, type = request.GET.get('query', None), request.GET.get('type', None)
    question_list = []

    # query가 없으면 전체 데이터, 있으면 검색 결과만 표시
    if query is None:
        question_list = Question.objects.all().order_by('-create_date')
    else:
        question_list = get_question_list_result(query, type)

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    # 최다 조회수
    greatest_hits_list = Question.objects.order_by('-hits')[:MAXIMUM_DISPLAYED_COUNT]
    recently_answered_list = get_recently_answered_list()

    context = {
        'question_list': page_obj,
        'greatest_hits_list': greatest_hits_list, 
        'recently_answered_list': recently_answered_list,
        'query': query,
        'type': type,
    }

    return render(request, 'pybo/question_list.html', context)


def board_posts(request, board_id):
    # 해당 게시판의 게시글 정보만 가져와서 진행
    query, type = request.GET.get('query', None), request.GET.get('type', None)
    board_questions = []
    if query is None:
        board_questions = Question.objects.filter(posttype=board_id).order_by('-create_date')
    else:
        board_questions = get_question_board_list_result(board_id, query, type)
    
    
    if board_id > MAXIMUM_POSTTYPE:
        raise Http404('올바르지 않은 게시판입니다.')
    print(board_questions)
    page = request.GET.get('page', 1)
    paginator = Paginator(board_questions, 10)
    page_obj = paginator.get_page(page)

    context = {
        'question_list': page_obj,
        'posttype': POSTTYPE[board_id],
        'query': query,
        'type': type
    }

    return render(request, 'pybo/board_question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answer_page_id = request.GET.get('page', '1')

    # 조회수 갱신
    question.hits += 1
    question.save()

    # Answer Pagination, 추천수 정렬
    paginator = Paginator(Answer.objects.filter(question=question).order_by('-voter'), 3)
    page_obj = paginator.get_page(answer_page_id)

    context = {'question': question, 'answer_list': page_obj}
    return render(request, 'pybo/question_detail.html', context)
