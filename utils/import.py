#!/usr/bin/env python
import sys
from BeautifulSoup import BeautifulSoup

def get_members_of_listserv(html):
    """
    takes a listserv membership list and returns a list of (name, email) tuples. 
    """
    soup = BeautifulSoup(html)
    def find_name_email_pairs(row):
        def safe_lookup(td):
            try: 
                return td.a.string.strip()
            except:
                return td.string.strip().title()
        
        return tuple(reversed([safe_lookup(td) for td in row.findAll('td')]))

    return [find_name_email_pairs(row) for row in soup.findAll('tr') if 
            row['class'].startswith('blockTableInnerRow')]

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print "Usage: import.py <listserv_html>"
    else:
        print get_members_of_listserv(open(sys.argv[1]))


