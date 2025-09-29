# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AppProduct(models.Model):
    name          = models.TextField(blank=True, null=True)
    image_url     = models.TextField(blank=True, null=True)
    spec          = models.TextField(blank=True, null=True)
    external_id   = models.TextField(blank=True, null=True)
    url           = models.TextField(blank=True, null=True)
    color         = models.TextField(blank=True, null=True)
    price         = models.FloatField(blank=True, null=True)
    category      = models.TextField(blank=True, null=True)
    color_detail  = models.TextField(blank=True, null=True)
    brand_id      = models.IntegerField(blank=True, null=True)
    co2_saved_kg  = models.TextField(blank=True, null=True)
    currency      = models.TextField(blank=True, null=True)
    water_saved_l = models.TextField(blank=True, null=True)
    material      = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_product'
