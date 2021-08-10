from django.db import models

class Food(models.Model):
    fno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    path = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'food'

class Attribute(models.Model):
    fno = models.OneToOneField('Food', models.DO_NOTHING, db_column='fno', primary_key=True)
    sense = models.CharField(max_length=20)
    frequency = models.IntegerField(blank=True, null=True)
    good = models.IntegerField(blank=True, null=True)
    bad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attribute'
        unique_together = (('fno', 'sense'),)

class App(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()