##############################
# region Channels ---------- #
##############################

init -5 python:
    # Two channels share the ambience mixer so a change of place crossfades:
    # the old sound fades out on one while the new one fades in on the other.
    # tight=True keeps the fading-out loop wrapping instead of ending mid-fade.
    renpy.music.register_channel("ambience_a", mixer = "ambience", loop = True, tight = True)
    renpy.music.register_channel("ambience_b", mixer = "ambience", loop = True, tight = True)

    AMBIENCE_CHANNELS = ("ambience_a", "ambience_b")

    # share of the ambience volume that stays audible under a scene
    AMBIENCE_EVENT_VOLUME = 0.35
    # crossfade and volume-glide time in seconds
    AMBIENCE_FADE = 1.5

# endregion
##############################

#############################
# region Ambience --------- #
#############################

init -5 python:
    from typing import Dict, List

    class Ambience:
        """
        One candidate sound for a location or map, shaped like BGImage.

        ### Parameters:
        1. sound: str
            - A file under game/ ("audio/empty-room.ogg") or an audio. name (audio.empty_room).
            - A path with a folder resolves into the registering mod's folder.
        2. priority: int
            - The highest usable priority wins; ties keep declaration order.
        3. *conditions: Condition
            - All must pass. They are checked without event kwargs.
            - Use conditions that read global state: time, school level, flags, situations.
        4. volume: float (default 1.0)
            - 0.0 - 1.0, multiplied with the player's ambience slider.
        """

        def __init__(self, sound: str, priority: int = 0, *conditions: Condition, volume: float = 1.0):
            # bare file names are looked up in game/audio by Ren'Py and never belong to a mod folder
            if "/" in sound:
                sound = get_mod_path(active_mod_key) + sound
            self._sound = sound
            self._priority = priority
            self._conditions = list(conditions)
            self._volume = volume

        def can_be_used(self, **kwargs) -> bool:
            # is_fulfilled passes everything during a replay so event gates open;
            # ambience describes the world rather than gating it, so it must stay
            # honest there or every replay would hear the top-priority candidate
            return all(
                condition.options.has_option('Optional') or condition.check_condition(**kwargs)
                for condition in self._conditions)

        def get_priority(self) -> int:
            return self._priority

        def get_sound(self) -> str:
            return self._sound

        def get_volume(self) -> float:
            return self._volume

    class AmbienceStorage:
        """
        The ambience candidates of one location or map.

        ### Parameters:
        1. fallback: Ambience | None
            - Plays when no candidate fits; None means silence.
        2. *ambiences: Ambience
            - The candidates.
        """

        def __init__(self, fallback: Ambience = None, *ambiences: Ambience):
            self._fallback = fallback
            self._ambiences = list(ambiences)
            # "building:courtyard"; set on registration, read by the mod overview
            self._key = None

        def add_ambience(self, *ambience: Ambience):
            """
            Adds candidates, e.g. from a mod to a base location. Skipped while the
            registering mod is inactive.
            """

            if self._key is not None and get_mod_content_owner("ambience", self._key) not in (None, active_mod_key):
                record_mod_change("ambience_add", self._key)
            if not is_mod_active(active_mod_key):
                return
            self._ambiences.extend(ambience)

        def get_ambiences(self) -> List[Ambience]:
            return self._ambiences

        def resolve(self, **kwargs) -> Ambience:
            """
            Returns the usable candidate with the highest priority, the fallback when
            none fits, or None for silence.
            """

            best = None
            for ambience in self._ambiences:
                if not ambience.can_be_used(**kwargs):
                    continue
                if best is None or ambience.get_priority() > best.get_priority():
                    best = ambience
            return best if best is not None else self._fallback

    # Plain init dicts, deliberately not pickled into saves: a location's sound
    # changed in code reaches old saves on the next load.
    building_ambiences = {}
    map_ambiences = {}

    def _register_ambience(registry: Dict[str, AmbienceStorage], kind: str, key: str, storage: AmbienceStorage):
        storage._key = "{}:{}".format(kind, key)
        record_mod_content("ambience", storage._key)
        if is_mod_active(active_mod_key):
            registry[key] = storage

    def register_building_ambience(key: str, storage: AmbienceStorage):
        """
        Registers the ambience of a building, played when the player enters it.
        A building without one keeps whatever was playing (usually the map's sound).
        """

        _register_ambience(building_ambiences, "building", key, storage)

    def register_map_ambience(key: str, storage: AmbienceStorage):
        """
        Registers the ambience of a map, played in the map overview.
        """

        _register_ambience(map_ambiences, "map", key, storage)

    def get_building_ambience(key: str) -> AmbienceStorage:
        return building_ambiences.get(key)

    def get_map_ambience(key: str) -> AmbienceStorage:
        return map_ambiences.get(key)

    def _get_ambience_registry(kind: str) -> Dict[str, AmbienceStorage]:
        if kind == "map":
            return map_ambiences
        return building_ambiences

# endregion
#############################

#############################
# region Playback -------- #
#############################

# Lives in the save so a loaded game knows which channel holds the sound and
# whether a scene had ducked it; Ren'Py restores the channels themselves.
default ambience_state = {
    "channel": "ambience_a",
    "sound": None,
    "volume": 1.0,
    "ducked": False,
    "location": None,
}

init -5 python:
    def _ambience_target_volume() -> float:
        factor = AMBIENCE_EVENT_VOLUME if ambience_state["ducked"] else 1.0
        return ambience_state["volume"] * factor

    def _play_ambience_file(sound: str, volume: float):
        current = ambience_state["channel"]
        ambience_state["volume"] = volume

        # the same file only glides to its new volume, so walking between two
        # rooms with the same tone never restarts the loop
        if ambience_state["sound"] == sound and renpy.music.is_playing(channel = current):
            renpy.music.set_volume(_ambience_target_volume(), delay = AMBIENCE_FADE, channel = current)
            return

        following = AMBIENCE_CHANNELS[1] if current == AMBIENCE_CHANNELS[0] else AMBIENCE_CHANNELS[0]
        renpy.music.stop(channel = current, fadeout = AMBIENCE_FADE)
        renpy.music.set_volume(_ambience_target_volume(), channel = following)
        renpy.music.play(sound, channel = following, loop = True, fadein = AMBIENCE_FADE)

        ambience_state["channel"] = following
        ambience_state["sound"] = sound

    def play_ambience(sound: str, volume: float = 1.0):
        """
        Plays a sound as ambience from inside a scene. It replaces the location's
        sound until end_event and plays un-ducked: the scene asked for it.
        """

        ambience_state["ducked"] = False
        _play_ambience_file(sound, volume)

    def stop_ambience(fadeout: float = None):
        """
        Silences the ambience. end_event brings the location's sound back.
        """

        if fadeout is None:
            fadeout = AMBIENCE_FADE
        for channel in AMBIENCE_CHANNELS:
            renpy.music.stop(channel = channel, fadeout = fadeout)
        ambience_state["sound"] = None

    def duck_ambience():
        """
        Lowers the ambience under a scene. Safe to call repeatedly (fragments,
        decision re-entry).
        """

        ambience_state["ducked"] = True
        renpy.music.set_volume(_ambience_target_volume(), delay = 1.0, channel = ambience_state["channel"])

    def unduck_ambience():
        ambience_state["ducked"] = False
        renpy.music.set_volume(_ambience_target_volume(), delay = 1.0, channel = ambience_state["channel"])

    def play_location_ambience(kind: str, key: str, ducked: bool = False):
        """
        Plays the registered ambience of a building or map and remembers it as the
        current location, so end_event can bring it back.

        ### Parameters:
        1. kind: str
            - "building" or "map".
        2. key: str
            - The building or map key.
        3. ducked: bool (default False)
            - Start already lowered, for a scene that brings its own location (replays).
        """

        storage = _get_ambience_registry(kind).get(key)
        if storage is None and kind == "building":
            # unregistered buildings inherit the map's sound (a beach under the
            # forest), which is what they did before the registry existed; the map
            # becomes the location so end_event also ends a scene override there
            # the key straight from game data: map_manager is only filled once load_maps ran
            play_location_ambience("map", get_game_data("current_map", "school"), ducked)
            return

        ambience_state["location"] = (kind, key)
        ambience_state["ducked"] = ducked
        if storage is None:
            renpy.music.set_volume(_ambience_target_volume(), delay = 1.0, channel = ambience_state["channel"])
            return

        ambience = storage.resolve()
        if ambience is None:
            stop_ambience()
            return

        _play_ambience_file(ambience.get_sound(), ambience.get_volume())

    def restore_location_ambience():
        """
        Ends ducking and any scene override, re-resolving the current location so
        a level-up or flag set during the scene is heard right away.
        """

        location = ambience_state["location"]
        if location is None:
            unduck_ambience()
            return
        play_location_ambience(*location)

    def _ambience_mp3_to_ogg(filename: str) -> str:
        # Saves keep what each channel was playing, and before 0.2.2 the room tone
        # was game/audio/*.mp3; those files are .ogg now, so an old save (or a mod
        # naming the file directly) would crash the audio thread on load.
        if not filename.lower().endswith(".mp3"):
            return filename
        if renpy.loadable(filename) or renpy.loadable("audio/" + filename):
            return filename
        ogg = filename[:-4] + ".ogg"
        if renpy.loadable(ogg) or renpy.loadable("audio/" + ogg):
            return ogg
        return filename

    config.audio_filename_callback = _ambience_mp3_to_ogg

    def _move_legacy_ambience_after_load():
        # A pre-0.2.2 save has its room tone looping on the effects channel. Left
        # there it would play on top of the new ambience channels at the next
        # location change, so it moves over: stop it, play the map's ambience.
        # get_playing() is still None here: Ren'Py restarts the saved loops at the
        # next interaction, from the channel context, so read what it will restart
        saved = renpy.audio.audio.get_channel("sound").context.last_filenames
        if not saved:
            return
        legacy = os.path.splitext(os.path.basename(saved[0]))[0]
        known = set()
        for registry in (building_ambiences, map_ambiences):
            for storage in registry.values():
                for ambience in storage.get_ambiences() + ([storage._fallback] if storage._fallback else []):
                    known.add(os.path.splitext(os.path.basename(ambience.get_sound()))[0])
        if legacy not in known:
            return
        renpy.music.stop(channel = "sound", fadeout = AMBIENCE_FADE)
        if ambience_state["sound"] is None:
            play_location_ambience("map", get_game_data("current_map", "school"))

    config.after_load_callbacks.append(_move_legacy_ambience_after_load)

    def play_sound(sound: str, loop: bool = False, volume: float = 1.0, fadein: float = 1.0):
        """
        Plays a one-shot effect on the sound channel (Effects slider).
        Looping room tone through here is deprecated: use register_building_ambience.
        """

        if not renpy.music.get_playing(channel='sound') == sound or not renpy.music.is_playing(channel='sound'):
            renpy.sound.play(sound, loop = loop, relative_volume = volume, fadein = fadein)

# endregion
#############################

#############################
# region Music ----------- #
#############################

init -5 python:
    # Where a track sits at volume 1.0: tracks come mastered anywhere between
    # -10 and -17 LUFS, so each one states its measured loudness and is turned
    # down to this line. -20 keeps the music about 9 LU over the map's room
    # tone and leaves the slider's top end for players who want more.
    MUSIC_REFERENCE_LUFS = -20.0
    # the bed under scenes sits 6 dB below map music, over the ducked ambience
    MUSIC_BED_VOLUME = 0.5
    # the map plays a little under full level (LO's ear test, 2026-10-21)
    MUSIC_MAP_VOLUME = 0.75
    MUSIC_FADE = 2.0
    # a track that was just started can read as "not playing" for a moment
    # while the audio thread opens it; the playlist waits this long before it
    # treats silence as the end of a track
    MUSIC_START_GRACE = 1.5

    class MusicTrack(Ambience):
        """
        One piece of music. Shaped like Ambience (priority + conditions pick it
        from a MusicStorage), plus what music needs on top.

        ### Parameters:
        1. sound: str
            - A file under game/ ("audio/music/brain-fog.ogg").
            - A path with a folder resolves into the registering mod's folder.
        2. priority: int (default 0)
        3. *conditions: Condition
            - Checked like Ambience conditions (honest in replays).
        4. loudness: float (default None)
            - The file's integrated loudness in LUFS (None = play as is).
            - The track is turned down to MUSIC_REFERENCE_LUFS, so all play equally loud.
        5. end: float (default None)
            - Stop playing at this second, e.g. to skip silence at the file's end.
            - The file itself stays untouched (licences like CC BY-SA).
        6. volume: float (default 1.0)
            - Extra factor on top of the loudness match.
        """

        def __init__(self, sound: str, priority: int = 0, *conditions: Condition, loudness: float = None, end: float = None, volume: float = 1.0):
            super().__init__(sound, priority, *conditions, volume = volume)
            self._loudness = loudness
            self._end = end

        def get_spec(self) -> str:
            if self._end is None:
                return self.get_sound()
            return "<to {}>{}".format(self._end, self.get_sound())

        def get_volume(self) -> float:
            factor = 1.0
            if self._loudness is not None:
                factor = min(1.0, 10 ** ((MUSIC_REFERENCE_LUFS - self._loudness) / 20))
            return factor * self._volume

    class MusicStorage(AmbienceStorage):
        """
        Music candidates of a map, picked like ambience: the highest-priority
        MusicTrack whose conditions pass, else the fallback (None = no music).
        """

    map_music = {}
    music_pools = {}
    menu_music = {"track": None}

    def register_map_music(key: str, storage: MusicStorage):
        """
        Registers the music of a map. It plays once each time a new daytime
        starts on that map, then the map is left to its ambience.
        """

        storage._key = "map_music:{}".format(key)
        record_mod_content("music", storage._key)
        if is_mod_active(active_mod_key):
            map_music[key] = storage

    def register_music_pool(key: str, *tracks: MusicTrack):
        """
        Registers a playlist under a mood key ("bed", "tender", ...). play_music(key)
        plays its tracks one after another in a shuffled order, without repeats
        until all have played.
        """

        record_mod_content("music", "pool:{}".format(key))
        if is_mod_active(active_mod_key):
            music_pools[key] = list(tracks)

    def add_to_music_pool(key: str, *tracks: MusicTrack):
        """
        Adds tracks to an existing pool, e.g. from a mod to the base game's "bed".
        """

        if get_mod_content_owner("music", "pool:{}".format(key)) not in (None, active_mod_key):
            record_mod_change("music_add", "pool:{}".format(key))
        if is_mod_active(active_mod_key) and key in music_pools:
            music_pools[key].extend(tracks)

    def register_menu_music(track: MusicTrack):
        """
        Sets the main menu's music; it loops while the menu is open.
        """

        record_mod_content("music", "menu")
        if is_mod_active(active_mod_key):
            menu_music["track"] = track

# Saved: which pool plays and in what order, so a loaded game picks the
# playlist up again, and which daytime last got its map music.
default music_state = {
    "mode": None,
    "pool": None,
    "order": [],
    "index": 0,
    "level": 1.0,
    "map_slot": None,
    "map_track": None,
}

init -5 python:
    import time as _music_clock

    # wall-clock start of the current track; not saved, a loaded game starts fresh
    _music_started = [0.0]

    def _play_music_track(track: MusicTrack, level: float = 1.0, loop: bool = False):
        renpy.music.play(track.get_spec(), channel = "music", loop = loop,
            fadeout = MUSIC_FADE, fadein = MUSIC_FADE, relative_volume = track.get_volume() * level)
        _music_started[0] = _music_clock.time()

    def _play_next_pool_track():
        tracks = music_pools.get(music_state["pool"], [])
        if not tracks:
            music_state["mode"] = None
            return

        order = music_state["order"]
        if music_state["index"] >= len(order) or any(i >= len(tracks) for i in order):
            last = order[music_state["index"] - 1] if order and 0 < music_state["index"] <= len(order) else None
            order = list(range(len(tracks)))
            renpy.random.shuffle(order)
            # a fresh round never opens with the track that just ended
            if len(order) > 1 and order[0] == last:
                order.append(order.pop(0))
            music_state["order"] = order
            music_state["index"] = 0

        track = tracks[order[music_state["index"]]]
        music_state["index"] += 1
        _play_music_track(track, music_state["level"])

    def play_music(pool: str, volume: float = None):
        """
        Plays a music pool. The same pool already playing keeps going (no restart);
        another one fades over.

        ### Parameters:
        1. pool: str
            - A key from register_music_pool ("bed", ...).
        2. volume: float (default None)
            - Level of the pool; None = MUSIC_BED_VOLUME for "bed", else 1.0.
        """

        if volume is None:
            volume = MUSIC_BED_VOLUME if pool == "bed" else 1.0
        if music_state["mode"] == "pool" and music_state["pool"] == pool and renpy.music.is_playing(channel = "music"):
            return

        if pool not in music_pools:
            log("Unknown music pool '{}'; register it with register_music_pool".format(pool), log_type = "error", category = "audio")
            return

        music_state["mode"] = "pool"
        music_state["pool"] = pool
        music_state["level"] = volume
        music_state["order"] = []
        music_state["index"] = 0
        _play_next_pool_track()

    def stop_music(fadeout: float = None):
        """
        Fades the music out and keeps it out until something starts music again
        (the next event, the next daytime on the map). Use it for deliberate
        silence inside a scene.
        """

        music_state["mode"] = None
        renpy.music.stop(channel = "music", fadeout = MUSIC_FADE if fadeout is None else fadeout)

    def play_map_music(key: str):
        """
        Called by map_entry. A new daytime gets the map's track once; coming
        back to the map within the same daytime leaves it to the ambience.
        """

        slot = (time.year, time.month, time.day, time.daytime, key)
        if music_state["map_slot"] == slot:
            # an event's bed has no business on the map
            if music_state["mode"] == "pool":
                stop_music()
            return
        music_state["map_slot"] = slot

        storage = map_music.get(key)
        track = storage.resolve() if storage is not None else None
        if track is None:
            stop_music()
            return

        # one track covers several daytimes (noon to afternoon): it marks the
        # start of that part of the day once instead of restarting at each step
        if music_state.get("map_track") == track.get_sound():
            if music_state["mode"] == "pool":
                stop_music()
            return
        music_state["map_track"] = track.get_sound()

        music_state["mode"] = "once"
        music_state["pool"] = None
        _play_music_track(track, MUSIC_MAP_VOLUME)

    def start_event_music(**kwargs):
        """
        Called by begin_event: a fresh scene or fragment gets the bed unless it is
        already playing. Decision re-entry keeps whatever the scene set up,
        including a deliberate silence.
        """

        if get_kwargs("is_decision_call", False, **kwargs):
            return
        if "bed" in music_pools:
            play_music("bed")

    def play_menu_music():
        track = menu_music["track"]
        if track is None:
            return
        music_state["mode"] = None
        _play_music_track(track, loop = True)

    def _music_tick():
        # config.periodic_callbacks run on the main thread, so the playlist can
        # touch the store; Ren'Py's own loop would give every track the last
        # track's volume, which is why the pool advances here
        if music_state["mode"] not in ("pool", "once"):
            return
        if renpy.music.is_playing(channel = "music"):
            return
        if _music_clock.time() - _music_started[0] < MUSIC_START_GRACE:
            return
        if music_state["mode"] == "once":
            # the map track has run out; the map belongs to its ambience now
            music_state["mode"] = None
            return
        _play_next_pool_track()

    config.periodic_callbacks.append(_music_tick)

    def _restart_music_after_load():
        # a playlist track is not a Ren'Py loop, so a load restores nothing on the
        # music channel; start the next track right away instead of after the grace
        _music_started[0] = 0.0
        if music_state["mode"] == "pool":
            _play_next_pool_track()
        elif music_state["mode"] == "once":
            music_state["mode"] = None

    config.after_load_callbacks.append(_restart_music_after_load)

label before_main_menu:
    $ play_menu_music()
    return

# endregion
#############################
