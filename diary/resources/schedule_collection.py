import json
from datetime import datetime

from flask import Response, url_for, request
from flask_restful import Resource

from diary import db
from diary.models import Schedule
from diary.utils import MasonBuilder, DiaryBuilder, MIMETYPE, TIME_FORMAT


class ScheduleCollection(Resource):
    def get(self):

        body = DiaryBuilder()

        body.add_namespace()
        body.add_control('self', url_for('.schedulecollection'))
        body.add_control('profile','/profile/schedule/')
        body.add_control_add_schedule()

        query_results = Schedule.query.all()
        items = []
        for schedule_item in query_results:
            item_dict = MasonBuilder()
            item_dict['name'] = schedule_item.name
            item_dict['start_time'] = schedule_item.start_time.strftime(TIME_FORMAT)
            item_dict['end_time'] = schedule_item.end_time.strftime(TIME_FORMAT)
            item_dict.add_control('self', url_for('.schedule', schedule_id=schedule_item.id))
            items.append(item_dict)
        body['items'] = items
        return Response(json.dumps(body, indent=4), status=200, mimetype=MIMETYPE)
    
    def post(self):
        if request.json is not None:
            try:
                name = request.json['name']
                start_time = datetime.strptime(request.json['start_time'], TIME_FORMAT)
                end_time = datetime.strptime(request.json['end_time'], TIME_FORMAT)
            except KeyError:
                return DiaryBuilder.create_error_response(400, 'Invalid JSON payload')
            except ValueError:
                return DiaryBuilder.create_error_response(400, 'Invalid time format in payload')
        else:
            return DiaryBuilder.create_error_response(415, 'Json payload please')
        schedule  = Schedule(
            name=name,
            start_time=start_time,
            end_time=end_time,
        )
        db.session.add(schedule)            
        db.session.commit()
        DiaryBuilder.create_error_response(409, 'Schedule already exists')
        return Response(status=201)

