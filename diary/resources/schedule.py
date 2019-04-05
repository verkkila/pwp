import json
from datetime import datetime

from flask import Response, url_for, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from diary import db
from diary.models import Schedule
from diary.utils import MasonBuilder, DiaryBuilder, MIMETYPE, TIME_FORMAT


class ScheduleResource(Resource):
    def get(self, schedule_id):
        schedule_item = Schedule.query.filter_by(id=schedule_id).first()
        if schedule_item is None:
            return DiaryBuilder.create_error_response(404, 'Schedule not found')
        body = DiaryBuilder()
        body['start_time'] = schedule_item.start_time.strftime(TIME_FORMAT)
        body['end_time'] = schedule_item.end_time.strftime(TIME_FORMAT)
        body['name'] = schedule_item.name
        body.add_control('self',url_for('.scheduleresource',schedule_id=schedule_id))
        body.add_control('collection', url_for('.schedulecollection'))
        body.add_control('profile', '/profiles/schedule/')
        body.add_control_edit_schedule(schedule_id)
        body.add_control_delete_schedule(schedule_id)
        items_dict = DiaryBuilder()
        items_dict.add_control('item', url_for('.itemcollection', schedule_id=schedule_id))
        items_dict.add_control('task', url_for('.taskcollection', schedule_id=schedule_id))
        items_dict.add_control('event', url_for('.eventcollection', schedule_id=schedule_id))
        body['items'] = [items_dict]
        return Response(json.dumps(body, indent=4), status=200, mimetype=MIMETYPE)



    def put(self, schedule_id):
        if request.json is not None:
            try:
                name = request.json.get('name', None)
                start_time = datetime.strptime(request.json['start_time'], TIME_FORMAT)
                end_time = datetime.strptime(request.json['end_time'], TIME_FORMAT)
            except KeyError:
                return DiaryBuilder.create_error_response(400, 'Invalid JSON payload')
            except ValueError:
                return DiaryBuilder.create_error_response(400, 'Invalid time format in payload')
        else:
            DiaryBuilder.create_error_response(415, 'Json payload please')
        query = Shedule.query.filter_by(id=schedule_id).first()
        if query is None:
            return DiaryBuilder.create_error_response(404, 'Schedule does not exit')
        query.name = name
        query.start_time = start_time
        query.end_time = end_time
        try:
            db.session.commit()
        except IntegrityError:
            return DiaryBuilder.create_error_response(409, 'Schedule already exists')
        else:
            return Response(status=204)
        

    def delete(self, schedule_id):
        query = Schedule.query.filter_by(id=schedule_id).first()
        if query is None:
            return DiaryBuilder.create_error_response(404, 'Schedule does not exist')
        db.session.delete(query)
        db.commit()
        return Response(status=204)
        


    