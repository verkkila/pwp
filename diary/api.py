
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
from diary.resources.schedule import ScheduleResource
from diary.resources.item_collection import ItemCollection
from diary.resources.item import ItemResource
from diary.resources.event_collection import EventCollection
from diary.resources.event import EventResource
from diary.resources.task_collection import TaskCollection
from diary.resources.task import TaskResource

api.add_resource(ScheduleCollection,SCHEDULE_COLLECTION_URI)
api.add_resource(ScheduleResource,SCHEDULE_URI)
api.add_resource(ItemCollection, ITEM_COLLETION_URI)
api.add_resource(ItemResource, ITEM_URI)
api.add_resource(EventCollection, EVENT_COLLECTION_URI)
api.add_resource(EventResource, EVENT_URI)
api.add_resource(TaskCollection, TASK_COLLECTION_URI)
api.add_resource(TaskResource, TASK_URI)

@api_bp.route('/')
def index():
    return 'Hello world', 200

