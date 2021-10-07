from pybo.views import notification_views
from django.urls import path
from .views import base_views, question_views, answer_views, comment_views, vote_views, notification_views

app_name = 'pybo'

notification_api = notification_views.NotificationViewSet.as_view({
    'get': 'get_notification_information',
})

notification_api_pk = notification_views.NotificationViewSet.as_view({
    'get': 'change_notification_status',
})

urlpatterns = [
    path('', base_views.index, name='index'),
    path('<int:question_id>/', base_views.detail, name='detail'),
    path('board/<int:board_id>/', base_views.board_posts, name='board_post'),

    # 질문 관련 처리
    path('question/create/', question_views.QuestionCreateView.as_view(), name='question_create'),
    path('question/modify/<int:question_id>/', question_views.QuestionUpdateView.as_view(), name='question_modify'),
    path('question/delete/<int:question_id>/', question_views.QuestionDeleteView.as_view(), name='question_delete'),

    # 답변 관련 처리
    path('answer/create/<int:question_id>/', answer_views.AnswerCreateView.as_view(), name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.AnswerUpdateView.as_view(), name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.AnswerDeleteView.as_view(), name='answer_delete'),
    path('answer/accept/<int:answer_id>/', answer_views.AnswerAcceptView.as_view(), name='answer_accept'),

    # 질문 댓글 관련 처리
    path('comment/create/question/<int:question_id>/', comment_views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', comment_views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', comment_views.comment_delete_question, name='comment_delete_question'),
    
    # 답변 댓글 관련 처리
    path('comment/create/answer/<int:answer_id>/', comment_views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/', comment_views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/', comment_views.comment_delete_answer, name='comment_delete_answer'),

    # 추천 관련 처리
    path('vote/question/<int:question_id>/', vote_views.vote_question, name='vote_question'),
    path('vote/answer/<int:answer_id>/', vote_views.vote_answer, name='vote_answer'),

    # API 처리
    path('API/notification/', notification_api, name="get_notification_list"),
    path('API/notification/<int:pk>/',notification_api_pk, name="set_notification_data")
]
