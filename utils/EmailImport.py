#!/usr/bin/env python
import sys
from BeautifulSoup import BeautifulSoup

from django.contrib.auth.models import User

def get_members_of_listserv(html):
    """
    takes a listserv membership list and returns a list of (name, email) tuples. 
    """
    soup = BeautifulSoup(html)
    def find_name_email_pairs(row):
        def safe_lookup(td):
            try: 
                return td.a.string.strip().lower()
            except:
                return td.string.strip().title()
        
        return tuple(reversed([safe_lookup(td) for td in row.findAll('td')]))

    return (find_name_email_pairs(row) for row in soup.findAll('tr') if 
            row['class'].startswith('blockTableInnerRow'))

def filter_to_mst_addresses(address_tuples):
    return ((str(email).partition("@")[0] , name, email) for name, email in address_tuples if str(email).endswith("@mst.edu"))

def get_emails(f):
    return filter_to_mst_addresses(get_members_of_listserv(open(f)))

def add_users(users):
    for user in users:
        u = User.objects.create_user(user[0], user[2])
        u.first_name = user[1]
        u.save()

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print "Usage: import.py <listserv_html>"
    else:
        l = get_emails(sys.argv[1])
        print len(l)
        print l


