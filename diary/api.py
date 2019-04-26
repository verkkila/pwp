
from flask import Blueprint, redirect
from flask_restful import Api

STATIC_PATH = '../static/'

api_bp = Blueprint('diary', __name__,static_folder=STATIC_PATH)

api = Api(api_bp)

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

from diary.resources.schedule_collection import ScheduleCollection
from diary.resources.schedule import ScheduleResource
from diary.resources.item_collection import ItemCollection
from diary.resources.item import ItemResource
from diary.resources.event_collection import EventCollection
from diary.resources.event import EventResource
from diary.resources.task_collection import TaskCollection
from diary.resources.task import TaskResource

api.add_resource(ScheduleCollection,SCHEDULE_COLLECTION_URI)
api.add_resource(ScheduleResource,SCHEDULE_URI)
api.add_resource(ItemCollection, ITEM_COLLECTION_URI)
api.add_resource(ItemResource, ITEM_URI)
api.add_resource(EventCollection, EVENT_COLLECTION_URI)
api.add_resource(EventResource, EVENT_URI)
api.add_resource(TaskCollection, TASK_COLLECTION_URI)
api.add_resource(TaskResource, TASK_URI)

@api_bp.route('/')
def index():
    return 'Hello world', 200

@api_bp.route('/schedules/')
def schedules():
    return api_bp.send_from_static('html/schedules.html')

@api_bp.route('/tasks?schedule_id/')
def schedules():
    return api_bp.send_from_static('html/tasks.html')

@api_bp.route('/items?schedule_id/')
def schedules():
    return api_bp.send_from_static('html/items.html')

@api_bp.route('/events?schedule_id/')
def schedules():
    return api_bp.send_from_static('html/events.html')
