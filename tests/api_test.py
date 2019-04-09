import unittest
import pytest
import json
import re
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
    TASK_URI,
    REGEX_PATTERN
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
    assert resp.json["@controls"]["profile"]["href"] == "/profiles/schedule/"
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
    resp3 = app.test_client().post(SCHEDULE_COLLECTION_URI, json={"name": "testSchedule1", "start_time": "2014-03-04 08:00:00", "end_time": "2014-04-05 16:00:00"})
    assert resp3.status_code == 409

def test_schedule_get(app):
    resp = app.test_client().get(SCHEDULE_COLLECTION_URI + "1/")
    assert resp.status_code == 200
    resp2 = app.test_client().get(SCHEDULE_COLLECTION_URI + "10/")
    assert resp2.status_code == 404

def test_schedule_put(app):
    resp = app.test_client().put(SCHEDULE_COLLECTION_URI + "1/", data = json.dumps({"name": "testSchedule", "start_time": "2014-03-04 09:00:00", "end_time": "2014-04-05 15:00:00"}))
    assert resp == 204
    resp2 = app.test_client().put(SCHEDULE_COLLECTION_URI + "10/", data = json.dumps({"name": "testSchedule", "start_time": "2014-03-04 09:00:00", "end_time": "2014-04-05 15:00:00"}))
    assert resp2 == 404
    resp3 = app.test_client().put(SCHEDULE_COLLECTION_URI + "10/", data = "not json")
    assert resp3 == 409

def test_schedule_delete(app):
    resp = app.test_client().delete(SCHEDULE_COLLECTION_URI + "1/")
    assert resp.status_code == 204
    resp2 = app.test_client().delete(SCHEDULE_COLLECTION_URI + "10/")
    assert resp2.status_code == 404

def test_event_collection_get(app):
    event_collection_uri = re.sub(REGEX_PATTERN, "{}", EVENT_COLLECTION_URI).format(1, 1)
    resp = app.test_client().get(event_collection_uri)
    assert resp.status_code == 200
    assert resp.json["@namespaces"]["diary"]["name"] == "/diary/link-relations/"
    assert resp.json["@controls"]["self"]["href"] == event_collection_uri
    assert resp.json["@controls"]["profile"]["href"] == "/profiles/event/"
    assert resp.json["@controls"]["collection"]["href"] == re.sub(REGEX_PATTERN, "{}", SCHEDULE_URI).format(1)
    assert resp.json["@controls"]["diary:add-event"]["method"] == "POST"
    assert resp.json["@controls"]["diary:add-event"]["encoding"] == "json"
    assert resp.json["@controls"]["diary:add-event"]["href"] == re.sub(REGEX_PATTERN, "{}", EVENT_URI).format(1, 1)
    assert resp.json["@controls"]["diary:add-event"]["schema"]["type"] == "object"
    assert resp.json["@controls"]["diary:add-event"]["schema"]["properties"]["name"]["type"] == "string"
    assert resp.json["@controls"]["diary:add-event"]["schema"]["properties"]["duration"]["type"] == "integer"
    assert resp.json["@controls"]["diary:add-event"]["schema"]["properties"]["note"]["type"] == "string"
    assert resp.json["@controls"]["diary:items-in"]["href"] == re.sub(REGEX_PATTERN, "{}", ITEM_COLLECTION_URI).format(1)
    assert resp.json["@controls"]["diary:tasks-in"] == re.sub(REGEX_PATTERN, "{}", TASK_COLLECTION_URI).format(1)
    assert resp.json["@controls"]["diary:all-schedules"] == SCHEDULE_COLLECTION_URI

def test_event_collection_post(app):
    resp = app.test_client().post(EVENT_COLLECTION_URI, data = json.dumps({"name": "testEvent", "duration": 4, "note": "testNote"}))
    assert resp.status_code == 201
    resp2 = app.test_client().post(EVENT_COLLECTION_URI, data = json.dumps({"name": "testEvent", "duration": 4, "note": "testNote"}))
    assert resp2.status_code == 409
    resp3 = app.test_client().post(EVENT_COLLECTION_URI, data = "not json")
    assert resp3.status_code == 400

def test_event_get(app):
    event_uri = re.sub(REGEX_PATTERN, "{}", EVENT_URI).format(1, 1)
    resp = app.test_client().get(event_uri)
    assert resp.status_code == 200
    assert resp.json["@namespaces"]["diary"]["name"] == "/diary/link-relations/"
    assert resp.json["name"] == "testEvent"
    assert resp.json["duration"] == 4
    assert resp.json["note"] == "testNote"
    assert resp.json["@controls"]["self"]["href"] == event_uri
    assert resp.json["@controls"]["profile"]["href"] == "/profiles/event/"
    assert resp.json["@controls"]["collection"]["href"] == re.sub(REGEX_PATTERN, "{}", EVENT_COLLECTION_URI).format(1)
    assert resp.json["@controls"]["edit"]["href"] == event_uri
    assert resp.json["@controls"]["edit"]["title"] == "Edit"
    assert resp.json["@controls"]["edit"]["encoding"] == "json"
    assert resp.json["@controls"]["edit"]["method"] == "PUT"
    assert resp.json["@controls"]["diary:delete"]["href"] == event_uri
    assert resp.json["@controls"]["diary:delete"]["method"] == "DELETE"

    resp2 = app.test_client().get(re.sub(REGEX_PATTERN, "{}", EVENT_URI).format(10, 10))
    assert resp2.status_code == 404

def test_event_patch(app):
    resp = app.test_client().patch(re.sub(REGEX_PATTERN, "{}", EVENT_URI).format(1, 1), data = json.dumps({"name": "testEvent", "duration": 6, "note": "new note"}))
    assert resp.status_code == 204
    resp2 = app.test_client().patch(re.sub(REGEX_PATTERN, "{}", EVENT_URI).format(1, 1), data = "not json")
    assert resp2.status_code == 400

def test_event_delete(app):
    resp = app.test_client().delete(re.sub(REGEX_PATTERN, "{}", EVENT_URI).format(1, 1))
    assert resp.status_code == 204
    resp2 = app.test_client().delete(re.sub(REGEX_PATTERN, "{}", EVENT_URI).format(10, 10))
    assert resp2.status_code == 404

def test_task_collection_get(app):
    task_collection_uri = re.sub(REGEX_PATTERN, "{}", TASK_COLLECTION_URI).format(1, 1)
    resp = app.test_client().get(task_collection_uri)
    assert resp.status_code == 200
    assert resp.json["@namespaces"]["diary"]["name"] == "/diary/link-relations/"
    assert resp.json["@controls"]["self"]["href"] == task_collection_uri
    assert resp.json["@controls"]["profile"]["href"] == "/profiles/task/"
    assert resp.json["@controls"]["collection"]["href"] == re.sub(REGEX_PATTERN, "{}", SCHEDULE_URI).format(1)
    assert resp.json["@controls"]["diary:add-task"]["method"] == "POST"
    assert resp.json["@controls"]["diary:add-task"]["encoding"] == "json"
    assert resp.json["@controls"]["diary:add-task"]["href"] == re.sub(REGEX_PATTERN, "{}", EVENT_URI).format(1, 1)
    assert resp.json["@controls"]["diary:add-task"]["schema"]["type"] == "object"
    assert resp.json["@controls"]["diary:add-task"]["schema"]["properties"]["name"]["type"] == "string"
    assert resp.json["@controls"]["diary:add-task"]["schema"]["properties"]["priority"]["type"] == "int"
    assert resp.json["@controls"]["diary:add-task"]["schema"]["properties"]["goal"]["type"] == "string"
    assert resp.json["@controls"]["diary:add-task"]["schema"]["properties"]["result"]["type"] == "string"
    assert resp.json["@controls"]["diary:items-in"]["href"] == re.sub(REGEX_PATTERN, "{}", ITEM_COLLECTION_URI).format(1)
    assert resp.json["@controls"]["diary:events-in"] == re.sub(REGEX_PATTERN, "{}", EVENT_COLLECTION_URI).format(1)
    assert resp.json["@controls"]["diary:all-schedules"] == SCHEDULE_COLLECTION_URI

def test_task_collection_post(app):
    resp = app.test_client().post(re.sub(REGEX_PATTERN, "{}", TASK_COLLECTION_URI).format(1), data = json.dumps({"name": "testTask", "priority": 10, "goal": "testGoal", "result": "testResult"}))
    assert resp.status_code == 201
    resp2 = app.test_client().post(re.sub(REGEX_PATTERN, "{}", TASK_COLLECTION_URI).format(1), data = json.dumps({"name": "testTask", "priority": 10, "goal": "testGoal", "result": "testResult"}))
    assert resp2.status_code == 409
    resp3 = app.test_client().post(re.sub(REGEX_PATTERN, "{}", TASK_COLLECTION_URI).format(1), data = "not json")
    assert resp3.status_code == 400

def test_task_get(app):
    task_uri = re.sub(REGEX_PATTERN, "{}", TASK_URI).format(1, 1)
    resp = app.test_client().get(task_uri)
    assert resp.status_code == 200
    assert resp.json["@namespaces"]["diary"]["name"] == "/diary/link-relations/"
    assert resp.json["name"] == "testTask"
    assert resp.json["priority"] == 100
    assert resp.json["goal"] == "testGoal"
    assert resp.json["result"] == "testResult"
    assert resp.json["@controls"]["self"]["href"] == task_uri
    assert resp.json["@controls"]["profile"]["href"] == "/profiles/task/"
    assert resp.json["@controls"]["collection"]["href"] == re.sub(REGEX_PATTERN, "{}", TASK_COLLECTION_URI).format(1)
    assert resp.json["@controls"]["edit"]["href"] == task_uri
    assert resp.json["@controls"]["edit"]["title"] == "Edit"
    assert resp.json["@controls"]["edit"]["encoding"] == "json"
    assert resp.json["@controls"]["edit"]["method"] == "PUT"
    assert resp.json["@controls"]["diary:delete"]["href"] == task_uri
    assert resp.json["@controls"]["diary:delete"]["method"] == "DELETE"
    resp2 = app.test_client().get(task_uri)
    assert resp2.status_code == 200

def test_task_patch(app):
    resp = app.test_client().patch(re.sub(REGEX_PATTERN, "{}", TASK_URI).format(1, 1), data = json.dumps({"name": "testEvent", "priority": 5, "goal": "new goal", "result": "new result"}))
    assert resp.status_code == 204
    resp2 = app.test_client().patch(re.sub(REGEX_PATTERN, "{}", TASK_URI).format(1, 1), data = "not json")
    assert resp2.status_code == 400

def test_task_delete(app):
    resp = app.test_client().delete(re.sub(REGEX_PATTERN, "{}", TASK_URI).format(1, 1))
    assert resp.status_code == 204
    resp2 = app.test_client().delete(re.sub(REGEX_PATTERN, "{}", TASK_URI).format(10, 10))
    assert resp2.status_code == 404

def test_item_collection_get(app):
    item_collection_uri = re.sub(REGEX_PATTERN, "{}", ITEM_COLLECTION_URI).format(1, 1)
    resp = app.test_client().get(item_collection_uri)
    assert resp.status_code == 200
    assert resp.json["@namespaces"]["diary"]["name"] == "/diary/link-relations/"
    assert resp.json["@controls"]["self"]["href"] == item_collection_uri
    assert resp.json["@controls"]["profile"]["href"] == "/profiles/item/"
    assert resp.json["@controls"]["collection"]["href"] == re.sub(REGEX_PATTERN, "{}", SCHEDULE_URI).format(1)
    assert resp.json["@controls"]["diary:add-item"]["method"] == "POST"
    assert resp.json["@controls"]["diary:add-item"]["encoding"] == "json"
    assert resp.json["@controls"]["diary:add-item"]["href"] == re.sub(REGEX_PATTERN, "{}", EVENT_URI).format(1, 1)
    assert resp.json["@controls"]["diary:add-item"]["schema"]["type"] == "object"
    assert resp.json["@controls"]["diary:add-item"]["schema"]["properties"]["name"]["type"] == "string"
    assert resp.json["@controls"]["diary:add-item"]["schema"]["properties"]["priority"]["type"] == "number"
    assert resp.json["@controls"]["diary:tasks-in"]["href"] == re.sub(REGEX_PATTERN, "{}", TASK_COLLECTION_URI).format(1)
    assert resp.json["@controls"]["diary:events-in"] == re.sub(REGEX_PATTERN, "{}", EVENT_COLLECTION_URI).format(1)
    assert resp.json["@controls"]["diary:all-schedules"] == SCHEDULE_COLLECTION_URI

def test_item_collection_post(app):
    resp = app.test_client().post(re.sub(REGEX_PATTERN, "{}", ITEM_COLLECTION_URI).format(1), data = json.dumps({"name": "testItem", "value": 10}))
    assert resp.status_code == 201
    resp2 = app.test_client().post(re.sub(REGEX_PATTERN, "{}", ITEM_COLLECTION_URI).format(1), data = json.dumps({"name": "testItem", "value": 10}))
    assert resp2.status_code == 409
    resp3 = app.test_client().post(re.sub(REGEX_PATTERN, "{}", ITEM_COLLECTION_URI).format(1), data = "not json")
    assert resp3.status_code == 400

def test_item_get(app):
    item_uri = re.sub(REGEX_PATTERN, "{}", ITEM_URI).format(1, 1)
    resp = app.test_client().get(item_uri)
    assert resp.status_code == 200
    assert resp.json["@namespaces"]["diary"]["name"] == "/diary/link-relations/"
    assert resp.json["name"] == "testItem"
    assert resp.json["value"] == 50.0
    assert resp.json["@controls"]["self"]["href"] == item_uri
    assert resp.json["@controls"]["profile"]["href"] == "/profiles/item/"
    assert resp.json["@controls"]["collection"]["href"] == re.sub(REGEX_PATTERN, "{}", ITEM_COLLECTION_URI).format(1)
    assert resp.json["@controls"]["edit"]["href"] == item_uri
    assert resp.json["@controls"]["edit"]["title"] == "Edit"
    assert resp.json["@controls"]["edit"]["encoding"] == "json"
    assert resp.json["@controls"]["edit"]["method"] == "PUT"
    assert resp.json["@controls"]["diary:delete"]["href"] == item_uri
    assert resp.json["@controls"]["diary:delete"]["method"] == "DELETE"
    resp2 = app.test_client().get(item_uri)
    assert resp2.status_code == 200

def test_item_patch(app):
    resp = app.test_client().patch(re.sub(REGEX_PATTERN, "{}", ITEM_URI).format(1, 1), data = json.dumps({"name": "testItem", "value": 5}))
    assert resp.status_code == 204
    resp2 = app.test_client().patch(re.sub(REGEX_PATTERN, "{}", ITEM_URI).format(1, 1), data = "not json")
    assert resp2.status_code == 400

def test_item_delete(app):
    resp = app.test_client().delete(re.sub(REGEX_PATTERN, "{}", ITEM_URI).format(1, 1))
    assert resp.status_code == 204
    resp2 = app.test_client().delete(re.sub(REGEX_PATTERN, "{}", ITEM_URI).format(10, 10))
    assert resp2.status_code == 404
