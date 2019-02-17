import os
import tempfile
from datetime import datetime, timedelta

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy import event

from app import app, db
from models import Routine, RecurringRoutines, RoutineEvent, RoutineItem, Event, Item


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
        price=2.0,
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
    return RecurringRoutines(
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

    assert RecurringRoutines.query.count() == 1
    assert Routine.query.count() == 1
