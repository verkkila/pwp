import unittest
import sys
sys.path.append("../")

from diary import create_app

tc = create_app().test_client()

class TestBasic(unittest.TestCase):
    def test_hello_world(self):
        resp = tc.get("/")
        assert resp.status_code == 200

class TestScheduleCollection(unittest.TestCase):
    def test_get(self):
        pass

    def test_post(self):
        pass

class TestSchedule(unittest.TestCase):
    def test_get(self):
        pass

    def test_put(self):
        pass

    def test_delete(self):
        pass

class TestEventCollection(unittest.TestCase):
    def test_get(self):
        pass

    def test_post(self):
        pass

class TestEvent(unittest.TestCase):
    def test_get(self):
        pass
    
    def test_patch(self):
        pass

    def test_delete(self):
        pass

class TestTaskCollection(unittest.TestCase):
    def test_get(self):
        pass

    def test_post(self):
        pass

class TestTask(unittest.TestCase):
    def test_get(self):
        pass

    def test_patch(self):
        pass

    def test_delete(self):
        pass

class TestItemCollection(unittest.TestCase):
    def test_get(self):
        pass

    def test_post(self):
        pass

class TestItem(unittest.TestCase):
    def test_get(self):
        pass

    def test_patch(self):
        pass

    def test_delete(self):
        pass
