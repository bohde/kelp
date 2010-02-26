from django.db import models
from itertools import chain
from django.contrib.auth.models import User
from collections import defaultdict
from functools import wraps
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

    def current(self):
        time = datetime.datetime.now()
        now = datetime.time(hour=time.hour,minute=time.minute)
        return self.start <= now <= self.end

def slotify(f):
    @wraps(f)
    def inner(user, *args, **kwargs):
        blocks = defaultdict(list)
        slots, entries = f(*args, **kwargs)
        for k,s in enumerate(slots):
            blocks[s.time].append(s)
            e = entries.get(s, False)
            if e:
                e.can_undo = (e.within_time(10) and e.is_mine(user))
            s.isdone = e
            s.time.key = k
        return sorted(((k,sorted(v, key=lambda s:s.pk)) for k,v in blocks.items()),
                      key=lambda (k,v):k.key)
    return inner

class ProgramSlot(models.Model):
    #blocks for programming
    #the active toggle is so you don't delete old
    #blocks with entries tied to them
    active = models.BooleanField()
    program = models.ForeignKey(Program)
    time = models.ForeignKey(ProgramBlock)

    def __unicode__(self):
        return str(self.time) + " - " + str(self.program)

    @staticmethod
    @slotify
    def get_slots():
        slots = ProgramSlot.objects.filter(active=True).all().select_related('program', 'time')
        slots = slots.order_by('time__start')

        def todays_entries():
            entries = {}
            for entry in Entry.objects.filter(date=datetime.datetime.today).select_related('slot'):
                entries[entry.slot] = entry
            return entries

        return slots, todays_entries()


    @staticmethod
    @slotify
    def next_n_hours(n):
        now = datetime.datetime.now().time()
        now = datetime.time(now.hour)
        end_hour = now.hour + n
        end = now.replace(hour=end_hour%24)

        today = datetime.datetime.today()

        slots = ProgramSlot.objects.filter(time__start__gte=now).select_related('program', 'time')
        entries = Entry.objects.filter(date=today).select_related('slot')
        entries = entries.filter(slot__time__start__gte=now).order_by('time')
        if end_hour > 23:
            slots = slots.order_by('time__start')
            other = ProgramSlot.objects.filter(time__end__lte=end).order_by('time__start')
            other = other.select_related('program', 'time')
            slots = chain(slots, other)

            tomorrow = today+datetime.timedelta(days=1)
            tomorrows_entries = Entry.objects.filter(date=tomorrow).filter(slot__time__end__lte=end)
            tomorrows_entries = tomorrows_entries.select_related('slot')
            tomorrows_entries = tomorrows_entries.order_by('time')
            entries = chain(entries, tomorrows_entries)
        else:
            slots = slots.filter(time__end__lte=end).order_by('time__start')
            entries = entries.filter(slot__time__end__lte=end).select_related('slot').order_by('time')


        entry_dict = {}
        for entry in entries:
            entry_dict[entry.slot] = entry
        return slots,entry_dict


                 
class Entry(models.Model):
    #Individual program log entry
    slot = models.ForeignKey(ProgramSlot)
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(auto_now_add=True)
    notes = models.CharField(max_length=64)
    user = models.ForeignKey(User)
    class Meta:
        unique_together = (("slot", "date"),)

    def __unicode__(self):
        return str(self.time)

    def is_mine(self, user):
        return user==self.user

    def within_time(self, minutes):
        return (datetime.datetime.now() - datetime.timedelta(minutes=minutes)).time() < self.time

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
        tomorrow = today + datetime.timedelta(days=1)

        # Let's see if we can add it today.
        start = datetime.datetime.combine(today, slot.time.start) - diff
        end = datetime.datetime.combine(today, slot.time.end) + diff

        if start < now < end :
            try:
                Entry.objects.create(user=user, slot=slot, notes=notes)        
            except:
                pass
            return True

        # Today didn't work, how about tomorrow?
        start = datetime.datetime.combine(tomorrow, slot.time.start) - diff
        end = datetime.datetime.combine(tomorrow, slot.time.end) + diff

        if start < now < end :
            try:
                Entry.objects.create(user=user, slot=slot, notes=notes)
            except:
                pass
            return True
        
        # Frak, the user messed up.
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
