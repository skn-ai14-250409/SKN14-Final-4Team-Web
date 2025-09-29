# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class SearchHistory(models.Model):
    user_id         = models.IntegerField(blank=True, null=True)
    look_style      = models.CharField(max_length=256, blank=True, null=True)
    look_img_url    = models.CharField(max_length=300, blank=True, null=True)
    look_desc       = models.TextField(blank=True, null=True)
    searched_at     = models.DateTimeField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'search_history'
