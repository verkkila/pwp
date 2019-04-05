from flask_restful import Resource

class TaskResource(Resource):
    
    def get(self):
        raise NotImplementedError
    
    def patch(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

