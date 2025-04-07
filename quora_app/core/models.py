from django.db import models
from django.contrib.auth.models import User


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=True)

    objects = ActiveManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


class Question(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.title

class Answer(TimeStampedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_answers', blank=True)

    def total_likes(self):
        return self.likes.count()
