from django.core.management.base import BaseCommand
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

    return (find_name_email_pairs(row) for row in soup.findAll('tr'))

def filter_to_mst_addresses(address_tuples):
    return list(set(((str(email).partition("@")[0] , name, email) for name, email in address_tuples if str(email).endswith("@mst.edu"))))

def get_emails(f):
    return filter_to_mst_addresses(get_members_of_listserv(open(f)))

def add_users(users):
    def add_user(user):
        u,created = User.objects.get_or_create(username=user[0])
        u.email = user[2]
        u.first_name = user[1]
        u.save()
        return created
    return sum(add_user(user) for user in users)
        

class Command(BaseCommand):
    help = "Import users from the html of the listserv output."

    def handle(self, *args, **options):
        if not len(args):
            print "Usage: ./manage.py import_user_list.py <file_1> [<file_2>...]"
            return
        for l in args:
            print "Adding users from file: %s" % l
            users = get_emails(l)
            print "Found %u unique users." % len(users)
            print "Created %u new users." % add_users(users)
