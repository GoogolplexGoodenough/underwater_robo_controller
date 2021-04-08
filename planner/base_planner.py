import json
from .hooks import Hook

class BasePlanner:
    def __init__(self, config_file = None):
        self.config_file = config_file
        if config_file is not None:
            self.load_config()
        else:
            self.config = None
        
        self._hooks = []

    def set_config(self, config_file):
        self.config_file = config_file

    def load_config(self):
        with open(self.config_file, 'r') as f:
            config = json.load(config)
            self.config = config

    def register_hook(self, hook, priority = 0):
        assert isinstance(hook, Hook)
        if hasattr(hook, 'priority'):
            raise ValueError('"priority" is a reserved attribute for hooks')
        priority = get_priority(priority)
        hook.priority = priority
        # insert the hook to a sorted list
        inserted = False
        for i in range(len(self._hooks) - 1, -1, -1):
            if priority >= self._hooks[i].priority:
                self._hooks.insert(i + 1, hook)
                inserted = True
                break
        if not inserted:
            self._hooks.insert(0, hook)

    def call_hook(self, fn_name):
        for hook in self._hooks:
            getattr(hook, fn_name)(self)

    def run(self):
        raise NotImplementedError

    def route(self):

        raise NotImplementedError

    def navigate(self):

        raise NotImplementedError

    def look_around(self):

        raise NotImplementedError

    def reset(self):

        raise NotImplementedError

    def run(self):

        raise NotImplementedError