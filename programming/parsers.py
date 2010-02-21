from BeautifulSoup import BeautifulStoneSoup
import urllib2

def parse_sci_am(link, limit=5):
    page = urllib2.urlopen(link)
    soup = BeautifulStoneSoup(page)
    items = soup.findAll('item', limit=limit)

    def get_dict(item):
        dur = item.find('itunes:duration').string
        title = item.title.string
        link = item.link.string
        date = item.find('pubdate').string
        return {"duration":dur,
                "title":title,
                "link":link,
                "date":date}

    return (get_dict(i) for i in items)

def get_sci():
    return parse_sci_am("http://rss.sciam.com/sciam/60secsciencepodcast")

def get_psych():
    return parse_sci_am("http://rss.sciam.com/sciam/60-second-psych", 10)
