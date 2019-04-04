

from flask_restful import Resource

from diary.utils import DiaryBuilder 


class Schedule(Resource):
    def get(self):
        raise NotImplementedError

    def put(self):
        raise NotImplementedError
    
    def delete(self):
        raise NotImplementedError


    