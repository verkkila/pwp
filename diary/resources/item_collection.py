import json
from datetime import datetime

from flask import Response, url_for, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from diary import db
from diary.models import ScheduleItem, Item
from diary.utils import MasonBuilder, DiaryBuilder, MIMETYPE, TIME_FORMAT

class ItemCollection(Resource):
    def get(self, schedule_id):
        query = ScheduleItem.query.filter_by(schedule_id=schedule_id).first()
        if query is None:
            return DiaryBuilder.create_error_response(404, 'Schedule does not exist')
        body = DiaryBuilder()
        body.add_namespace()
        body.add_control('self', url_for('.itemcollection', schedule_id=schedule_id))
        body.add_control('collection', url_for('.scheduleresource',schedule_id=schedule_id))
        body.add_control('profile','/profiles/item/')
        body.add_control_add_item(schedule_id)
        body.add_control_events_in(schedule_id)
        body.add_control_tasks_in(schedule_id)
        item_list = Item.query.all()
        items = []
        for item in item_list:
            item_dict = MasonBuilder( 
                name=item.name,
                value=item.value,
                )
            item_dict.add_control(
                'self',url_for('.itemresource',schedule_id=schedule_id,item_id=item.id))
            item_dict.add_control('profile','/profiles/item/')
            items.append(item_dict)
        body['items'] = items
        return Response(json.dumps(body, indent=4),status=200, mimetype=MIMETYPE)
    
    def post(self,schedule_id):
        if request.json is not None:
            try:
                name = request.json['name']
                value = float(request.json['duration'])
            except KeyError:
                return DiaryBuilder.create_error_response(400, 'Invalid json payload')
            except ValueError:
                return DiaryBuilder.create_error_response(400, 'Value must be number')
        else:
            return DiaryBuilder.create_error_response(415, 'please json')
        
        item = Item(
            name=name,
            value=value
        )
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            return DiaryBuilder.create_error_response(409, 'Item already exists')
        else:
            return Response(201)

