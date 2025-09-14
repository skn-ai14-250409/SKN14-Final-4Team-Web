# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AppProductBackup(models.Model):
    name                = models.CharField(max_length=255, blank=True, null=True)
    image_url           = models.CharField(max_length=200, blank=True, null=True)
    spec                = models.TextField(blank=True, null=True)
    material            = models.CharField(max_length=255, blank=True, null=True)
    esg_report_url      = models.CharField(max_length=200, blank=True, null=True)
    external_id         = models.CharField(max_length=32, blank=True, null=True)
    url                 = models.CharField(max_length=200, blank=True, null=True)
    composition_parts   = models.TextField(blank=True, null=True)
    details_bullets     = models.TextField(blank=True, null=True)
    details_intro       = models.TextField(blank=True, null=True)
    fit                 = models.CharField(max_length=64, blank=True, null=True)
    impact              = models.TextField(blank=True, null=True)
    made_in             = models.CharField(max_length=128, blank=True, null=True)
    price               = models.TextField(blank=True, null=True)  # This field type is a guess.
    sustainable_detail  = models.TextField(blank=True, null=True)
    sustainable_icons   = models.TextField(blank=True, null=True)
    category            = models.CharField(max_length=64, blank=True, null=True)
    color_detail        = models.CharField(max_length=64, blank=True, null=True)
    color               = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_product_backup'
