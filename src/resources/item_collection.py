from flask_restful import Resource

class ItemCollection(Resource):
    def get(self):
        raise NotImplementedError
    
    def post(self):
        raise NotImplementedError
