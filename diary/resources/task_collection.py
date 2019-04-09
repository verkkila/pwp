import json
from datetime import datetime

from flask import Response, url_for, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from diary import db
from diary.models import ScheduleTask, Task
from diary.utils import MasonBuilder, DiaryBuilder, MIMETYPE, TIME_FORMAT

class TaskCollection(Resource):
    def get(self, schedule_id):
        query = ScheduleTask.query.filter_by(schedule_id=schedule_id).all()
        if len(query) == 0:
            return DiaryBuilder.create_error_response(404, 'Schedule does not exist or has no tasks')
        body = DiaryBuilder()
        body.add_namespace()
        body.add_control('self', url_for('.taskcollection', schedule_id=schedule_id))
        body.add_control('collection', url_for('.scheduleresource',schedule_id=schedule_id))
        body.add_control('profile','/profiles/task/')
        body.add_control_add_task(schedule_id)
        body.add_control_items_in(schedule_id)
        body.add_control_events_in(schedule_id)
        body.add_control_all_schedules()
        items = []
        for task_item in query:
            task_item = task_item.task
            item_dict = MasonBuilder( 
                name=task_item.name,
                priority=task_item.priority,
                goal=task_item.goal,
                result=task_item.result
                )
            item_dict.add_control(
                'self',url_for('.taskresource',schedule_id=schedule_id,task_id=task_item.id))
            item_dict.add_control('profile','/profiles/task/')
            items.append(item_dict)
        body['items'] = items
        return Response(json.dumps(body, indent=4),status=200, mimetype=MIMETYPE)
    
    def post(self, schedule_id):
        if request.json is not None:
            try:
                name = request.json['name']
                priority = int(request.json['priority'])
                goal = request.json.get('goal',None)
                result = request.json.get('result',None)
            except KeyError:
                return DiaryBuilder.create_error_response(400, 'Missing keys in payload')
            except ValueError:
                return DiaryBuilder.create_error_response(400, 'Duration must be integer')
        else:
            return DiaryBuilder.create_error_response(415, 'please json')
        
        task = Task(
            name=name,
            priority=priority,
            goal=goal,
            result=result
        )
        try:
            db.session.add(task)
            db.session.commit()
        except IntegrityError:
            return DiaryBuilder.create_error_response(409, 'Task already exists')
        else:
            return Response(201)
