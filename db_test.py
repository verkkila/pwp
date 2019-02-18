import os
import tempfile
from datetime import datetime, timedelta

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy import event

from app import app, db
from models import Routine, RecurringRoutine, RoutineEvent, RoutineItem, Event, Item


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
        name="Pushup",
        goal=10,
        note="Success"
    )


def _get_item():
    return Item(
        name="Banana",
        value=2.0,
    )


def _get_routine():
    start = datetime.utcnow()
    end = start + timedelta(hours=1)
    return Routine(
        name="Gym",
        start_time=start,
        end_time=end
    )


def _get_recurring_routine():
    routine = _get_routine()
    return RecurringRoutine(
        routine=routine,
        recurring_interval=20,
        recurring_count=15
    )


def test_add_event_routine(db_handle):
    '''
    Creates new RoutineEvent
    '''
    event = _get_event()
    routine = _get_routine()

    routine_event = RoutineEvent(
        routine=routine,
        event=event
    )
    db_handle.session.add(routine_event)
    db_handle.session.commit()
    assert Routine.query.count() == 1
    assert Event.query.count() == 1
    assert RoutineEvent.query.count() == 1


def test_add_item_routine(db_handle):
    '''
    Creates new RoutineItem
    '''
    item = _get_item()
    routine = _get_routine()

    routine_item = RoutineItem(
        routine=routine,
        item=item
    )

    db_handle.session.add(routine_item)
    db_handle.session.commit()

    assert Routine.query.count() == 1
    assert Item.query.count() == 1
    assert RoutineItem.query.count() == 1

def test_add_recurring_routine(db_handle):
    '''
    Creates new RecurringRoutine
    '''
    recurring_routine = _get_recurring_routine()
    db_handle.session.add(recurring_routine)
    db_handle.session.commit()

    assert RecurringRoutine.query.count() == 1
    assert Routine.query.count() == 1

def test_query_event(db_handle):
    '''
    Tests the success and failure of querying events by their name, goal and note
    '''
    event = _get_event()
    db_handle.session.add(event)
    db_handle.session.commit()

    assert len(Event.query.filter_by(name="Pushup").all()) == 1
    assert len(Event.query.filter_by(goal=10).all()) == 1
    assert len(Event.query.filter_by(note="Success").all()) == 1

    assert len(Event.query.filter_by(name="Pullup").all()) == 0
    assert len(Event.query.filter_by(goal=20).all()) == 0
    assert len(Event.query.filter_by(note="Fail").all()) == 0

def test_query_routine_event(db_handle):
    '''
    Tests the success and failure of querying RoutineEvents by their ids
    '''
    event = _get_event()
    routine = _get_routine()

    routine_event = RoutineEvent(
        routine=routine,
        event=event
    )
    db_handle.session.add(routine_event)
    db_handle.session.commit()

    assert len(RoutineEvent.query.filter_by(event_id=event.id).all()) == 1
    assert len(RoutineEvent.query.filter_by(routine_id=routine.id).all()) == 1

    assert len(RoutineEvent.query.filter_by(event_id=event.id+1).all()) == 0
    assert len(RoutineEvent.query.filter_by(routine_id=routine.id+1).all()) == 0

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

def test_query_routine_item(db_handle):
    '''
    Tests the success and failure of querying RoutineItems by their ids
    '''
    item = _get_item()
    routine = _get_routine()

    routine_item = RoutineItem(
        routine=routine,
        item=item
    )

    db_handle.session.add(routine_item)
    db_handle.session.commit()

    assert len(RoutineItem.query.filter_by(item_id=item.id).all()) == 1
    assert len(RoutineItem.query.filter_by(routine_id=routine.id).all()) == 1

    assert len(RoutineItem.query.filter_by(item_id=item.id+1).all()) == 0
    assert len(RoutineItem.query.filter_by(routine_id=routine.id+1).all()) == 0

def test_query_routine(db_handle):
    '''
    Tests the success and failure of querying routines by their names
    '''
    routine = _get_routine()
    db_handle.session.add(routine)
    db_handle.session.commit()

    assert len(Routine.query.filter_by(name="Gym").all()) == 1

    assert len(Routine.query.filter_by(name="Jog").all()) == 0

def test_query_recurring_routine(db_handle):
    '''
    Tests the success and failure of querying recurring routines by their intervals and counts
    '''
    recurring_routine = _get_recurring_routine()
    db_handle.session.add(recurring_routine)
    db_handle.session.commit()

    assert len(RecurringRoutine.query.filter_by(recurring_interval=20).all()) == 1
    assert len(RecurringRoutine.query.filter_by(recurring_count=15).all()) == 1

    assert len(RecurringRoutine.query.filter_by(recurring_interval=30).all()) == 0
    assert len(RecurringRoutine.query.filter_by(recurring_count=25).all()) == 0

def test_update_event(db_handle):
    '''
    Tests updating the name field of events
    '''
    event = _get_event()

    db_handle.session.add(event)
    db_handle.session.commit()

    event = Event.query.filter_by(name="Pushup").first()

    event.name = "Pullup"

    db_handle.session.commit()

    assert len(Event.query.filter_by(name="Pullup").all()) == 1

def test_update_routine_event(db_handle):
    '''
    Tests updating the events and routines of RoutineEvents
    '''
    event1 = Event(name="event1", goal=1, note="")
    event2 = Event(name="event2", goal=2, note="")
    routine1 = Routine(name="routine1", start_time=datetime(2019, 1, 1, 12, 0, 0, 0), end_time=datetime(2019, 1, 2, 12, 0, 0, 0))
    routine2 = Routine(name="routine2", start_time=datetime(2019, 2, 1, 12, 0, 0, 0), end_time=datetime(2019, 2, 2, 12, 0, 0, 0))
    routine_event = RoutineEvent(event=event1, routine=routine1)
    db_handle.session.add(routine_event)
    db_handle.session.commit()
    re = RoutineEvent.query.filter_by(event_id=event1.id).first()
    assert re is not None
    re.event = event2
    re.routine = routine2
    db_handle.session.commit()
    
    assert len(RoutineEvent.query.filter_by(event_id=event2.id).all()) == 1
    assert len(RoutineEvent.query.filter_by(routine_id=routine2.id).all()) == 1

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

def test_update_routine_item(db_handle):
    '''
    Tests updating the items and routines of RoutineItems
    '''
    item1 = Item(name="item1", value=1.0)
    item2 = Item(name="item2", value=2.0)
    routine1 = Routine(name="routine1", start_time=datetime(2019, 1, 1, 12, 0, 0, 0), end_time=datetime(2019, 1, 2, 12, 0, 0, 0))
    routine2 = Routine(name="routine2", start_time=datetime(2019, 2, 1, 12, 0, 0, 0), end_time=datetime(2019, 2, 2, 12, 0, 0, 0))
    routine_event = RoutineItem(item=item1, routine=routine1)
    db_handle.session.add(routine_event)
    db_handle.session.commit()
    re = RoutineItem.query.filter_by(item_id=item1.id).first()
    assert re is not None
    re.item = item2
    re.routine = routine2
    db_handle.session.commit()
    
    assert len(RoutineItem.query.filter_by(item_id=item2.id).all()) == 1
    assert len(RoutineItem.query.filter_by(routine_id=routine2.id).all()) == 1

def test_update_routine(db_handle):
    '''
    Tets updating the names, start times and end times of routines
    '''
    routine = _get_routine()
    db_handle.session.add(routine)
    db_handle.session.commit()

    r = Routine.query.filter_by(name="Gym").first()
    assert r is not None
    r.name = "Jog"
    r.start_time = datetime(2020, 4, 3, 16, 0, 0, 0)
    r.end_time = datetime(2020, 4, 4, 12, 0, 0, 0)
    db_handle.session.commit()

    r_updated = Routine.query.filter_by(name="Jog").first()
    assert r_updated is not None
    assert r_updated.start_time.year == 2020
    assert r_updated.start_time.month == 4
    assert r_updated.start_time.day == 3

def test_update_recurring_routine(db_handle):
    '''
    Tests updating the routines, intervals and counts of recurring routines
    '''
    recurring_routine = _get_recurring_routine()
    routine2 = Routine(name="Jog", start_time=datetime(2019, 5, 6, 7, 0, 0, 0), end_time=datetime(2019, 6, 7, 8, 0, 0, 0))

    db_handle.session.add(recurring_routine)
    db_handle.session.commit()

    rr = RecurringRoutine.query.filter_by(routine_id=recurring_routine.routine.id).first()
    assert rr is not None
    rr.routine = routine2
    rr.recurring_interval = 30
    rr.recurring_count = 40

    db_handle.session.commit()

    assert len(RecurringRoutine.query.filter_by(routine_id=routine2.id).all()) == 1
    assert len(RecurringRoutine.query.filter_by(recurring_interval=30).all()) == 1
    assert len(RecurringRoutine.query.filter_by(recurring_count=40).all()) == 1
