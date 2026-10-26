##################################
# region Kinks ----------------- #
##################################

# What the player allows, per kink key: "yes", "no" or "neutral" (ask).
# Shared by all saves; a key that is missing counts as "neutral".
default persistent.kink_settings = {}

init -99 python:
    from typing import Dict, List, Optional, Tuple

    KINK_SETTINGS = ("yes", "neutral", "no")

    class Kink:
        """
        A content preference the player can allow, block or be asked about.

        The key is the identity: the base game and any number of mods may
        register the same key, and they all share one kink with one setting.

        ### Parameters:
        1. key: str
            - Unique key, compared case-insensitively ("NTR" == "ntr").
        2. title: str
            - Short name for buttons and lists.
        3. description: str
            - One or two neutral, non-explicit sentences for the prompt and
                the settings page.
        """

        def __init__(self, key: str, title: str, description: str = ""):
            self.key = normalize_kink_key(key)
            self.title = title
            self.description = description
            # (source_key, title, description) in registration order
            self.sources: List[Tuple[str, str, str]] = []

        def add_source(self, source_key: str, title: str, description: str):
            if any(source[0] == source_key for source in self.sources):
                return
            if self.sources and (self.sources[0][1] != title or self.sources[0][2] != description):
                log(f"Kink '{self.key}' from '{source_key}' has a different title or description than from '{self.sources[0][0]}'; the first one is used",
                    log_type = "warning", category = "kinks")
            self.sources.append((source_key, title, description))

        def get_source_keys(self) -> List[str]:
            return [source[0] for source in self.sources]

        def get_active_source_keys(self) -> List[str]:
            return [source_key for source_key in self.get_source_keys() if source_key == "base" or is_mod_active(source_key)]

        def _get_text_source(self) -> Tuple[str, str, str]:
            # the base game's text wins, then the first active mod's, then
            # whoever registered it first (a kink of switched-off mods only)
            for source in self.sources:
                if source[0] == "base":
                    return source
            active = self.get_active_source_keys()
            for source in self.sources:
                if source[0] in active:
                    return source
            return self.sources[0]

        def get_title(self) -> str:
            return self._get_text_source()[1] if self.sources else self.title

        def get_description(self) -> str:
            return self._get_text_source()[2] if self.sources else self.description

        def is_known(self) -> bool:
            """
            True while at least one source that registered the kink is active;
            content of a kink nobody active knows about is never allowed.
            """

            return len(self.get_active_source_keys()) > 0

        def to_data(self) -> Dict[str, str]:
            # plain data for persistent.modList: no class instances in persistent
            return {"key": self.key, "title": self.title, "description": self.description}

    # rebuilt at every start; never saved
    kink_registry: Dict[str, Kink] = {}

    def normalize_kink_key(key: str) -> str:
        return str(key).strip().lower()

    def register_kinks(source_key: str, kinks: List[Kink]) -> List[Dict[str, str]]:
        """
        Adds kinks to the registry under the given source (``"base"`` or a
        mod key). Called by ``register_mod(..., kinks = [...])``; the base
        game registers its kinks through it directly.

        ### Returns:
        1. List[Dict[str, str]]
            - The kinks as plain data, for the mod list.
        """

        data = []
        for kink in kinks:
            if not isinstance(kink, Kink):
                log(f"'{source_key}' registered a kink that is not a Kink: {kink!r}", log_type = "error", category = "kinks")
                continue

            registered = kink_registry.get(kink.key)
            if registered is None:
                registered = Kink(kink.key, kink.title, kink.description)
                kink_registry[kink.key] = registered
            registered.add_source(source_key, kink.title, kink.description)
            data.append(kink.to_data())
        return data

    def get_kink(key: str) -> Optional[Kink]:
        return kink_registry.get(normalize_kink_key(key))

    def get_known_kinks() -> List[Kink]:
        """
        All kinks with at least one active source, sorted by title, for the
        settings page.
        """

        return sorted((kink for kink in kink_registry.values() if kink.is_known()), key = lambda kink: kink.get_title().lower())

    def get_mod_kinks(mod_key: str) -> List[Kink]:
        """
        The kinks a mod registered, also while it is switched off (taken from
        its entry in the mod list), so they can be set before switching it on.
        """

        mod = persistent.modList.get(mod_key) if persistent.modList else None
        if mod is None:
            return []
        output = []
        for data in mod.get("kinks", []):
            kink = get_kink(data["key"])
            if kink is None:
                kink = Kink(data["key"], data["title"], data.get("description", ""))
            output.append(kink)
        return output

    ########################
    # Settings and answers

    def get_kink_setting(key: str) -> str:
        """
        The value from the menu: ``"yes"``, ``"no"`` or ``"neutral"``.
        """

        setting = persistent.kink_settings.get(normalize_kink_key(key), "neutral")
        return setting if setting in KINK_SETTINGS else "neutral"

    def set_kink_setting(key: str, setting: str):
        if setting not in KINK_SETTINGS:
            log(f"Unknown kink setting '{setting}' for '{key}'", log_type = "error", category = "kinks")
            return
        key = normalize_kink_key(key)
        persistent.kink_settings[key] = setting
        # a choice made in the menu replaces whatever was answered for now
        _get_kink_session_answers().pop(key, None)

    def _get_kink_session_answers() -> Dict[str, bool]:
        # renpy.session is neither saved nor rolled back and only empties when
        # the game is restarted: exactly the lifetime of a "for now" answer
        return renpy.session.setdefault("kink_answers", {})

    def get_kink_session_answer(key: str) -> Optional[bool]:
        return _get_kink_session_answers().get(normalize_kink_key(key))

    def set_kink_session_answer(key: str, allowed: bool):
        _get_kink_session_answers()[normalize_kink_key(key)] = bool(allowed)

    def get_kink_state(key: str) -> Optional[bool]:
        """
        Whether content with this kink may run right now.

        ### Returns:
        1. Optional[bool]
            - True: allowed (setting yes, or neutral answered "yes, for now").
            - False: not allowed (setting no, neutral answered "no, for now",
                or no active source knows the kink).
            - None: neutral and not answered this session; ask the player.
        """

        kink = get_kink(key)
        if kink is None or not kink.is_known():
            return False

        setting = get_kink_setting(key)
        if setting == "yes":
            return True
        if setting == "no":
            return False
        return get_kink_session_answer(key)

    def get_open_kinks(keys) -> List[str]:
        """
        The keys among ``keys`` that still need an answer, without duplicates,
        in their original order.
        """

        output = []
        for key in keys:
            key = normalize_kink_key(key)
            if key not in output and get_kink_state(key) is None:
                output.append(key)
        return output

init -98 python:
    # The base game's kinks. Mods pass theirs to register_mod(kinks = [...]).
    base_kinks = []

    repair_mod_list()
    persistent.modList['base']['kinks'] = register_kinks("base", base_kinks)

# endregion
##################################
