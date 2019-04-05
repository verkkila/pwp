from flask_restful import Resource

class ItemResource(Resource):
    
    def get(self):
        raise NotImplementedError
    
    def patch(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

