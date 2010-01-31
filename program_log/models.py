from django.db import models
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
        except IndexError:
            return datetime.today()


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