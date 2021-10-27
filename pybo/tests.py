from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User


from .models import Question

'''
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    posttype = models.IntegerField(default=0, choices=CHOICES)
    subject = models.CharField(max_length = 200)
    modify_date = models.DateTimeField(null=True, blank=True)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_question')
    image = models.ImageField(blank=True, upload_to='Question_media')
    hits = models.IntegerField(default=0)
'''

class QuestionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='aa', password='bb')

        target_question = Question.objects.create(
                author=user,
                posttype=2,
                subject='test',
                modify_date=timezone.now(),
                create_date=timezone.now(),
                content='test',
        )

        cls.question_id = target_question.id

    
    def setUp(self):
        self.client = Client()

    def test_hit_count(self):
        # 게시글 조회시 제대로 조회수가 1 증가하는지 테스트 (22번 게시글 기준)
        target_question = Question.objects.get(id=self.question_id)
        expect_hits = target_question.hits
        self.client.get(reverse('pybo:detail', kwargs={'question_id': self.question_id}))
        self.assertIs(Question.objects.get(id=self.question_id).hits, expect_hits)

