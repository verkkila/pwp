from flask_restful import Resource


class SchdeuleCollection(Resource):
    def get(self):
        raise NotImplementedError
    
    def post(self):
        raise NotImplementedError