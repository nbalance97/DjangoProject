from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Question(models.Model):
    CHOICES = (
        (0, '자유'),
        (1, '파이썬'),
        (2, '자바'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    posttype = models.IntegerField(default=0, choices=CHOICES)
    subject = models.CharField(max_length = 200)
    modify_date = models.DateTimeField(null=True, blank=True)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_question')
    image = models.ImageField(blank=True, upload_to='Question_media')
    hits = models.IntegerField(default=0)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    modify_date = models.DateTimeField(null=True, blank=True)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_answer')

    def __str__(self):
        return "" + str(self.id)
    

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True,
                                 on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notification')
    content = models.TextField()
    arrive_date = models.DateTimeField(auto_now_add=True)
    isread = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)






