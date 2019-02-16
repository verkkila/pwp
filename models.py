from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///development.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Routine(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    routine_events = db.relationship('RoutineEvent', back_populates='routine')
    routine_items = db.relationship('RoutineItems', back_populates='routine')


class RoutineEvent(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('routine_id', 'event_id'),
    )
    routine_id = db.Column(db.ForeignKey('routine.id'), nullable=False)
    event_id = db.Column(db.ForeignKey('event.id'), nullable=False)

    routine = db.relationship('Routine', back_populates='routine_events')
    event = db.relationship('Event', back_populates='routine_event')


class Event(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    goal = db.Column(db.Integer, nullable=True)
    value = db.Column(db.Integer, default=0)
    duration = db.Column(db.Time, default=0)
    note = db.Column(db.String, nullable=True)

    routine_event = db.relationship('RoutineEvent', back_populates='event')


class RoutineItem(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('routine_id', 'item_id'),
    )
    routine_id = db.Column(db.ForeignKey('routine.id'), nullable=False)
    item_id = db.Column(db.ForeignKey('item.id'), nullable=False)

    routine = db.relationship('Routine', back_populates='routine_events')
    item = db.relationship('Item', back_populates='routine_item')


class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    routine_item = db.relationship('RoutineItem', back_populates='item')


class RecurringRoutines(db.Model):
    routine_id = db.Column(db.ForeignKey('routine.id'),
                           nullable=False, primary_key=True)

    recurring_interval = db.Column(db.Time, default=0)
    recurring_count = db.Column(db.Integer, default=1)

    routine = db.relationship('Routine', back_populates='routine_events')
