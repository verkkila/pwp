from flask_restful import Resource

class ScheduleCollection(Resource):
    def get(self):
        raise NotImplementedError
    
    def post(self):
        raise NotImplementedError