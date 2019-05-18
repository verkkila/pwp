import re
import json

from flask import request, Response


SCHEDULE_COLLECTION_URI = '/diary/schedules/'
SCHEDULE_URI = '/diary/schedules/<schedule_id>/'

EVENT_COLLECTION_URI = '/diary/schedules/<schedule_id>/events/'
EVENT_URI = '/diary/schedules/<schedule_id>/events/<event_id>/'

ITEM_COLLECTION_URI = '/diary/schedules/<schedule_id>/items/'
ITEM_URI = '/diary/schedules/<schedule_id>/items/<item_id>/'

TASK_COLLECTION_URI = '/diary/schedules/<schedule_id>/tasks/'
TASK_URI = '/diary/schedules/<schedule_id>/tasks/<task_id>/'


MIMETYPE = 'application/vnd.mason+json'
REGEX_PATTERN = r'<[a-z_]*>'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class MasonBuilder(dict):
    ## Class taken from:
    ### https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2019/implementing-rest-apis-with-flask/#generating-hypermedia
    
    '''
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    '''

    def add_error(self, title, details):
        '''
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.

        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.

        : param str title: Short title for the error
        : param str details: Longer human-readable description
        '''

        self['@error'] = {
            '@message': title,
            '@messages': [details],
        }

    def add_namespace(self, ns, uri):
        '''
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.

        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        '''

        if '@namespaces' not in self:
            self['@namespaces'] = {}

        self['@namespaces'][ns] = {
            'name': uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        '''
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.

        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md

        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        '''

        if '@controls' not in self:
            self['@controls'] = {}

        self['@controls'][ctrl_name] = kwargs
        self['@controls'][ctrl_name]['href'] = href


class DiaryBuilder(MasonBuilder):
    @staticmethod
    def create_error_response(status_code, title, message=None):
        resource_url = request.path
        body = MasonBuilder(resource_url=resource_url)
        body.add_error(title, message)
        body.add_control("profile", href='/profiles/error/')
        return Response(json.dumps(body, indent=4), status=status_code, mimetype=MIMETYPE)


    def add_namespace(self):
        return super().add_namespace('diary', '/diary/link-relations/')
    
    def add_control_all_schedules(self):
        return super().add_control(
            'diary:all-schedules',
            SCHEDULE_COLLECTION_URI
        )

    def add_control_add_schedule(self):
        return super().add_control(
            'diary:add-schedule',
            SCHEDULE_COLLECTION_URI,
            method='POST',
            encoding='json',
            schema={
                'type':'object',
                'properties':{
                    'start_time':{
                        'description':'Start time',
                        'type':'datetime'
                    },
                    'end_time':{
                        'description':'End time',
                        'type':'datetime'
                    }
                }
            },
            required=['start_time','end_time']
        )
    def add_control_edit_schedule(self, schedule_id):
        super().add_control(
            'edit',
            re.sub(REGEX_PATTERN, '{}',SCHEDULE_URI).format(schedule_id),
            encoding='json',
            method='PUT',
            schema={
                'type':'object',
                'properties':{
                    'start_time':{
                        'description':'Start time',
                        'type':'datetime',
                    },
                    'end_time':{
                        'description':'End time',
                        'type':'datetime',
                    },
                    'name':{
                        'description':'Schedule name',
                        'type':'string',
                    },
                },
            },
            required=['name', 'duration']
        )
    def add_control_delete_schedule(self, schedule_id):
        super().add_control(
            'diary:delete',
            re.sub(REGEX_PATTERN, '{}',SCHEDULE_URI).format(schedule_id),
        )
    
    def add_control_events_in(self, schedule_id):
        super().add_control(
            'diary:events-in',
            re.sub(REGEX_PATTERN, '{}',EVENT_COLLECTION_URI).format(schedule_id),
        )

    def add_control_items_in(self, schedule_id):
        super().add_control(
            'diary:items-in',
            re.sub(REGEX_PATTERN, '{}',ITEM_COLLECTION_URI).format(schedule_id),
        )

    def add_control_tasks_in(self, schedule_id):
        super().add_control(
            'diary:tasks-in',
            re.sub(REGEX_PATTERN, '{}',TASK_COLLECTION_URI).format(schedule_id),
        )
    def add_control_delete_item(self, schedule_id, item_id):
        super().add_control(
            'diary:delete',
            re.sub(REGEX_PATTERN, '{}',ITEM_URI).format(schedule_id, item_id),
            method='DELETE'
        )

    def add_control_delete_event(self, schedule_id, event_id):
        super().add_control(
            'diary:delete',
            re.sub(REGEX_PATTERN, '{}',EVENT_URI).format(schedule_id, event_id),
            method='DELETE'
        )
    
    def add_control_delete_task(self, schedule_id,task_id):
        super().add_control(
            'diary:delete',
            re.sub(REGEX_PATTERN, '{}',TASK_URI).format(schedule_id, task_id),
            method='DELETE'
        )

    def add_control_add_item(self, schedule_id):
        super().add_control(
            'diary:add-item',
            re.sub(REGEX_PATTERN, '{}',ITEM_COLLECTION_URI).format(schedule_id),
            method='POST',
            encoding='json',
            schema={
                'type':'object',
                'properties':{
                    'name':{
                        'description':'item name',
                        'type':'string'
                    },
                    'value':{
                        'description':'Item value',
                        'type':'float'
                    }
                }
            },
            required=['name', 'value']
        )
    def add_control_add_task(self,schedule_id):
        super().add_control(
            'diary:add-task',
            re.sub(REGEX_PATTERN, '{}',TASK_COLLECTION_URI).format(schedule_id),
            method='POST',
            encoding='json',
            schema={
                'type':'object',
                'properties':{
                    'name':{
                        'description':'Task name',
                        'type':'string'
                    },
                    'priority':{
                        'description':'Task priority',
                        'type':'integer'
                    },
                    'goal':{
                        'description':'Task goal',
                        'type':'string'
                    },
                    'result':{
                        'description':'Task result',
                        'type':'string'
                    }
                }
            },
            required=['name', 'priority']
        )

    def add_control_add_event(self, schedule_id):
        super().add_control(
            'diary:add-event',
            re.sub(REGEX_PATTERN, '{}',EVENT_COLLECTION_URI).format(schedule_id),
            method='POST',
            encoding='json',
            schema={
                'type':'object',
                'properties':{
                    'name':{
                        'description':'event name',
                        'type':'string'
                    },
                    'duration':{
                        'description':'event duration',
                        'type':'integer'
                    },
                    'note':{
                        'description':'event note',
                        'type':'string'
                    }
                }
            },
            required=['name', 'duration']
        )
    def add_control_edit_item(self, schedule_id, item_id):
        super().add_control(
            'edit',
            re.sub(REGEX_PATTERN, '{}',ITEM_URI).format(schedule_id, item_id),
            encoding='json',
            method='PATCH',
            schema={
                'type':'object',
                'properties':{
                    'name':{
                        'description':'item name',
                        'type':'string'
                    },
                    'value':{
                        'description':'Item value',
                        'type':'float'
                    }
                }
            },
            required=['name', 'value']
        )

    def add_control_edit_event(self, schedule_id, event_id):
            super().add_control(
            'edit',
            re.sub(REGEX_PATTERN, '{}',EVENT_URI).format(schedule_id, event_id),
            encoding='json',
            method='PATCH',
            schema={
                'type':'object',
                'properties':{
                    'name':{
                        'description':'event name',
                        'type':'string',
                    },
                    'duration':{
                        'description':'event duration',
                        'type':'integer',
                    },
                    'note':{
                        'description':'event note',
                        'type':'string',
                    },
                },
            },
            required=['name', 'duration']
        )
    
    def add_control_edit_task(self, schedule_id, task_id):
            super().add_control(
            'edit',
            re.sub(REGEX_PATTERN, '{}',TASK_URI).format(schedule_id, task_id),
            encoding='json',
            method='PATCH',
            schema={
                'type':'object',
                'properties':{
                    'name':{
                        'description':'Task name',
                        'type':'string'
                    },
                    'priority':{
                        'description':'Task priority',
                        'type':'integer'
                    },
                    'goal':{
                        'description':'Task goal',
                        'type':'String'
                    }
                }
            },
            required=['name', 'priority']
        )
