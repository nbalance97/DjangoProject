from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404
from django.http import Http404

from django.views.generic import ListView, DetailView
from django.db.models import Count


from django.db.models import Q, F, Count

from ..models import Question, Answer

MAXIMUM_POSTTYPE = 2 # 최대 게시판 개수
MAXIMUM_DISPLAYED_COUNT = 5 # 최대 조회수 / 최대 답변 게시글 개수
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


class QuestionListView(ListView):
    model = Question
    template_name = 'pybo/question_list.html'
    paginate_by = 15
    context_object_name = 'question_list'

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        context['greatest_hits_list'] = Question.objects.order_by('-hits')[:MAXIMUM_DISPLAYED_COUNT]
        context['recently_answered_list'] = get_recently_answered_list()
        context['query'] = self.request.GET.get('query', None) 
        context['type'] = self.request.GET.get('type', None)
        context['greatest_recommended_answer'] = Answer.objects.annotate(recommend_count=Count('voter')).order_by('-recommend_count')
        return context

    def get_queryset(self):
        query = self.request.GET.get('query', None) 
        type = self.request.GET.get('type', None)
        queryset = []
        if query is None:
            queryset = Question.objects.all().order_by('-create_date')
        else:
            queryset = get_question_list_result(query, type)
        
        return queryset

class BoardQuestionListView(ListView):
    template_name = 'pybo/board_question_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BoardQuestionListView, self).get_context_data(**kwargs)
        context['posttype'] = POSTTYPE[self.kwargs['board_id']]
        context['type'] = self.request.GET.get('type', None)
        context['query'] = self.request.GET.get('query', None)

        return context

    def get_queryset(self):
        # 해당 게시판의 게시글 정보만 가져와서 진행
        query = self.request.GET.get('query', None)
        type = self.request.GET.get('type', None)
        board_id = self.kwargs['board_id']

        if board_id > MAXIMUM_POSTTYPE or board_id < 0:
            raise Http404('올바르지 않은 게시판입니다.')

        queryset = []
        if query is None:
            queryset = Question.objects.filter(posttype=board_id).order_by('-create_date')
        else:
            queryset = get_question_board_list_result(board_id, query, type)
        
        return queryset

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'pybo/question_detail.html'
    pk_url_kwarg = 'question_id'

    def get(self, request, *args, **kwargs):
        target_question = self.get_object()
        target_question.hits += 1
        target_question.save()

        return super(QuestionDetailView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        answer_page_id = self.request.GET.get('page', '1')
        answer_list = Answer.objects.filter(
            question=self.get_object()
        ).annotate(
            num_voter_count=Count('voter') 
        ).order_by(
            '-num_voter_count'
        )
        paginator = Paginator(answer_list, 3)
        page_obj = paginator.get_page(answer_page_id)
        context['answer_list'] = page_obj
        return context

