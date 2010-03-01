from django.db import models
import feedparser
import dateutil
import datetime
    
class ProgrammingFeed(models.Model):
    short_name = models.SlugField(primary_key=True)
    program = models.ForeignKey('program_log.Program')
    feed_url = models.URLField()
    etag = models.CharField(max_length=50, blank=True, editable=False)
    modified = models.DateTimeField(null=True, editable=False)
    
    def refresh_feed(self):
        kwargs = {}

        mod = self.modified.timetuple() if self.modified else None

        feed = feedparser.parse(self.feed_url, etag=self.etag, modified=mod)
        if feed.status != 200:
            return False
        self.etag = feed.etag
        self.modified = datetime.datetime(*feed.modified[0:6])
        self.save()

        kwargs["feed"] = self

        def process_entry(entry):
            def take_first_key(*keys):
                for k in keys:
                    v = entry.get(k, '')
                    if v:
                        return v
                return ''
            tfk = take_first_key
            kwargs["date"] = dateutil.parser.parse(tfk("date")).date()
            kwargs["title"] = tfk("title")
            kwargs["length"] = tfk("duration", "itunes_duration")
            kwargs["link"] = tfk("link")
            try:
                kwargs["description"] = entry.content[0].value
            except AttributeError:
                kwargs["description"] = tfk("summary", "description")
            return ProgrammingAudio.new(**kwargs)

        self.new_entries = sum([process_entry(entry) for entry in feed.entries])
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
