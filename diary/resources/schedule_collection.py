from flask import Response, url_for
from flask_restful import Resource

from diary.models import Schedule
from diary.utils import MasonBuilder, DiaryBuilder, MIMETYPE, SCHEDULE_COLLECTION_URI


class ScheduleCollection(Resource):
    def get(self):

        body = DiaryBuilder()

        body.add_namespace()
        body.add_control('self', SCHEDULE_COLLECTION_URI)
        body.add_control('profile','/profile/schedule/')
        body.add_control_add_schedule()

        query_results = Schedule.query.all()
        items = []
        for schedule_item in query_results:
            item_dict = MasonBuilder()
            item_dict['id'] = schedule_item.id
            # name = schedule_item.name # TODO: Name is still in models but not in api bp
            item_dict['start_time'] = schedule_item.start_time
            item_dict['end_time'] = schedule_item.end_time
            item_dict.add_control('self', url_for('.Schedule', schedule_item.id))
            items.append(item_dict)
        body['items'] = items
        return Response(json.dump(body), status=200, mimetype=MIMETYPE)
    def post(self):
        raise NotImplementedError