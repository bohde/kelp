from django.db import models
import feedparser
import datetime
from parsers import default, enclosures, earth_sky

PARSER_FUNCTIONS = {
    "d":default,
    "e":enclosures,
    "s":earth_sky,
}

PARSER_CHOICES = (
    ("d", "default"),
    ("e", "enclosures"),
    ("s", "earth_sky"),
)
    
class ProgrammingFeed(models.Model):
    short_name = models.SlugField(primary_key=True)
    title = models.CharField(max_length=100)
    feed_url = models.URLField()
    etag = models.CharField(max_length=50, blank=True, editable=False)
    modified = models.DateTimeField(null=True, editable=False)
    parse_method = models.CharField(max_length=1, choices=PARSER_CHOICES, default="d")

    def __unicode__(self):
        return str(self.title)
    
    def refresh_feed(self):
        mod = self.modified.timetuple() if self.modified else None

        feed = feedparser.parse(self.feed_url, etag=self.etag, modified=mod)
        if feed.status != 200:
            return False
        self.etag = feed.etag
        self.modified = datetime.datetime(*feed.modified[0:6])
        self.save()

        process_entry = PARSER_FUNCTIONS[self.parse_method](self)

        self.new_entries = sum([ProgrammingAudio.new(**process_entry(entry)) for entry in feed.entries])
        return bool(self.new_entries)
    
class ProgrammingAudio(models.Model):
    feed = models.ForeignKey(ProgrammingFeed)
    date = models.DateTimeField()
    title = models.CharField(max_length=200, unique=True)
    length = models.CharField(max_length=20)
    link = models.URLField()
    description = models.TextField()

    class Meta:
        ordering = ("-date",)
    
    @staticmethod
    def get_feed(slug):
        return ProgrammingAudio.objects.filter(short_name=slug)

    @staticmethod
    def new(feed, date, title, length, link, description):
        try:
            return bool(feed.programmingaudio_set.create(**locals()))
        except:
            return 0
