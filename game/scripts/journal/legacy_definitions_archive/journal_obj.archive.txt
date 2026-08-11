init -7 python:
    from deprecated import deprecated

    @deprecated(version='0.2.3', reason="Replaced by Unlockable / Situation; kept for save compatibility.")
    class Journal_Obj:
        """Legacy journal object base.

        Kept so existing saves can unpickle ``Rule`` / ``Club`` instances.
        Do not use for new content.
        """

        def __init__(self, name: str = "", title: str = ""):
            self._name = name
            self._title = title
            self._description = [""]
            self._image_path_alt = "images/journal/empty_image.webp"
            self._image_path = "images/journal/empty_image.webp"
            self._unlock_conditions = {}
            self._vote_comments = {}
            self._default_comments = {}
            self._unlock_effects = []
            self._unlocked = False

        def get_type(self) -> str:
            return "journal_obj"
