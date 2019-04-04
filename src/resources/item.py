from flask_restful import Resource

class Item(Resource):
    
    def get(self):
        raise NotImplementedError
    
    def patch(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

