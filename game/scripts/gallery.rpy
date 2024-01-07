init python:
    def prep_gallery(location: str, event: str, *key: str):
        if persistent.gallery is None:
            persistent.gallery = {}
        if location not in persistent.gallery.keys():
            persistent.gallery[location] = {}
        if event not in persistent.gallery[location].keys():
            persistent.gallery[location][event] = {'values': {}, 'ranges': {}, 'options': {}}
        current = persistent.gallery[location][event]['values']
        for k in key:
            if k not in current.keys():
                current[k] = {}
                current = current[k]

    class Gallery_Manager:
        def __init__(self, location: str, event: str):
            self.event = event
            self.stack = []
            persistent.gallery[location][event] = {'values': {}, 'ranges': {}, 'options': {}}
            prep_gallery(event)
            self.current_list = persistent.gallery[location][event]['values']
            self.current_ranges = persistent.gallery[location][event]['ranges']
            renpy.call_screen("black_screen_text", 'test')

        def set_stat_ranges(self, **max_limits: List[float]):
            for key in max_limits.keys():
                    self.current_ranges[key] = list(max_limits[key])

        def register_value(self, key: str, value: Any):
            if key in self.current_ranges.keys() and is_float(value):
                value = min(filter(lambda x: x > float(value), self.current_ranges[key]))                

            if key not in self.current_list.keys():
                self.current_list[key] = {}
            if value not in self.current_list[key].keys():
                self.current_list[key][value] = {}
            self.current_list = self.current_list[key][value]

        def get_value(self, key: str, alt: Any = None, **kwargs) -> Any:
            value = get_kwargs(key, alt, **kwargs)
            if not _in_replay:
                self.register_value(key, value)
                log_val('gallery', persistent.gallery)
            return value

        
