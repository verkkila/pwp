import json
from datetime import datetime

from flask import Response, url_for, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from diary import db
from diary.models import ScheduleTask, Task
from diary.utils import MasonBuilder, DiaryBuilder, MIMETYPE, TIME_FORMAT

class TaskResource(Resource):
    
    def get(self, schedule_id, task_id):
        task_item = Task.query.filter_by(id=task_id).first()
        if task_item is None:
            return DiaryBuilder.create_error_response(404, 'Task does not exist')
        body = DiaryBuilder()
        body['name'] = task_item.name
        body['priority'] = task_item.priority
        body['goal'] = task_item.goal
        body['result'] = task_item.result
        body.add_namespace()
        body.add_control('profile', '/profiles/task/')
        body.add_control('collection', url_for('.taskcollection', schedule_id=schedule_id))
        body.add_control_add_task(schedule_id)
        body.add_control_edit_task(schedule_id,task_id)
        body.add_control_delete_task(schedule_id, task_id)
        return Response(json.dumps(body, indent=4), mimetype=MIMETYPE)

    def patch(self,schedule_id, task_id):
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
        
        task_item = Task.query.filter_by(id=task_id).first()
        if task_item is None:
            return DiaryBuilder.create_error_response(404, 'Task does not exist')
        task_item.name = name
        task_item.priority = priority
        task_item.goal = goal
        task_item.result = result
        try:
            db.session.commit()
        except IntegrityError:
            return DiaryBuilder.create_error_response(409, 'Task already exists')
        else:
            return Response(status=204)

    def delete(self, task_id):
        task_item = Task.query.filter_by(id=task_id).first()
        if task_item is None:
            return DiaryBuilder.create_error_response(404, 'Task does not exist')
        db.session.delete(task_item)
        db.session.commit()
        return Response(status=204)
