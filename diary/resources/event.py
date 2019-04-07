import json
from datetime import datetime

from flask import Response, url_for, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from diary import db
from diary.models import Event
from diary.utils import MasonBuilder, DiaryBuilder, MIMETYPE, TIME_FORMAT

class EventResource(Resource):
    
    def get(self,schedule_id, event_id):
        event_item = Event.query.filter_by(id=event_id).first()
        if event_item is None:
            return DiaryBuilder.create_error_response(404, 'Event does not exist')
        body = DiaryBuilder()
        body['name'] = event_item.name
        body['note'] = event_item.note
        body['duration'] = event_item.duration
        body.add_namespace()
        body.add_control('profile', '/profiles/event/')
        body.add_control('collection', url_for('.eventcollection', schedule_id=schedule_id))
        body.add_control_add_event(schedule_id)
        body.add_control_edit_event(schedule_id,event_id)
        body.add_control_delete_event(schedule_id, event_id)
        return Response(json.dumps(body, indent=4), mimetype=MIMETYPE)

    def patch(self,schedule_id, event_id):
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
        
        event_item = Event.query.filter_by(id=event_id).first()
        if event_item is None:
            return DiaryBuilder.create_error_response(404, 'Event does not exist')
        event_item.name = name
        event_item.duration = duration
        event_item.note = note
        try:
            db.session.commit()
        except IntegrityError:
            return DiaryBuilder.create_error_response(409, 'Event already exists')
        else:
            return Response(status=204)

    def delete(self, event_id):
        event_item = Event.query.filter_by(id=event_id).first()
        if event_item is None:
            return DiaryBuilder.create_error_response(404, 'Event does not exist')
        db.session.delete(event_item)
        db.session.commit()
        return Response(status=204)
