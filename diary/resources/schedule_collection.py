import re
import json

from flask import Response, url_for
from flask_restful import Resource

from diary.models import Schedule
from diary.utils import MasonBuilder, DiaryBuilder, MIMETYPE


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
            item_dict['start_time'] = schedule_item.start_time.strftime('%Y-%m-%d %H:%M:%S')
            item_dict['end_time'] = schedule_item.end_time.strftime('%Y-%m-%d %H:%M:%S')
            item_dict.add_control('self', url_for('.schedule', schedule_id=schedule_item.id))
            items.append(item_dict)
        body['items'] = items
        return Response(json.dumps(body), status=200, mimetype=MIMETYPE)
    
    def post(self):
        raise NotImplementedError
