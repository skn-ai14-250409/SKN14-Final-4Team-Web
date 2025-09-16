import re
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from mainapp.models.influencer import Influencer


# Create your models here.

class ChatHistory(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")
    influencer    = models.ForeignKey(Influencer, on_delete=models.CASCADE, related_name="chats", default=1)
    talker_type   = models.CharField(max_length=4)
    style_text    = models.TextField()
    optional_text = models.TextField(blank=True, null=True)
    voice_url     = models.CharField(max_length=256, null=True)
    talked_at     = models.DateTimeField(auto_now_add=True)

    @property
    def time(self):
        return self.talked_at.strftime("%H:%M %p")

    @property
    def log_time(self):
        now   = datetime.now()
        diff  = now - self.talked_at
        hours = diff.seconds // 3600
        if hours > 24:   return f"{diff.days} 일 전"
        elif hours > 0:  return f"{hours} 시간 전"
        else:            return self.time

    @property
    def is_user(self):
        return self.talker_type == "user"

    @property
    def text_only(self):
        return re.sub(r"</?\w+[^>]*>", "", self.style_text)

    class Meta:
        ordering = ['-talked_at']