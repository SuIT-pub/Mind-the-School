init -99 python:
    class Map:
        def __init__(self, key, map_path, *building_keys):
            self.key = key
            self.map_path = get_current_mod_path() + map_path
            self.building_keys = list(building_keys)

        def get_map_path(self) -> str:
            return self.map_path

        def get_building_keys(self) -> List[str]:
            return self.building_keys

        def get_building(self, key: str) -> Building:
            return building_manager.get_building(key)

        def get_buildings(self) -> List[Building]:
            return [self.get_building(key) for key in self.building_keys if self.get_building(key) is not None]

    class MapManager:
        def __init__(self):
            self.maps = {}

        def load_map(self, map_obj: Map):
            if is_mod_active(active_mod_key):
                self.maps[map_obj.key] = map_obj

        def has_map(self, key: str) -> bool:
            return key in self.maps

        def get_map(self, key: str) -> Map:
            if key not in self.maps:
                return self.maps["school"]
            return self.maps[key]

        def get_current_map(self) -> Map:
            # read-only: screens call this during prediction, so no writes here
            return self.get_map(get_game_data("current_map", "school"))

        def add_building_to_map(self, map_key: str, building: Building):
            if map_key in self.maps:
                map = self.get_map(map_key)
                if building.key not in map.building_keys:
                    map.building_keys.append(building.key)

        def clear_maps(self):
            self.maps.clear()

    map_manager = MapManager()

label load_maps:
    $ set_current_mod('base')

    $ map_manager.clear_maps()

    $ map_manager.load_map(Map("school", "images/background/school_map.webp", "school_building", "school_dormitory", "labs", "sports_field", "beach", "staff_lodges", "gym", "swimming_pool", "cafeteria", "bath", "kiosk", "courtyard", "office_building"))

