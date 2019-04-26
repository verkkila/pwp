
from flask import Blueprint, redirect, request, url_for
from flask_restful import Api

STATIC_PATH = 'static/'

api_bp = Blueprint('diary',  __name__, static_folder=STATIC_PATH)

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
    return redirect(url_for(".schedules"))

@api_bp.route('/schedules/')
def schedules():
    return api_bp.send_static_file('html/schedules.html')

@api_bp.route('/tasks/')
def tasks():
    if request.args.get("schedule_id", None) is None:
        return "Schedule id not specified", 400
    print(request.args["schedule_id"])
    return api_bp.send_static_file('html/tasks.html')

@api_bp.route('/items/')
def items():
    if request.args.get("schedule_id", None) is None:
        return "Schedule id not specified", 400
    return api_bp.send_static_file('html/items.html')

@api_bp.route('/events/')
def events():
    if request.args.get("schedule_id", None) is None:
        return "Schedule id not specified", 400
    return api_bp.send_static_file('html/events.html')
