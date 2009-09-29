from django.db import models

# Create your models here.

class Schedule(models.Model):
	active		=	models.BooleanField()
	name		=	models.CharField(max_length=64)
	url		=	models.CharField(max_length=64)
	#military style hour 0-23
	scheduled	=	models.IntegerField(default=0)

class Entry(models.Model):
	Schedule	=	models.ForeignKey(Schedule)
	played		=	models.DateTimeField()
	notes		=	models.CharField(max_length=64)

class DiskJockey(models.Model):
	name		=	models.CharField(max_length=35)
	seniority	=	models.IntegerField(default=0)
	email		=	models.EmailField(max_length=64)


class Semester(models.Model):
	name		=	models.CharField(max_length=16)
	start		=	models.DateField()
	end			=	models.DateField()

DAY_CHOICES = (
  ('Monday', 'Mon'),
  ('Tuesday', 'Tues'),
  ('Wednesday', 'Wed'),
  ('Thursday', 'Thurs'),
  ('Friday', 'Fri'),
  ('Saturday', 'Sat'),
  ('Sunday', 'Sun'),
)

class Block(models.Model):
	day			=	models.CharField(max_length=10,choices=DAY_CHOICES)
	start		=	models.TimeField()
	end			=	models.TimeField()
	semester	=	models.ForeignKey(Semester)


class Show(models.Model):
	name		=	models.CharField(max_length=75)
	type		=	models.TextField()
	block		=	models.ForeignKey(Block,blank=True,null=True)
	dj			=	models.ForeignKey(DiskJockey)

class pick(models.Model):
	block		=	models.ForeignKey(Block)
	show		=	models.ForeignKey(Show)
	rank		=	models.IntegerField()