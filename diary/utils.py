from diary.api import api, ScheduleCollection, ItemCollection, EventCollection, TaskCollection


class MasonBuilder(dict):
    ## Class taken from:
    ### https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2019/implementing-rest-apis-with-flask/#generating-hypermedia
    
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    """

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.

        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.

        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.

        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.

        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md

        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href


class DiaryBuilder(MasonBuilder):
    
    def add_namespace(self):
        return super().add_namespace('diary', '/diary/link-relations/')
    
    def add_control_all_schedules(self):
        return super().add_control(
            'diary:all-schedules',
            api.url_for(ScheduleCollection)
        )

    def add_control_add_schedule(self):
        return super().add_control(
            'diary:add-schedule',
            api.url_for(ScheduleCollection),
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
    
    def add_control_events_in(self, schedule_id):
        raise NotImplementedError

    def add_control_items_in(self, schedule_id):
        raise NotImplementedError

    def add_control_tasks_in(self, schedule_id):
        raise NotImplementedError

    def add_control_delete_item(self, schedule_id, item_id):
        raise NotImplementedError

    def add_control_delete_event(self, schedule_id, event_id):
        raise NotImplementedError
    
    def add_control_delete_task(self, schedule_id,task_id):
        raise NotImplementedError

    def add_control_add_item(self, schedule_id):
        raise NotImplementedError

    def add_control_add_task(self,schedule_id):
        raise NotImplementedError

    def add_control_add_event(self, schedule_id):
        raise NotImplementedError
