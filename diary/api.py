
from flask import Blueprint, redirect
from flask_restful import Api


api_bp = Blueprint('diary', __name__)

api = Api(api_bp)


from diary.resources.schedule_collection import ScheduleCollection
from diary.resources.schedule import Schedule
from diary.resources.event_collection import EventCollection
from diary.resources.event import Event
from diary.resources.item_collection import ItemCollection
from diary.resources.item import Item
from diary.resources.task_collection import TaskCollection
from diary.resources.task import Task


@api_bp.route('/')
def index():
    return 'Hello world', 200

