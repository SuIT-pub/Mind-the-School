init -99 python:
    pictogram_manager = None
    class Pictogram:
        def __init__(self, key: str, label: str, tooltip: str, icon: str):
            self.key = key
            self.label = label
            self.tooltip = tooltip
            # Redirect the path into the current mod's folder (base = "" prefix).
            self.icon = get_mod_path(active_mod_key) + icon if icon else icon
            self.label_keys = get_interpolation_keys(label)
            self.tooltip_keys = get_interpolation_keys(tooltip)
            self.icon_keys = get_interpolation_keys(icon)
            remove_all_from_list(self.icon_keys, ["school_level", "teacher_level", "parent_level", "secretary_level"])

        def get_interpolation_keys(self, type: List[str] = []) -> List[str]:
            keys = []
            len_type = len(type)
            if "label" in type or len_type == 0:
                keys.extend(self.label_keys)
            if "tooltip" in type or len_type == 0:
                keys.extend(self.tooltip_keys)
            if "icon" in type or len_type == 0:
                keys.extend(self.icon_keys)
            return keys

        def check_interpolation_keys(self, type: List[str] = [], **kwargs) -> bool:
            keys = self.get_interpolation_keys(type)
            missing_keys = [key for key in keys if key not in kwargs]
            if missing_keys:
                log(f"Missing interpolation keys for {type}: {missing_keys}", log_type="warning", category="pictogram")
                return False
            return True

        def get_label(self, **kwargs) -> str:
            if not self.check_interpolation_keys(type=["label"], **kwargs):
                return None
            return interpolate_string(self.label, **kwargs)

        def get_tooltip(self, **kwargs) -> str:
            if not self.check_interpolation_keys(type=["tooltip"], **kwargs):
                return None
            return interpolate_string(self.tooltip, **kwargs)

        def get_icon(self, **kwargs) -> str:
            if not self.check_interpolation_keys(type=["icon"], **kwargs):
                return None
            return refine_image(self.icon, **kwargs)

    class PictogramManager:
        def __init__(self):
            self.pictograms = {}

        def has_pictogram(self, key: str) -> bool:
            return key in self.pictograms

        def add_pictogram(self, pictogram: Pictogram):
            # Gated on the current mod being active (like event `add_event`): a
            # disabled mod's pictograms are not registered. Base loaders set
            # `set_current_mod('base')`, and base is always active.
            if not is_mod_active(active_mod_key):
                return
            self.pictograms[pictogram.key] = pictogram

        def get_pictogram(self, key: str) -> Pictogram:
            return self.pictograms.get(key)

        def get_interpolation_keys(self, key: str, type: List[str] = []) -> List[str]:
            pictogram = self.get_pictogram(key)
            if pictogram is None:
                return []
            return pictogram.get_interpolation_keys(type)

        def get_label(self, key: str, **kwargs) -> str:
            pictogram = self.get_pictogram(key)
            if pictogram is None:
                return None
            return pictogram.get_label(**kwargs)

        def get_tooltip(self, key: str, **kwargs) -> str:
            pictogram = self.get_pictogram(key)
            if pictogram is None:
                return None
            return pictogram.get_tooltip(**kwargs)

        def get_icon(self, key: str, **kwargs) -> str:
            pictogram = self.get_pictogram(key)
            if pictogram is None:
                return None
            return pictogram.get_icon(**kwargs)

    def load_pictograms(*pictograms: Pictogram):
        for pictogram in pictograms:
            pictogram_manager.add_pictogram(pictogram)

label load_pictograms:
    $ set_current_mod('base')

    if pictogram_manager is None:
        $ pictogram_manager = PictogramManager()

    $ pictogram_manager.add_pictogram(Pictogram("teachers", "Convince Teachers", "The faculty needs to be won over.", "images/icons/teacher.webp"))
    $ pictogram_manager.add_pictogram(Pictogram("parents", "Convince Parents", "The parents need to be brought on board.", "images/icons/ages.webp"))
    $ pictogram_manager.add_pictogram(Pictogram("students", "Convince Students", "The student body needs winning over.", "images/icons/graduate-cap.webp"))
    $ pictogram_manager.add_pictogram(Pictogram("vote", "Hold a Vote", "This has to pass a vote at the PTA meeting.", "images/icons/vote.webp"))
    $ pictogram_manager.add_pictogram(Pictogram("scandal", "Avoid a Scandal", "Pushing too hard risks a scandal.", "images/icons/siren.webp"))
    $ pictogram_manager.add_pictogram(Pictogram("curriculum", "Change Curriculum", "This reworks what gets taught.", "images/icons/book-cover.webp"))
    $ pictogram_manager.add_pictogram(Pictogram("demo", "Run a Demonstration", "This needs to be shown in practice.", "images/icons/teacher.webp"))
    $ pictogram_manager.add_pictogram(Pictogram("dresscode", "Change Dress Code", "This adjusts the school dress code.", "images/icons/clothes.webp"))
    $ pictogram_manager.add_pictogram(Pictogram("facility", "Build Facility", "This constructs or upgrades a space on campus.", "images/icons/house.webp"))
    $ pictogram_manager.add_pictogram(Pictogram("money", "Cover the Cost", "This takes funding to push through.", "images/icons/cash.webp"))
    $ pictogram_manager.add_pictogram(Pictogram("rapport", "Build Rapport", "This means strengtehning ties with the people involved.", "images/icons/heart.webp"))
    $ pictogram_manager.add_pictogram(Pictogram("stats", "Raise Stats", "Certain school stats need to be higher first.", "images/icons/level_icon_511_black.webp"))

    return

