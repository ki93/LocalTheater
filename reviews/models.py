from django.db import models
from django.conf import settings
# board app의 model import
from board.models import Room
from django.contrib.auth.models import User

# Create your models here.
class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # on_delete 무조건 필요함...(강사님에게 여쭤보기)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # textfield가 크기가 커서 글 작성에 적합함
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

