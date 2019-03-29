from src.app import app, db



ScheduleEvent = db.Table(
    'ScheduleEvent',
    db.Column(
        'schedule_id',
        db.ForeignKey('schedule.id'),
        primary_key=True,
        ),
    db.Column(
        'event_id',
        db.ForeignKey('event.id'),
        primary_key=True
        )
    )

ScheduleItem = db.Table(
    'ScheduleItem',
    db.Column(
        'schedule_id',
        db.ForeignKey('schedule.id'),
        primary_key=True,
        ),
    db.Column(
        'item_id',
        db.ForeignKey('item.id'),
        primary_key=True
        )
    )

ScheduleTask = db.Table(
    'ScheduleTask',
    db.Column(
        'schedule_id',
        db.ForeignKey('schedule.id'),
        primary_key=True,
        ),
    db.Column(
        'task_id',
        db.ForeignKey('task.id'),
        primary_key=True
        )
    )


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    schedule_events = db.relationship("ScheduleEvent", back_populates="schedule", cascade="delete, delete-orphan")
    schedule_tasks = db.relationship("ScheduleTask", back_populates="schedule", cascade="delete, delete-orphan")
    schedule_items = db.relationship("ScheduleItem", back_populates="schedule", cascade="delete, delete-orphan")


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

