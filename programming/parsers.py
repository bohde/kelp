from BeautifulSoup import BeautifulStoneSoup
import urllib2
from dateutil import parser
from models import ProgrammingAudio

def parse_sci_am(link, limit=None):
    page = urllib2.urlopen(link)
    soup = BeautifulStoneSoup(page, convertEntities=BeautifulStoneSoup.ALL_ENTITIES)
    items = soup.findAll('item', limit=limit)

    def get_dict(item):
        dur = item.find('itunes:duration').string
        title = item.title.string
        link = item.link.string
        d = item.find('pubdate').string
        date = parser.parse(d)
        return {"duration":dur,
                "title":title,
                "link":link,
                "date":date.date()}

    return (get_dict(i) for i in items)

def load_sci():
    for d in  parse_sci_am("http://rss.sciam.com/sciam/60secsciencepodcast", 10):
        try:
            ProgrammingAudio.objects.create(short_name="sci", date=d["date"], length=d["duration"],
                                title=d["title"], audio_file=d["link"])
        except Exception, e:
            print e
    
def load_psych():
    for d in  parse_sci_am("http://rss.sciam.com/sciam/60-second-psych", 5):
        try:
            ProgrammingAudio.objects.create(short_name="psych", date=d["date"], length=d["duration"],
                                title=d["title"], audio_file=d["link"])
        except Exception, e:
            print e

