import json
from datetime import datetime

from flask import Response, url_for, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from diary import db
from diary.models import ScheduleEvent, Event
from diary.utils import MasonBuilder, DiaryBuilder, MIMETYPE, TIME_FORMAT

class EventCollection(Resource):
    def get(self, schedule_id):
        query = ScheduleEvent.query.filter_by(schedule_id=schedule_id).all()
        if len(query)==0:
            return DiaryBuilder.create_error_response(404, 'Schedule does not exist or has no events')
        body = DiaryBuilder()
        body.add_namespace()
        body.add_control('self', url_for('.eventcollection', schedule_id=schedule_id))
        body.add_control('collection', url_for('.scheduleresource',schedule_id=schedule_id))
        body.add_control('profile','/profiles/event/')
        body.add_control_add_event(schedule_id)
        body.add_control_items_in(schedule_id)
        body.add_control_tasks_in(schedule_id)
        body.add_control_all_schedules()
        items = []
        for event_item in query:
            event_item = event_item.event
            item_dict = MasonBuilder(
                name=event_item.name,
                duration=event_item.duration,
                note=event_item.note,
                id=event_item.id
                )
            item_dict.add_control(
                'self',url_for('.eventresource',schedule_id=schedule_id,event_id=event_item.id))
            item_dict.add_control('profile','/profiles/event/')
            items.append(item_dict)
        body['items'] = items
        return Response(json.dumps(body, indent=4),status=200, mimetype=MIMETYPE)
    
    def post(self, schedule_id):
        if request.json is not None:
            try:
                name = request.json['name']
                duration = int(request.json['duration'])
                note = request.json.get('note',None)
            except KeyError:
                return DiaryBuilder.create_error_response(400, 'Missing keys in payload')
            except ValueError:
                return DiaryBuilder.create_error_response(400, 'Duration must be integer')
        else:
            return DiaryBuilder.create_error_response(415, 'please json')
        
        event = Event(
            name=name,
            duration=duration,
            note=note
        )
        s_event= ScheduleEvent(
            schedule_id=schedule_id,
            event=event
        )
        try:
            db.session.add(s_event)
            db.session.commit()
        except IntegrityError:
            return DiaryBuilder.create_error_response(409, 'Event already exists')
        else:
            return Response(status=201)
