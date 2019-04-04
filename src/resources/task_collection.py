from flask_restful import Resource

class TaskCollection(Resource):
    def get(self):
        raise NotImplementedError
    
    def post(self):
        raise NotImplementedError
