import os
import tempfile
from datetime import datetime, timedelta

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy import event

from app import app, db
from models import Schedule, RepeatSchedule, ScheduleEvent, ScheduleTask, ScheduleItem, Event, Task, Item


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture
def db_handle():
    db_fd, db_fname = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()

    yield db

    os.close(db_fd)
    os.unlink(db_fname)


def _get_event():
    return Event(
        name="Meeting",
        duration=2,
        note="Success"
    )

def _get_task():
    return Task(
        name="Study",
        priority=100,
        goal="chapters 5-6",
        result="mostly success"
    )


def _get_item():
    return Item(
        name="Banana",
        value=2.0,
    )

def _get_schedule():
    start = datetime.utcnow()
    end = start + timedelta(hours=1)
    return Schedule(
        name="Gym",
        start_time=start,
        end_time=end
    )

def _get_repeat_schedule():
    return RepeatSchedule(
        interval_days=20,
        count=15
    )


def test_add_event_schedule(db_handle):
    '''
    Tests that creating the relationship table between events and schedules work
    '''
    event = _get_event()
    schedule = _get_schedule()

    schedule_event = ScheduleEvent(
        schedule=schedule,
        event=event
    )
    db_handle.session.add(schedule_event)
    db_handle.session.commit()
    assert Schedule.query.count() == 1
    assert Event.query.count() == 1
    assert ScheduleEvent.query.count() == 1

def test_add_task_schedule(db_handle):
    '''
    Tests that creating the relationship table between tasks and schedules work
    '''
    task = _get_task()
    schedule = _get_schedule()

    schedule_task = ScheduleTask(
        schedule=schedule,
        task=task
    )
    db_handle.session.add(schedule_task)
    db_handle.session.commit()
    assert Schedule.query.count() == 1
    assert Task.query.count() == 1
    assert ScheduleTask.query.count() == 1

def test_add_item_schedule(db_handle):
    '''
    Tests that creating the relationship table between items and schedules work
    '''
    item = _get_item()
    schedule = _get_schedule()

    schedule_item = ScheduleItem(
        schedule=schedule,
        item=item
    )

    db_handle.session.add(schedule_item)
    db_handle.session.commit()

    assert Schedule.query.count() == 1
    assert Item.query.count() == 1
    assert ScheduleItem.query.count() == 1

def test_add_repeat_schedule(db_handle):
    '''
    Tests that creating a repeating schedule works
    '''
    repeat_schedule = _get_repeat_schedule()
    db_handle.session.add(repeat_schedule)
    db_handle.session.commit()

    assert RepeatSchedule.query.count() == 1

def test_query_event(db_handle):
    '''
    Tests the success and failure of querying events by their name, duration and note
    '''
    event = _get_event()
    db_handle.session.add(event)
    db_handle.session.commit()

    assert len(Event.query.filter_by(name="Meeting").all()) == 1
    assert len(Event.query.filter_by(duration=2).all()) == 1
    assert len(Event.query.filter_by(note="Success").all()) == 1

    assert len(Event.query.filter_by(name="Not a meeting").all()) == 0
    assert len(Event.query.filter_by(duration=4).all()) == 0
    assert len(Event.query.filter_by(note="Fail").all()) == 0

def test_query_task(db_handle):
    '''
    Tests the success and failure of querying tasks by their name, priority, goal and result
    '''
    task = _get_task()
    db_handle.session.add(task)
    db_handle.session.commit()

    assert len(Task.query.filter_by(name="Study").all()) == 1
    assert len(Task.query.filter_by(priority=100).all()) == 1
    assert len(Task.query.filter_by(goal="chapters 5-6").all()) == 1
    assert len(Task.query.filter_by(result="mostly success").all()) == 1

    assert len(Task.query.filter_by(name="").all()) == 0
    assert len(Task.query.filter_by(priority=0).all()) == 0
    assert len(Task.query.filter_by(goal="").all()) == 0
    assert len(Task.query.filter_by(result="").all()) == 0

def test_query_item(db_handle):
    '''
    Tests the success and failure of querying items by their names and values
    '''
    item = _get_item()
    db_handle.session.add(item)
    db_handle.session.commit()

    assert len(Item.query.filter_by(name="Banana").all()) == 1
    assert len(Item.query.filter_by(value=2.0).all()) == 1

    assert len(Item.query.filter_by(name="Apple").all()) == 0
    assert len(Item.query.filter_by(value=3.0).all()) == 0

def test_query_schedule_event(db_handle):
    '''
    Tests the success and failure of querying ScheduleEvents by their ids
    '''
    event = _get_event()
    schedule = _get_schedule()

    schedule_event = ScheduleEvent(
        schedule=schedule,
        event=event
    )
    db_handle.session.add(schedule_event)
    db_handle.session.commit()

    assert len(ScheduleEvent.query.filter_by(event_id=event.id).all()) == 1
    assert len(ScheduleEvent.query.filter_by(schedule_id=schedule.id).all()) == 1

    assert len(ScheduleEvent.query.filter_by(event_id=event.id+1).all()) == 0
    assert len(ScheduleEvent.query.filter_by(schedule_id=schedule.id+1).all()) == 0

def test_query_schedule_task(db_handle):
    '''
    Tests the success and failure of querying ScheduleTasks by their ids
    '''
    task = _get_task()
    schedule = _get_schedule()

    schedule_task = ScheduleTask(
        schedule=schedule,
        task=task
    )

def test_query_schedule_item(db_handle):
    '''
    Tests the success and failure of querying RoutineItems by their ids
    '''
    item = _get_item()
    schedule = _get_schedule()

    schedule_item = ScheduleItem(
        schedule=schedule,
        item=item
    )

    db_handle.session.add(schedule_item)
    db_handle.session.commit()

    assert len(ScheduleItem.query.filter_by(item_id=item.id).all()) == 1
    assert len(ScheduleItem.query.filter_by(schedule_id=schedule.id).all()) == 1

    assert len(ScheduleItem.query.filter_by(item_id=item.id+1).all()) == 0
    assert len(ScheduleItem.query.filter_by(schedule_id=schedule.id+1).all()) == 0

def test_query_schedule(db_handle):
    '''
    Tests the success and failure of querying routines by their names
    '''
    schedule = _get_schedule()
    db_handle.session.add(schedule)
    db_handle.session.commit()

    assert len(Schedule.query.filter_by(name="Gym").all()) == 1
    assert len(Schedule.query.filter_by(name="Jog").all()) == 0

def test_query_repeat_schedule(db_handle):
    '''
    Tests the success and failure of querying recurring routines by their intervals and counts
    '''
    repeat_schedule = _get_repeat_schedule()
    db_handle.session.add(repeat_schedule)
    db_handle.session.commit()

    assert len(RepeatSchedule.query.filter_by(interval_days=20).all()) == 1
    assert len(RepeatSchedule.query.filter_by(count=15).all()) == 1

    assert len(RepeatSchedule.query.filter_by(interval_days=30).all()) == 0
    assert len(RepeatSchedule.query.filter_by(count=25).all()) == 0

def test_update_event(db_handle):
    '''
    Tests updating the fields of events
    '''
    event = _get_event()

    db_handle.session.add(event)
    db_handle.session.commit()
    event = Event.query.filter_by(name="Meeting").first()
    event.name = "Not a meeting"
    event.duration = 4
    event.note = "didnt attend"
    db_handle.session.commit()
    assert len(Event.query.filter_by(name="Not a meeting").all()) == 1
    assert len(Event.query.filter_by(duration=4).all()) == 1
    assert len(Event.query.filter_by(note="didnt attend").all()) == 1

def test_update_task(db_handle):
    '''
    Tests updating the fields of tasks
    '''
    task = _get_task()

    db_handle.session.add(task)
    db_handle.session.commit()
    task = Task.query.filter_by(name="Study").first()
    task.name = "Workout"
    task.priority = 50
    task.goal = "do everything"
    task.result = "did everything"
    db_handle.session.commit()
    assert len(Task.query.filter_by(name="Workout").all()) == 1
    assert len(Task.query.filter_by(priority=50).all()) == 1
    assert len(Task.query.filter_by(goal="do everything").all()) == 1
    assert len(Task.query.filter_by(result="did everything").all()) == 1

def test_update_item(db_handle):
    '''
    Tests updating the names and values of items
    '''
    item1 = Item(name="item1", value=1.0)

    db_handle.session.add(item1)
    db_handle.session.commit()
    item = Item.query.filter_by(name="item1").first()
    item.name = "item2"
    item.value = 2.0
    db_handle.session.commit()

    assert len(Item.query.filter_by(name="item2").all()) == 1
    assert len(Item.query.filter_by(value=2.0).all()) == 1

def test_update_schedule_event(db_handle):
    '''
    Tests updating the events and schedules of ScheduleEvents
    '''
    event1 = Event(name="event1", duration=1, note="")
    event2 = Event(name="event2", duration=2, note="")
    schedule1 = Schedule(name="schedule1", start_time=datetime(2019, 1, 1, 12, 0, 0, 0), end_time=datetime(2019, 1, 2, 12, 0, 0, 0))
    schedule2 = Schedule(name="schedule2", start_time=datetime(2019, 2, 1, 12, 0, 0, 0), end_time=datetime(2019, 2, 2, 12, 0, 0, 0))
    schedule_event = ScheduleEvent(event=event1, schedule=schedule1)
    db_handle.session.add(schedule_event)
    db_handle.session.commit()
    se = ScheduleEvent.query.filter_by(event_id=event1.id).first()
    assert se is not None
    se.event = event2
    se.schedule = schedule2
    db_handle.session.commit()
    
    assert len(ScheduleEvent.query.filter_by(event_id=event2.id).all()) == 1
    assert len(ScheduleEvent.query.filter_by(schedule_id=schedule2.id).all()) == 1

def test_update_schedule_task(db_handle):
    '''
    Tests updating the events and tasks of ScheduleTasks
    '''
    task1 = Task(name="task1", priority=100, goal="goal1", result="result1")
    task2 = Task(name="task2", priority=90, goal="goal2", result="result2")
    schedule1 = Schedule(name="schedule1", start_time=datetime(2019, 1, 1, 12, 0, 0, 0), end_time=datetime(2019, 1, 2, 12, 0, 0, 0))
    schedule2 = Schedule(name="schedule2", start_time=datetime(2019, 2, 1, 12, 0, 0, 0), end_time=datetime(2019, 2, 2, 12, 0, 0, 0))
    schedule_task = ScheduleTask(task=task1, schedule=schedule1)
    db_handle.session.add(schedule_task)
    db_handle.session.commit()
    st = ScheduleTask.query.filter_by(task_id=task1.id).first()
    assert st is not None
    st.task = task2
    st.schedule = schedule2
    db_handle.session.commit()

    assert len(ScheduleTask.query.filter_by(task_id=task2.id).all()) == 1
    assert len(ScheduleTask.query.filter_by(schedule_id=schedule2.id).all()) == 1

def test_update_schedule_item(db_handle):
    '''
    Tests updating the items and schedules of ScheduleItems
    '''
    item1 = Item(name="item1", value=1.0)
    item2 = Item(name="item2", value=2.0)
    schedule1 = Schedule(name="schedule1", start_time=datetime(2019, 1, 1, 12, 0, 0, 0), end_time=datetime(2019, 1, 2, 12, 0, 0, 0))
    schedule2 = Schedule(name="schedule2", start_time=datetime(2019, 2, 1, 12, 0, 0, 0), end_time=datetime(2019, 2, 2, 12, 0, 0, 0))
    schedule_event = ScheduleItem(item=item1, schedule=schedule1)
    db_handle.session.add(schedule_event)
    db_handle.session.commit()
    si = ScheduleItem.query.filter_by(item_id=item1.id).first()
    assert si is not None
    si.item = item2
    si.schedule = schedule2
    db_handle.session.commit()
    
    assert len(ScheduleItem.query.filter_by(item_id=item2.id).all()) == 1
    assert len(ScheduleItem.query.filter_by(schedule_id=schedule2.id).all()) == 1

def test_update_schedule(db_handle):
    '''
    Tets updating the names, start times and end times of schedules
    '''
    schedule = _get_schedule()
    db_handle.session.add(schedule)
    db_handle.session.commit()

    s = Schedule.query.filter_by(name="Gym").first()
    assert s is not None
    s.name = "Jog"
    s.start_time = datetime(2020, 4, 3, 16, 0, 0, 0)
    s.end_time = datetime(2020, 4, 4, 12, 0, 0, 0)
    db_handle.session.commit()

    s_updated = Schedule.query.filter_by(name="Jog").first()
    assert s_updated is not None
    assert s_updated.start_time.year == 2020
    assert s_updated.start_time.month == 4
    assert s_updated.start_time.day == 3

def test_update_repeat_schedule(db_handle):
    '''
    Tests updating the intervals and counts of repeating schedules
    '''
    repeat_schedule = _get_repeat_schedule()

    db_handle.session.add(repeat_schedule)
    db_handle.session.commit()

    rs = RepeatSchedule.query.filter_by(id=repeat_schedule.id).first()
    assert rs is not None
    rs.interval_days = 30
    rs.count = 40

    db_handle.session.commit()

    assert len(RepeatSchedule.query.filter_by(interval_days=30).all()) == 1
    assert len(RepeatSchedule.query.filter_by(count=40).all()) == 1

def test_delete_event(db_handle):
    '''
    Tests deleting events
    '''
    event = _get_event()

    db_handle.session.add(event)
    db_handle.session.commit()

    assert Event.query.count() == 1

    db_handle.session.delete(event)
    db_handle.session.commit()

    assert Event.query.count() == 0

def test_delete_task(db_handle):
    '''
    Tests deleting tasks
    '''
    task = _get_task()

    db_handle.session.add(task)
    db_handle.session.commit()

    assert Task.query.count() == 1

    db_handle.session.delete(task)
    db_handle.session.commit()

    assert Task.query.count() == 0

def test_delete_item(db_handle):
    '''
    Tests deleting items
    '''
    item = _get_item()

    db_handle.session.add(item)
    db_handle.session.commit()

    assert Item.query.count() == 1

    db_handle.session.delete(item)
    db_handle.session.commit()

    assert Item.query.count() == 0

def test_delete_schedule_event(db_handle):
    '''
    Tests deleting event and schedule relationships
    '''
    schedule_event = ScheduleEvent(event=_get_event(), schedule=_get_schedule())
    db_handle.session.add(schedule_event)
    db_handle.session.commit()

    assert ScheduleEvent.query.count() == 1

    db_handle.session.delete(schedule_event)
    db_handle.session.commit()

    assert ScheduleEvent.query.count() == 0

def tests_delete_schedule_task(db_handle):
    '''
    Tests deleting task and schedule relationships
    '''
    schedule_task = ScheduleTask(task=_get_task(), schedule=_get_schedule())
    db_handle.session.add(schedule_task)
    db_handle.session.commit()

    assert ScheduleTask.query.count() == 1

    db_handle.session.delete(schedule_task)
    db_handle.session.commit()

    assert ScheduleTask.query.count() == 0

def test_delete_schedule_item(db_handle):
    '''
    Tests deleting item and schedule relationships
    '''
    schedule_item = ScheduleItem(item=_get_item(), schedule=_get_schedule())
    db_handle.session.add(schedule_item)
    db_handle.session.commit()

    assert ScheduleItem.query.count() == 1

    db_handle.session.delete(schedule_item)
    db_handle.session.commit()

    assert ScheduleItem.query.count() == 0

def test_delete_schedule(db_handle):
    '''
    Tests deleting schedules
    '''
    schedule = _get_schedule()

    db_handle.session.add(schedule)
    db_handle.session.commit()

    assert Schedule.query.count() == 1

    db_handle.session.delete(schedule)
    db_handle.session.commit()

    assert Schedule.query.count() == 0

def test_delete_repeat_schedule(db_handle):
    '''
    Tests deleting repeating schedules
    '''
    rs = _get_repeat_schedule()

    db_handle.session.add(rs)
    db_handle.session.commit()

    assert RepeatSchedule.query.count() == 1

    db_handle.session.delete(rs)
    db_handle.session.commit()

    assert RepeatSchedule.query.count() == 0

def test_cascade_schedule_tables(db_handle):
    '''
    Tests that corresponding rows of ScheduleEvent/-Task/-Item tables are deleted when the events/tasks/items are deleted
    '''
    event = _get_event()
    task = _get_task()
    item = _get_item()
    schedule = _get_schedule()

    schedule_event = ScheduleEvent(event=event, schedule=schedule)
    schedule_task = ScheduleTask(task=task, schedule=schedule)
    schedule_item = ScheduleItem(item=item, schedule=schedule)

    db_handle.session.add(event)
    db_handle.session.add(task)
    db_handle.session.add(item)
    db_handle.session.add(schedule)
    db_handle.session.add(schedule_event)
    db_handle.session.add(schedule_task)
    db_handle.session.add(schedule_item)
    db_handle.session.commit()

    db_handle.session.delete(event)
    db_handle.session.delete(task)
    db_handle.session.delete(item)

    assert ScheduleEvent.query.count() == 0
    assert ScheduleTask.query.count() == 0
    assert ScheduleItem.query.count() == 0

def test_cascade_schedule_tables_2(db_handle):
    '''
    Tests that corresponding rows of ScheduleEvent/-Task/-Item tables are deleted when the schedule is deleted
    '''
    event = _get_event()
    task = _get_task()
    item = _get_item()
    schedule = _get_schedule()

    schedule_event = ScheduleEvent(event=event, schedule=schedule)
    schedule_task = ScheduleTask(task=task, schedule=schedule)
    schedule_item = ScheduleItem(item=item, schedule=schedule)

    db_handle.session.add(event)
    db_handle.session.add(task)
    db_handle.session.add(item)
    db_handle.session.add(schedule)
    db_handle.session.add(schedule_event)
    db_handle.session.add(schedule_task)
    db_handle.session.add(schedule_item)
    db_handle.session.commit()

    db_handle.session.delete(schedule)

    assert ScheduleEvent.query.count() == 0
    assert ScheduleTask.query.count() == 0
    assert ScheduleItem.query.count() == 0

def test_schedule_foreign_key_null(db_handle):
    '''
    Tests that the repeat_of field of schedule is nulled when the repeat schedule is deleted from the db
    '''
    repeat_schedule = _get_repeat_schedule()
    schedule = _get_schedule()

    schedule.repeat_schedule = repeat_schedule

    db_handle.session.add(repeat_schedule)
    db_handle.session.add(schedule)
    db_handle.session.commit()

    assert Schedule.query.filter_by(name="Gym").first().repeat_of == repeat_schedule.id

    db_handle.session.delete(repeat_schedule)

    assert Schedule.query.filter_by(name="Gym").first().repeat_of is None
