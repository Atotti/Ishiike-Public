# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db.models import Q


class ClassroomAllocation(models.Model):
    lecture_id = models.CharField(primary_key=True, max_length=5)  # The composite primary key (lecture_id, campus, building, room_id) found, that is not supported. The first column is selected.
    campus = models.CharField(max_length=6)
    building = models.CharField(max_length=20)
    room_id = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'classroom_allocation'
        unique_together = (('lecture_id', 'campus', 'building', 'room_id'),)
        app_label = "search_system"


class LectureRooms(models.Model):
    campus = models.CharField(primary_key=True, max_length=6)  # The composite primary key (campus, building, room_id) found, that is not supported. The first column is selected.
    building = models.CharField(max_length=20)
    room_id = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'lecture_rooms'
        unique_together = (('campus', 'building', 'room_id'),)
        app_label = "search_system"

class SyllabusBaseInfo(models.Model):
    year = models.SmallIntegerField(blank=True, null=True)
    season = models.CharField(max_length=8, blank=True, null=True)
    day = models.CharField(max_length=30, blank=True, null=True)
    period = models.CharField(max_length=30, blank=True, null=True)
    teacher = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    lecture_id = models.ForeignKey(ClassroomAllocation, db_column='lecture_id', on_delete=models.PROTECT, primary_key=True, max_length=5, null=True)
    credits = models.SmallIntegerField(blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    faculty = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'syllabus_base_info'
        app_label = "search_system"

