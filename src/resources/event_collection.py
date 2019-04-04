from flask_restful import Resource

class EventCollection(Resource):
    def get(self):
        raise NotImplementedError
    
    def post(self):
        raise NotImplementedError
        