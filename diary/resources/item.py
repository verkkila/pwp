import json
from datetime import datetime

from flask import Response, url_for, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from diary import db
from diary.models import ScheduleItem, Item
from diary.utils import MasonBuilder, DiaryBuilder, MIMETYPE, TIME_FORMAT


class ItemResource(Resource):
    
    def get(self, schedule_id, item_id):
        query = Item.query.filter_by(id=item_id).first()
        if query is None:
            return DiaryBuilder.create_error_response(404, 'Item does not exist')
        body = DiaryBuilder()
        body['name'] = query.name
        body['value'] = query.value
        body.add_namespace()
        body.add_control('self',url_for('.itemresource',schedule_id=schedule_id,item_id=item_id))
        body.add_control('collection', url_for('.itemcollection',schedule_id=schedule_id))
        body.add_control('profile', '/profiles/item/')
        body.add_control_edit_item(schedule_id,item_id)
        body.add_control_add_item(schedule_id)
        body.add_control_delete_item(schedule_id, item_id)
        return Response(json.dumps(body, indent=4), status=200, mimetype=MIMETYPE)


    def patch(self, schedule_id,item_id):
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
        
        query = Item.query.filter_by(id=item_id).first()
        if query is None:
            return DiaryBuilder.create_error_response(404, 'Item does not exist')
        query.name = name
        query.value = value
        try:
            db.session.add(query)
            db.session.commit()
        except IntegrityError:
            return DiaryBuilder.create_error_response(409, 'Item already exists')
        else:
            Response(status=204)

    def delete(self, schedule_id, event_id):
        query = Item.query.filter_by(id=item_id).first()
        if query is None:
            return DiaryBuilder.create_error_response(404, 'Item does not exist')
        db.session.delete(query)
        db.session.commit()
        return Response(status=204)

