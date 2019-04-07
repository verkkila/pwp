import unittest
import pytest
import sys
sys.path.append("../")

from diary import create_app, db
from diary.utils import (
    SCHEDULE_COLLECTION_URI,
    SCHEDULE_URI,
    ITEM_COLLECTION_URI,
    ITEM_URI,
    EVENT_COLLECTION_URI,
    EVENT_URI,
    TASK_COLLECTION_URI,
    TASK_URI
    )

@pytest.fixture
def app():
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///../db/test.db",
        "TESTING": True
    }

    app = create_app(config)

    with app.app_context():
        db.create_all()

    yield app

def test_schedule_collection_get(app):
    resp = app.test_client().get(SCHEDULE_COLLECTION_URI)
    assert resp.status_code == 200
    assert resp.json["@namespaces"]["diary"]["name"] == "/diary/link-relations/"
    assert resp.json["@controls"]["self"]["href"] == SCHEDULE_COLLECTION_URI
    assert resp.json["@controls"]["profile"]["href"] == "/profile/schedule/"
    assert resp.json["@controls"]["diary:add-schedule"]["method"] == "POST"
    assert resp.json["@controls"]["diary:add-schedule"]["encoding"] == "json"
    assert resp.json["@controls"]["diary:add-schedule"]["schema"]["type"] == "object"
    assert resp.json["@controls"]["diary:add-schedule"]["schema"]["properties"]["start_time"]
    assert resp.json["@controls"]["diary:add-schedule"]["schema"]["properties"]["end_time"]

def test_schedule_collection_post(app):
    resp = app.test_client().post(SCHEDULE_COLLECTION_URI, json={"name": "testSchedule1", "start_time": "2014-03-04 08:00:00", "end_time": "2014-04-05 16:00:00"})
    assert resp.status_code == 201
    resp2 = app.test_client().post(SCHEDULE_COLLECTION_URI, json={"name": "testSchedule2", "start_time": "2014-03-04 08:00:00"})
    assert resp2.status_code == 400
    resp3 = app.test_client().post(SCHEDULE_COLLECTION_URI, json={"name": "testSchedule2", "start_time": "2014-03-04 08:00:00", "end_time": "2014-04-05 16:00:00"})
    assert resp3.status_code == 409

def test_schedule_get(app):
    pass

def test_schedule_put(app):
    pass

def test_schedule_delete(app):
    pass

def test_event_collection_get(app):
    pass

def test_event_collection_post(app):
    pass

def test_event_get(app):
    pass

def test_event_patch(app):
    pass

def test_event_delete(app):
    pass

def test_task_collection_get(app):
    pass

def test_task_collectionpost(app):
    pass

def test_task_get(app):
    pass

def test_task_patch(app):
    pass

def test_task_delete(app):
    pass

def test_item_collection_get(app):
    pass

def test_item_collection_post(app):
    pass

def test_item_get(app):
    pass

def test_item_patch(app):
    pass

def test_item_delete(app):
    pass
