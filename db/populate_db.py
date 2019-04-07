from datetime import datetime
import sys
sys.path.append("../")
from sqlalchemy.engine import Engine
from sqlalchemy import event

from diary import create_app, db
import diary.models as models
#from diary.models import Schedule, ScheduleEvent, ScheduleTask, ScheduleItem, Event, Task, Item

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class Populator:
    class Schedule:
        def __init__(self, name, start_time, end_time):
            self.events = []
            self.tasks = []
            self.items = []
            self.name = name
            self.start_time = start_time
            self.end_time = end_time

        def add_event(self, event):
            self.events.append(event)

        def add_task(self, task):
            self.tasks.append(task)

        def add_item(self, item):
            self.items.append(item)

    class Event:
        def __init__(self, name, duration, note):
            self.name = name
            self.duration = duration
            self.note = note

    class Task:
        def __init__(self, name, priority, goal, result):
            self.name = name
            self.priority = priority
            self.goal = goal
            self.result = result

    class Item:
        def __init__(self, name, value):
            self.name = name
            self.value = value

    def __init__(self):
        self.schedules = []
        self.events = []
        self.tasks = []
        self.items = []
        self.models = []

    def add_schedule(self, schedule):
        self.schedules.append(schedule)
    
    def add_event(self, event):
        self.events.append(event)

    def add_task(self, task):
        self.tasks.append(task)

    def add_item(self, item):
        self.items.append(item)

    def create_all(self):
        for s in self.schedules:
            S = models.Schedule(name=s.name, start_time=s.start_time, end_time=s.end_time)
            db.session.add(S)
            for e in s.events:
                E = models.Event(name=e.name, duration=e.duration, note=e.note)
                SE = models.ScheduleEvent(schedule=S, event=E)
                db.session.add(E)
                db.session.add(SE)

            for t in s.tasks:
                T = models.Task(name=e.name, priority=t.priority, goal=t.goal, result=t.result)
                ST = models.ScheduleTask(schedule=S, task=T)
                db.session.add(T)
                db.session.add(ST)

            for i in s.items:
                I = models.Item(name=i.name, value=i.value)
                SI = models.ScheduleItem(schedule=S, item=I)
                db.session.add(I)
                db.session.add(SI)

        db.session.commit()

if __name__ == "__main__":
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///../db/test.db",
        "TESTING": True
    }
    app = create_app(config)
    db.create_all()
    populator = Populator()
    s = Populator.Schedule("testSchedule", 
            datetime.strptime("2019-05-04 08:00:00", "%y-%m-%d %H:%M:%S"),
            datetime.strptime("2019-05-04 16:00:00", "%y-%m-%d %H:%M:%S"))
    s.add_event(Populator.Event("testEvent", 4, "testNote"))
    s.add_task(Populator.Task("testTask", 100, "testGoal", "testResult"))
    s.add_item(Populator.Item("testItem", 50.0))
    populator.add_schedule(s)
    populator.create_all()
