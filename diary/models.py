import click
from flask.cli import with_appcontext

from . import db


@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    schedule_events = db.relationship("ScheduleEvent", back_populates="schedule", cascade="delete, delete-orphan")
    schedule_tasks = db.relationship("ScheduleTask", back_populates="schedule", cascade="delete, delete-orphan")
    schedule_items = db.relationship("ScheduleItem", back_populates="schedule", cascade="delete, delete-orphan")

class ScheduleEvent(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('schedule_id', 'event_id'),
    )
    schedule_id = db.Column(
        db.ForeignKey('schedule.id'), nullable=False)
    event_id = db.Column(
        db.ForeignKey('event.id'), nullable=False)

    schedule = db.relationship(
        'Schedule', back_populates='schedule_events')
    event = db.relationship(
        'Event', back_populates='schedule_event')

class ScheduleTask(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('schedule_id', 'task_id'),
    )
    schedule_id = db.Column(
        db.ForeignKey('schedule.id'), nullable=False)
    task_id = db.Column(
        db.ForeignKey('task.id'), nullable=False)

    schedule = db.relationship(
            'Schedule', back_populates='schedule_tasks')
    task = db.relationship(
            'Task', back_populates='schedule_task')

class ScheduleItem(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('schedule_id', 'item_id'),
    )
    schedule_id = db.Column(
        db.ForeignKey('schedule.id'), nullable=False)
    item_id = db.Column(
        db.ForeignKey('item.id'), nullable=False)

    schedule = db.relationship(
            'Schedule', back_populates='schedule_items')
    item = db.relationship(
            'Item', back_populates='schedule_item')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, default=0)
    note = db.Column(db.String, nullable=True)

    schedule_event = db.relationship("ScheduleEvent", back_populates="event", cascade="delete, delete-orphan")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=0)
    goal = db.Column(db.String)
    result = db.Column(db.String)

    schedule_task = db.relationship("ScheduleTask", back_populates="task", cascade="delete, delete-orphan")

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    value = db.Column(db.Float, nullable=False)

    schedule_item = db.relationship('ScheduleItem', back_populates='item', cascade="delete, delete-orphan")

