from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Program(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=64,null=True,blank=True)

    def __unicode__(self):
        return str(self.name)
                
class ProgramBlock(models.Model):
    start = models.TimeField()
    end = models.TimeField()

    def __unicode__(self):
        return str(self.start)

    def slots(self):
        slots = ProgramSlot.objects.filter(time=self)
	return slots

    def current(self):
	time = datetime.datetime.now()
	now = datetime.time(hour=time.hour,minute=time.minute)
	if now >= self.start:
            if now <= self.end:
                return True
	    return False
	    
class ProgramSlot(models.Model):
    #blocks for programming
    #the active toggle is so you don't delete old
    #blocks with entries tied to them
    active = models.BooleanField()
    program = models.ForeignKey(Program)
    time = models.ForeignKey(ProgramBlock)

    def __unicode__(self):
        return str(self.time) + " - " + str(self.program)

    def isdone(self):
        try:
            e = Entry.objects.filter(date=datetime.datetime.today).get(slot=self)
            return e
        except:
            return False
                                
class Entry(models.Model):
    #Individual program log entry
    slot = models.ForeignKey(ProgramSlot)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    notes = models.CharField(max_length=64)
    
    def __unicode__(self):
        return str(self.time)

    @staticmethod
    def get_first_date():
        try:
            return Entry.objects.aggregate(min_date=models.Min('date'))['min_date']
        except IndexError as e:
            return datetime.today()


class Report(models.Model):
    #Used to generate reports for program director
    slug = models.SlugField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    program = models.ManyToManyField(Program)
    
    def __unicode__(self):
        return str(self.slug)

class Quarter(models.Model):
    #Used for defining quaters. This shouldn't change, but what the hell.
    id = models.SlugField(max_length=3,primary_key=True, unique=True)
    begin = models.DateField()
    end = models.DateField()

    def __unicode__(self):
        return str(self.id)

                
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
