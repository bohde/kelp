from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class DiskJockey(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=35)
    seniority = models.IntegerField(default=0)
    email = models.EmailField(max_length=64)


class Semester(models.Model):
    name = models.CharField(max_length=16)
    start = models.DateField()
    end = models.DateField()

DAY_CHOICES = (
  ('Monday', 'Mon'),
  ('Tuesday', 'Tues'),
  ('Wednesday', 'Wed'),
  ('Thursday', 'Thurs'),
  ('Friday', 'Fri'),
  ('Saturday', 'Sat'),
  ('Sunday', 'Sun'),
)

class ShowBlock(models.Model):
    day = models.CharField(max_length=10,choices=DAY_CHOICES)
    start = models.TimeField()
    end = models.TimeField()
    semester = models.ForeignKey(Semester)

class Show(models.Model):
    name = models.CharField(max_length=75)
    type = models.TextField()
    block = models.ForeignKey(ShowBlock,blank=True,null=True)
    dj = models.ForeignKey(DiskJockey)

class pick(models.Model):
    #this will be used for sorting through
    #show selections
    block = models.ForeignKey(ShowBlock)
    show = models.ForeignKey(Show)
    rank = models.IntegerField()

