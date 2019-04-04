from flask_restful import Resource

class Task(Resource):
    
    def get(self):
        raise NotImplementedError
    
    def patch(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

