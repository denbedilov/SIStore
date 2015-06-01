__author__ = 'olesya'

import unittest
from DAL import DAL
from search_events_interface import SearchUsingAPI
from google.appengine.ext.ndb import query
from models.User import User
from models.Event import Event
from datetime import datetime

from google.appengine.ext import ndb
from google.appengine.ext import testbed


class UserDetails(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub(User)
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()
        self.mydb = DAL()
        self.obj = SearchUsingAPI()

    def test_get_user_details(self):
        self.mydb.set_user_details(10204308876621622, 'Itamar', 'Sharify')
        self.assertIsNotNone(self.mydb.get_user_details(user_id=10204308876621622))

    def test_set_name(self):
        self.mydb.set_user_details(10204308876621622, 'Itamar', 'Sharify')
        self.assertEqual(self.mydb.get_user_details(user_id=10204308876621622)['name'], "Itamar")

    def test_set_event(self):
        self.mydb.set_event_details("222342395", "Hadoop Ecosystem Workshop", datetime.now(),
                                    "Tel Aviv-Yafo",  "Kiryat Atidim", "long-story-short", "rika pedro-shoham", "http://www.meetup.com", 64, "free", "All")
        self.assertTrue(Event.check_event_exist("222342395"))

    def test_get_event_details(self):
        key = self.mydb.set_event_details("222342395", "Hadoop Ecosystem Workshop", datetime.now(),
                                    "Tel Aviv-Yafo",  "Kiryat Atidim", "long-story-short", "rika pedro-shoham", "http://www.meetup.com", 64, "free", "All")
        self.assertIsNotNone(self.mydb.get_event_details(key.id()))



    def tearDown(self):
        self.testbed.deactivate()


def main():
    unittest.main()

if __name__ == "__main__":
    main()