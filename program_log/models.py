from django.db import models
from itertools import chain
from django.contrib.auth.models import User
from django.template import Context, Template
import datetime

# Create your models here.
class Program(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=512,null=True,blank=True)

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
        return self.start <= now <= self.end

    @staticmethod
    def next_n_hours(n):
        now = datetime.datetime.now().time()
        now = datetime.time(now.hour)
        end_hour = now.hour + n
        end = now.replace(hour=end_hour%24)
        blocks = ProgramBlock.objects.filter(start__gte=now)
        if end_hour > 23:
            blocks = blocks.order_by('start')
            blocks = chain(blocks, ProgramBlock.objects.filter(end__lte=end).order_by('start'))
        else:
            blocks = blocks.filter(end__lte=end).order_by('start')
        return blocks
	    
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

    def url(self):
        t = Template(self.program.url)
        c = Context({"pk":self.pk,
                     "active":self.active,
                     "time":self.time})
        return t.render(c)
                                
class Entry(models.Model):
    #Individual program log entry
    slot = models.ForeignKey(ProgramSlot)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    notes = models.CharField(max_length=64)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return str(self.time)

    @staticmethod
    def get_first_date():
        try:
            return Entry.objects.aggregate(min_date=models.Min('date'))['min_date']
        except IndexError:
            return None

    @staticmethod
    def add_entry(user, slot, notes, hours):
        now = datetime.datetime.now()
        diff = datetime.timedelta(hours=hours)
        today = datetime.date.today()
        start = datetime.datetime.combine(today, slot.time.start) - diff
        end = datetime.datetime.combine(today, slot.time.end) + diff
        if start < now < end :
            e = Entry.objects.create(user=user, slot=slot, notes=notes)
            return True
        return False
        
class Report(models.Model):
    class Meta:
        permissions = (
            ("view_reports", "View Reports"),
        )

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
