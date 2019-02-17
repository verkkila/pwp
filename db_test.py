import os
import tempfile

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy import event

from app import app, db
from models import Routine, RecurringRoutines, RoutineEvent, RoutineItem, Event, Item


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

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

