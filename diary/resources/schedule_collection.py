from flask_restful import Resource

from diary.utils import DiaryBuilder 



class SchdeuleCollection(Resource):
    
    def get(self):
        raise NotImplementedError
    
    def post(self):
        raise NotImplementedError