import urllib2
import feedparser
from dateutil import parser

def take_first_key(e,*keys):
    for k in keys:
        v = e.get(k, '')
        if v:
            return v
    return ''

def default(feed):
    kwargs = {"feed":feed}
    def process_entry(entry):
        tfk = lambda *keys: take_first_key(entry, *keys)
        kwargs["date"] = parser.parse(tfk("date")).date()
        kwargs["title"] = tfk("title")
        kwargs["length"] = tfk("duration", "itunes_duration")
        kwargs["link"] = tfk("link")
        try:
            kwargs["description"] = entry.content[0].value
        except AttributeError:
            kwargs["description"] = tfk("summary", "description")
        return kwargs
    return process_entry

def enclosures(feed):
    kwargs = {"feed":feed}
    def process_entry(entry):
        tfk = lambda *keys: take_first_key(entry, *keys)
        kwargs["date"] = parser.parse(tfk("date")).date()
        kwargs["title"] = tfk("title")
        kwargs["length"] = tfk("duration", "itunes_duration")
        kwargs["link"] = entry.enclosures[0]["href"]
        try:
            kwargs["description"] = entry.content[0].value
        except AttributeError:
            kwargs["description"] = tfk("summary", "description")
        return kwargs
    return process_entry
    
def earth_sky(feed):
    kwargs = {"feed":feed}
    def process_entry(entry):
        tfk = lambda *keys: take_first_key(entry, *keys)
        kwargs["date"] = parser.parse(tfk("date")).date()
        kwargs["title"] = tfk("title")
        kwargs["length"] = "1:30"
        try:
            kwargs["link"] = [e["href"] for e in entry.enclosures
                              if e["href"].endswith("-90.mp3")][0]
        except:
            return None
        try:
            kwargs["description"] = entry.content[0].value
        except AttributeError:
            kwargs["description"] = tfk("summary", "description")
        return kwargs
    return process_entry
