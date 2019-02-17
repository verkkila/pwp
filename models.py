from app import app, db


class Routine(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    routine_events = db.relationship(
        'RoutineEvent', back_populates='routine')
    routine_items = db.relationship(
        'RoutineItem', back_populates='routine')
    recurring_routine = db.relationship(
        'RecurringRoutine', back_populates='routine')


class RoutineEvent(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('routine_id', 'event_id'),
    )
    routine_id = db.Column(
        db.ForeignKey('routine.id'), nullable=False)
    event_id = db.Column(
        db.ForeignKey('event.id'), nullable=False)

    routine = db.relationship(
        'Routine', back_populates='routine_events')
    event = db.relationship(
        'Event', back_populates='routine_event')


class Event(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    goal = db.Column(db.Integer, nullable=True)
    value = db.Column(db.Integer, default=0)
    duration = db.Column(db.Integer, default=0)
    note = db.Column(db.String, nullable=True)

    routine_event = db.relationship(
        'RoutineEvent', back_populates='event')


class RoutineItem(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('routine_id', 'item_id'),
    )
    routine_id = db.Column(
        db.ForeignKey('routine.id'), nullable=False)
    item_id = db.Column(
        db.ForeignKey('item.id'), nullable=False)

    routine = db.relationship('Routine', back_populates='routine_items')
    item = db.relationship('Item', back_populates='routine_item')


class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    value = db.Column(db.Float, nullable=False)

    routine_item = db.relationship('RoutineItem', back_populates='item')


class RecurringRoutine(db.Model):
    routine_id = db.Column(db.ForeignKey('routine.id'),
                           nullable=False, primary_key=True)

    recurring_interval = db.Column(db.Integer, default=0)
    recurring_count = db.Column(db.Integer, default=1)

    routine = db.relationship('Routine', back_populates='recurring_routine')
