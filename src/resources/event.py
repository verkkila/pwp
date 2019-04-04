from flask_restful import Resource

class Event(Resource):
    
    def get(self):
        raise NotImplementedError
    
    def patch(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

