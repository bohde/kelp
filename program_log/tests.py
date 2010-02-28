"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User

from models import Entry, ProgramSlot

import os
import datetime

TEST_ROOT = os.path.dirname(os.path.realpath(__file__))


class EntryTests(TestCase):
    fixtures = [os.path.join(TEST_ROOT,"test_fixtures/entries.json")]
    urls = "program_log.urls"
    
    def setUp(self):
        if not(self.client.login(username="admin", password="admin")):
            self.fail("Couldn't log in.")
        
    def testUndoMyEntry(self):
        try:
            s = get_object_or_404(ProgramSlot, pk=1)
            u = get_object_or_404(User, pk=1)
            e = Entry(pk=2, notes="", slot=s, user=u)
            e.save()
        except Http404, e:
            self.fail("Something doesn't exist.")
            
        res = self.client.get("/undo/2")
        self.assertEquals(res.status_code, 302)

        try:
            get_object_or_404(Entry, pk=1)
            self.fail("Entry 1 shouldn't exist.")
        except:
            pass
        
    def testNotMyEntry(self):
        try:
            e = get_object_or_404(Entry, pk=1)
            u = get_object_or_404(User, pk=2)
            e.user = u
            e.save()
        except Http404, e:
            self.fail("Entry 1 doesn't exist.")
            
        res = self.client.get("/undo/1")
        self.assertEquals(res.status_code, 404)

        try:
            get_object_or_404(Entry, pk=1)
        except:
            self.fail("Entry 1 was deleted when it shouldn't have been.")

    def testTimeOutOfRange(self):
        try:
            e = get_object_or_404(Entry, pk=1)
            self.assertTrue(e.time  > (datetime.datetime.now() + datetime.timedelta(minutes=10)).time(), "The time on the entry is not older than 10 minutes!")
        except Http404, e:
            self.fail("Entry 1 doesn't exist.")
            
        res = self.client.get("/undo/1")
        self.assertEquals(res.status_code, 403)

        try:
            get_object_or_404(Entry, pk=1)
        except:
            self.fail("Entry 1 was deleted when it shouldn't have been.")
