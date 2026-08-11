init -100 python:
    """
    Global lifecycle registry for persistent resources (modifiers, threshold checks).

    Origins track resources they create. During an init/reload check wave they
    ping KEEP / HIBERNATE / UPGRADE / REMOVE. Unpinged entries are swept only
    in finalize_check after all systems have finished their load pass.
    """

    KEEP = "keep"
    HIBERNATE = "hibernate"
    UPGRADE = "upgrade"
    REMOVE = "remove"

    LIFECYCLE_ACTIVE = "active"
    LIFECYCLE_HIBERNATED = "hibernated"

    class LifecycleEntry:
        """
        Serializable ownership record for one tracked resource.

        Attributes:
            key (str): Globally unique resource key.
            owner (str): System id (e.g. \"situations\").
            category (str): Instance id within the system.
            kind (str): Handler kind (e.g. \"modifier\").
            data (dict): Kind-specific serializable payload.
            state (str): LIFECYCLE_ACTIVE or LIFECYCLE_HIBERNATED.
        """

        def __init__(self, key, owner, category, kind, data=None, state=LIFECYCLE_ACTIVE):
            self.key = key
            self.owner = owner
            self.category = category
            self.kind = kind
            self.data = dict(data or {})
            self.state = state

    class LifecycleRegistry:
        """
        Store-backed registry with finalize-only ghost sweep.

        known_systems persists across saves (learned via track/ping/end_check).
        end_check only records that a system finished; _sweep runs solely in
        finalize_check so a missing/deactivated system cannot block cleanup.
        """

        def __init__(self):
            self.entries = {}
            self.known_systems = set()
            self.expected = set()
            self.done = set()
            self._pinged = set()
            self._checking = False
            self._wave_started = False
            self._swept = False

        def _remember_owner(self, owner):
            if owner is None:
                return
            self.known_systems.add(owner)
            if self._checking:
                self.expected.add(owner)

        def _forget_owner(self, owner):
            if owner is None:
                return
            self.known_systems.discard(owner)

        def _mark_pinged(self, key):
            if self._checking:
                self._pinged.add(key)

        def _remove_resource(self, entry):
            """Run kind handler remove from serializable meta."""
            if entry.kind == "modifier":
                remove_modifier(
                    entry.key,
                    stat=entry.data.get("stat", "all"),
                    collection=entry.data.get("collection", "default"),
                )
            elif entry.kind == "threshold_check":
                if situation_manager is not None and entry.key in situation_manager.threshold_checks:
                    del situation_manager.threshold_checks[entry.key]
                remove_timer(entry.key)

        def _resume_resource(self, entry):
            """
            Recreate resource from stored meta (HIBERNATED → ACTIVE).

            Returns:
                bool: False if the entry should be dropped (missing threshold).
                    True on success.
            """
            if entry.kind == "modifier":
                op = entry.data.get("op", entry.data.get("mod_type", "+"))
                value = entry.data.get("value", 0)
                set_modifier(
                    entry.key,
                    Modifier_Obj(entry.key, op, value),
                    stat=entry.data.get("stat", "all"),
                    collection=entry.data.get("collection", "default"),
                )
                return True

            if entry.kind == "threshold_check":
                # Dict/timer only — do not track; KEEP holds this entry reference.
                if situation_manager is None:
                    return False
                situation = situation_manager._situations.get(entry.category)
                if situation is None:
                    return False
                threshold = situation.thresholds.get(entry.key)
                if threshold is None:
                    return False
                situation_manager.threshold_checks[entry.key] = threshold
                if threshold.timed_release is not None:
                    threshold.timed_release.id = entry.key
                    set_timer(entry.key, "now")
                return True

            return True

        def track(self, key, owner, category, kind, **data):
            """
            Record a resource after it was applied.

            Args:
                key (str): Globally unique resource key.
                owner (str): System id.
                category (str): Instance id within the system.
                kind (str): Handler kind.
                **data: Kind payload (modifier: stat, collection, op, value).
            """
            self._remember_owner(owner)
            self.entries[key] = LifecycleEntry(
                key, owner, category, kind, data, LIFECYCLE_ACTIVE
            )
            self._mark_pinged(key)
            return self

        def ping(self, key, status, apply=None, owner=None, category=None, kind=None, **data):
            """
            Healthcheck ping for a tracked key.

            Args:
                key (str): Resource key.
                status (str): KEEP, HIBERNATE, UPGRADE, or REMOVE.
                apply (callable | None): Recreate callback for UPGRADE / optional KEEP resume.
                owner, category, kind, **data: Optional meta updates when tracking anew.
            """
            entry = self.entries.get(key)

            if status == REMOVE:
                if entry is not None:
                    self._remove_resource(entry)
                    del self.entries[key]
                self._pinged.discard(key)
                return self

            if owner is not None:
                self._remember_owner(owner)

            if status == KEEP:
                if entry is None:
                    if owner is not None and kind is not None:
                        self.track(key, owner, category, kind, **data)
                        entry = self.entries.get(key)
                    else:
                        return self
                if entry.state == LIFECYCLE_HIBERNATED:
                    if apply is not None:
                        apply()
                        if data:
                            entry.data.update(data)
                        entry.state = LIFECYCLE_ACTIVE
                    else:
                        if self._resume_resource(entry) is False:
                            # Missing definition resource — drop instead of reviving.
                            return self.ping(key, REMOVE)
                        entry.state = LIFECYCLE_ACTIVE
                self._mark_pinged(key)
                return self

            if status == HIBERNATE:
                if entry is None:
                    if owner is not None and kind is not None:
                        self.entries[key] = LifecycleEntry(
                            key, owner, category, kind, data, LIFECYCLE_HIBERNATED
                        )
                        entry = self.entries[key]
                        self._remove_resource(entry)
                    self._mark_pinged(key)
                    return self
                if entry.state != LIFECYCLE_HIBERNATED:
                    self._remove_resource(entry)
                    entry.state = LIFECYCLE_HIBERNATED
                self._mark_pinged(key)
                return self

            if status == UPGRADE:
                if entry is not None:
                    self._remove_resource(entry)
                if apply is not None:
                    apply()
                if owner is not None and kind is not None:
                    self.track(key, owner, category, kind, **data)
                elif entry is not None:
                    entry.state = LIFECYCLE_ACTIVE
                    if data:
                        entry.data.update(data)
                    self._mark_pinged(key)
                return self

            return self

        def hibernate_category(self, owner, category):
            """
            Hibernate every entry for an owner/category pair.

            Args:
                owner (str): System id.
                category (str): Instance id.
            """
            self._remember_owner(owner)
            for key, entry in list(self.entries.items()):
                if entry.owner == owner and entry.category == category:
                    self.ping(key, HIBERNATE)
            return self

        def resume_category(self, owner, category):
            """
            Resume every hibernated entry for an owner/category pair.

            Iterates a copy of entries so REMOVE during a failed resume cannot
            mutate the dict under iteration.

            Args:
                owner (str): System id.
                category (str): Instance id.
            """
            self._remember_owner(owner)
            for key, entry in list(self.entries.items()):
                if entry.owner == owner and entry.category == category:
                    if entry.state == LIFECYCLE_HIBERNATED:
                        self.ping(key, KEEP)
            return self

        def begin_check(self):
            """Start an init/reload check wave."""
            self._wave_started = True
            self._checking = True
            self._swept = False
            self._pinged = set()
            self.done = set()
            self.expected = set(self.known_systems)
            return self

        def end_check(self, system):
            """
            Mark a system finished for this wave.

            Does not sweep — ghost cleanup runs only in finalize_check.

            Args:
                system (str): System id (e.g. \"situations\").
            """
            self.done.add(system)
            self.known_systems.add(system)
            if self._checking:
                self.expected.add(system)
            return self

        def finalize_check(self):
            """
            End the check wave and remove unpinged ghosts.

            Must be called once after all systems have loaded (and called
            end_check). This is the only path that runs the sweep.
            """
            if self._wave_started and not self._swept:
                self._sweep()
            self._checking = False
            self._wave_started = False
            return self

        def _sweep(self):
            if self._swept or not self._wave_started:
                return self
            for key in list(self.entries.keys()):
                if key not in self._pinged:
                    entry = self.entries.pop(key)
                    self._remove_resource(entry)
            self._swept = True
            self._checking = False
            return self

        def clear(self, owner=None, category=None):
            """
            Remove tracked resources immediately.

            Args:
                owner (str | None): Limit to system. None = all.
                category (str | None): Limit to instance (requires owner).
            """
            for key, entry in list(self.entries.items()):
                if owner is not None and entry.owner != owner:
                    continue
                if category is not None and entry.category != category:
                    continue
                self._remove_resource(entry)
                del self.entries[key]
                self._pinged.discard(key)
            return self

        def has(self, key):
            return key in self.entries

        def get(self, key):
            return self.entries.get(key)

default lifecycle_registry = LifecycleRegistry()
