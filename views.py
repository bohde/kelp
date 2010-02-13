"""
Views that pertain to the site.
"""
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def kelp_logout(request):
    """
    Logout and send to index.
    """
    logout(request)
    return HttpResponseRedirect(reverse("kelp-index"))
