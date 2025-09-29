from django.contrib.auth.models import User
from django.db import models

from .search_history import SearchHistory


class Like(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes", null=True)
    search   = models.ForeignKey(SearchHistory, on_delete=models.CASCADE, related_name="likes", null=True)
    liked_at = models.DateTimeField(auto_now_add=True)