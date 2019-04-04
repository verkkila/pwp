
from flask import Blueprint, redirect
from flask_restful import Api


api_bp = Blueprint('diary', __name__)

api = Api(api_bp)

from diary.utils import (
    SCHEDULE_COLLECTION_URI,
    SCHEDULE_URI,
    ITEM_COLLETION_URI,
    ITEM_URI,
    EVENT_COLLECTION_URI,
    EVENT_URI,
    TASK_COLLECTION_URI,
    TASK_URI
    )

from diary.resources.schedule_collection import ScheduleCollection
from diary.resources.schedule import Schedule
from diary.resources.item_collection import ItemCollection
from diary.resources.item import Item
from diary.resources.event_collection import EventCollection
from diary.resources.event import Event
from diary.resources.task_collection import TaskCollection
from diary.resources.task import Task

api.add_resource(ScheduleCollection,SCHEDULE_COLLECTION_URI)
api.add_resource(Schedule,SCHEDULE_URI)
api.add_resource(ItemCollection, ITEM_COLLETION_URI)
api.add_resource(Item, ITEM_URI)
api.add_resource(EventCollection, EVENT_COLLECTION_URI)
api.add_resource(Event, EVENT_URI)
api.add_resource(TaskCollection, TASK_COLLECTION_URI)
api.add_resource(Task, TASK_URI)


@api_bp.route('/')
def index():
    return 'Hello world', 200

