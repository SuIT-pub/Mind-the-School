init -7 python:
    import re
    from abc import ABC, abstractmethod

    unlockable_manager = None

    class UnlockableScheduleVoteConditions:
        def __init__(self, *conditions: Condition):
            self.conditions = list(conditions)

    class Unlockable(Situation):
        def __init__(
            self,
            type_key: str,
            key: str,
            name: str,
            inject_default_measure: bool,
            *elements: SituationBar | SituationPassive | SituationEventPools | SituationTeaser | SituationThreshold | SituationResolution | SituationDescription | Condition | Effect,
            thumbnail: str = None,
            group_index: int = -1,
            inject_default_cancel: bool = True,
        ):
            self.unlockable_key = key
            self.type_key = type_key
            self.group_index = group_index
            self.conditions = ConditionStorage()
            cleaned_elements = []
            unlock_effects = []
            schedule_vote_conditions = None
            has_bars = False
            for element in elements:
                if isinstance(element, Condition):
                    self.conditions.add_conditions(element)
                elif isinstance(element, UnlockableScheduleVoteConditions):
                    schedule_vote_conditions = list(element.conditions)
                elif isinstance(element, SituationPositiveResolution) or (
                    isinstance(element, SituationResolution) and getattr(element, "key", None) == "positive_resolution"
                ):
                    unlock_effects.extend(list(element.effects.effects))
                elif isinstance(element, Effect):
                    unlock_effects.append(element)
                elif isinstance(element, SituationBar):
                    has_bars = True
                    cleaned_elements.append(element)
                else:
                    cleaned_elements.append(element)

            situation_key = f"{type_key}:{key}"
            if group_index != -1:
                situation_key = f"{type_key}:{key}:{group_index}"

            for effect in unlock_effects:
                Unlockable._attach_money_escrow_option(situation_key, effect)

            vote_measure_conditions = [VoteProposalFreeCondition()]
            if schedule_vote_conditions is not None:
                vote_measure_conditions.extend(schedule_vote_conditions)

            cleaned_elements.insert(0, SituationMeasure(
                name = "Schedule Vote",
                description = "Schedule vote for next Friday.",
                duration = None,
                conditions = vote_measure_conditions,
                instant_effects = [UnlockableScheduleVoteEffect(situation_key)],
                permanent_effects = [],
                open_ended = True,  # hold slot until pta_vote_result
            ))

            # Free default Cancel. Set inject_default_cancel=False to supply a custom
            # Cancel measure (e.g. with reputation cost) via *elements instead.
            if inject_default_cancel:
                cleaned_elements.insert(1, SituationMeasure(
                    name = "Cancel",
                    description = f"Cancel work on {get_translation(key)}.",
                    duration = None,
                    conditions = [],
                    instant_effects = [SituationEffectCancelSituation()],
                    permanent_effects = [],
                ))

            unlock_resolution_effects = [
                UnlockableUnlockEffect(
                    situation_key,
                    group_key = key if group_index != -1 else None,
                    group_index = group_index,
                ),
                *unlock_effects,
            ]
            vote_won = GameDataCondition(situation_key + "_vote_won", True)

            # Unlock as soon as the PTA vote passes. Bars only drive vote probability.
            cleaned_elements.insert(0, ConditionResolution(
                "vote_passed",
                vote_won,
                *unlock_resolution_effects,
            ))
            # Bars at max can still resolve once the vote has also passed.
            cleaned_elements.insert(0, PositiveResolution(
                "ALL",
                *unlock_resolution_effects,
                vote_won,
            ))

            if not has_bars:
                cleaned_elements.append(Bar("Students", limits = (0, 100), regular_decrease_rate = 0.5))
                cleaned_elements.append(Bar("Parents", limits = (0, 100), regular_decrease_rate = 0.5))
                cleaned_elements.append(Bar("Teachers", limits = (0, 100), regular_decrease_rate = 0.5))

            if inject_default_measure:
                cleaned_elements.append(SituationMeasure(
                    name = "Persuade",
                    description = f"Persuade the pta members to vote for the {get_translation(key)}.",
                    duration = None,
                    conditions = [TimerCondition(f"{situation_key}_persuade_cooldown", day = 1)],
                    instant_effects = [SituationEffectBarChangeModifier("ALL", 10, "range_percent", "daytime_change")],
                    permanent_effects = [],
                ))

            elements = tuple(cleaned_elements)

            super().__init__(situation_key, name, *elements, thumbnail=thumbnail)

            # Cheat override: when True, is_visible() returns True regardless of
            # the derived condition state. Runtime-only, survives live reloads
            # (update_data does not sync it).
            self.override_visible = False

        @staticmethod
        def parse_money_condition_amount(value) -> int:
            """
            Extract a numeric escrow amount from a MoneyCondition value.

            Args:
                value: Numeric threshold or comparison string (e.g. ``1500``, ``\"1500+\"``).

            Returns:
                int: Absolute amount to reserve, or ``-1`` when unparsable.
            """
            if isinstance(value, bool):
                return -1
            if isinstance(value, (int, float)):
                return int(value)
            if isinstance(value, str):
                digits = re.sub(r"[^\d]", "", value)
                if digits:
                    return int(digits)
            return -1

        @staticmethod
        def vote_money_stash_key(situation_key: str, effect_name: str) -> str:
            """Build the reserved-money key for a vote-cost MoneyEffect."""
            return f"vote_{situation_key}_{effect_name}"

        @staticmethod
        def _attach_money_escrow_option(situation_key: str, effect: Effect):
            """
            Tag cost MoneyEffects with MoneyEscrowOption for PTA vote stash consume.

            Args:
                situation_key: Unlockable situation key used in the stash key.
                effect: Candidate unlock-resolution effect.
            """
            if not isinstance(effect, MoneyEffect):
                return
            if effect.mode != "ADD" or effect.value >= 0:
                return
            if effect.options.has_option("MoneyEscrow"):
                return
            effect.options.add_option(
                MoneyEscrowOption(Unlockable.vote_money_stash_key(situation_key, effect.name))
            )

        @property
        def level(self):
            return self.group_index

        @property
        def status(self):
            state = self.visibility_state
            if state == "teaser_active":
                return "inactive"
            return state

        def get_title(self):
            """
            Returns the display title for this unlockable.

            Returns:
                str: Group members use their name; others prefer translation.
            """
            if self.group_index != -1:
                return self.name
            title = get_translation(self.unlockable_key)
            if title is None or title == self.unlockable_key:
                return self.name
            return title

        def update_data(self, situation: Situation):
            """
            Sync definition fields from a freshly loaded unlockable template.

            Args:
                situation (Situation): Template situation / unlockable from reload.
            """
            super().update_data(situation)
            if isinstance(situation, Unlockable):
                self.unlockable_key = situation.unlockable_key
                self.type_key = situation.type_key
                self.group_index = situation.group_index
                self.conditions = situation.conditions
            return self

        def run_self_test(self):
            error_messages = super().run_self_test()

            money_conditions = list(self.get_vote_money_conditions())
            money_effects = list(self.get_vote_money_cost_effects())
            unused_effects = list(money_effects)

            for condition in money_conditions:
                amount = Unlockable.parse_money_condition_amount(condition.value)
                if amount < 0:
                    error_messages.append((
                        800,
                        f"MoneyCondition value {condition.value!r} on Schedule Vote is not a usable escrow amount.",
                    ))
                    continue
                match = None
                for effect in unused_effects:
                    if abs(int(effect.value)) == amount:
                        match = effect
                        break
                if match is None:
                    error_messages.append((
                        801,
                        f"MoneyCondition({amount}) on Schedule Vote has no matching cost MoneyEffect.",
                    ))
                else:
                    unused_effects.remove(match)
                    if not match.options.has_option("MoneyEscrow"):
                        error_messages.append((
                            802,
                            f"MoneyEffect({match.name}) missing MoneyEscrowOption for vote stash.",
                        ))

            for effect in unused_effects:
                error_messages.append((
                    803,
                    f"MoneyEffect({effect.name}, {effect.value}) has no matching MoneyCondition on Schedule Vote.",
                ))

            return error_messages

        def get_schedule_vote_measure(self):
            """Return the injected Schedule Vote measure, if present."""
            return self.passives.get("Schedule Vote")

        def release_schedule_vote_measure(self):
            """
            End the Schedule Vote measure after the PTA vote has resolved.

            ``duration`` is None with ``open_ended=True``, so the slot does not
            expire on a timer and does not auto-close after apply. The measure
            stays active from scheduling until this call (win or lose).
            """
            measure = self.get_schedule_vote_measure()
            if measure is None:
                return
            if measure.active or self.active_measure == "Schedule Vote":
                measure.deactivate()

        def get_vote_money_conditions(self) -> list:
            """MoneyConditions on the Schedule Vote measure (escrow source)."""
            measure = self.get_schedule_vote_measure()
            if measure is None:
                return []
            return measure.conditions.find_by_type("money")

        def get_vote_money_cost_effects(self) -> list:
            """ADD cost MoneyEffects on unlock resolutions (escrow consumers)."""
            return [
                effect for effect in self.get_unlock_content_effects()
                if isinstance(effect, MoneyEffect) and effect.mode == "ADD" and effect.value < 0
            ]

        def get_vote_money_escrow_entries(self) -> list:
            """
            Paired Schedule-Vote money costs with their stash keys.

            Each entry is ``(amount, stash_key, money_effect)`` for a MoneyCondition
            matched by absolute value to a cost MoneyEffect.

            Returns:
                list: Escrow entries used by reserve/release.
            """
            entries = []
            unused_effects = list(self.get_vote_money_cost_effects())

            for condition in self.get_vote_money_conditions():
                amount = Unlockable.parse_money_condition_amount(condition.value)
                if amount < 0:
                    continue
                match = None
                for effect in unused_effects:
                    if abs(int(effect.value)) == amount:
                        match = effect
                        break
                if match is None:
                    continue
                unused_effects.remove(match)
                escrow = match.options.get_option("MoneyEscrow")
                stash_key = getattr(escrow, "stash_key", None) if escrow is not None else None
                if not stash_key:
                    stash_key = Unlockable.vote_money_stash_key(self.key, match.name)
                entries.append((amount, stash_key, match))
            return entries

        def reserve_vote_money(self) -> bool:
            """
            Escrow Schedule Vote MoneyCondition amounts into ``reserved_money``.

            Reserves each paired cost under that effect's MoneyEscrow stash key.

            Returns:
                bool: False if any reserve fails (partial reserves are rolled back).
            """
            reserved_keys = []
            for amount, stash_key, _effect in self.get_vote_money_escrow_entries():
                if not reserve_money(stash_key, amount):
                    for key in reserved_keys:
                        release_money(key)
                    return False
                reserved_keys.append(stash_key)
            return True

        def release_vote_money(self):
            """
            Refund PTA vote money still reserved for this unlockable's cost pairs.

            Only releases the concrete MoneyEscrow stash keys from
            ``get_vote_money_escrow_entries`` — never unrelated reservations.
            """
            for _amount, stash_key, _effect in self.get_vote_money_escrow_entries():
                release_money(stash_key)

        def is_visible(self, **kwargs):
            if getattr(self, "override_visible", False):
                return True
            return self.conditions.is_fulfilled(**kwargs)

        def is_unlocked(self, **kwargs):
            return get_game_data(self.key + "_unlocked") is not None

        def get_vote_probability(self):
            """
            Combined fill ratio across all bars on this unlockable.

            Returns:
                float: Value in ``[0, 1]``.
            """
            bar_value = self.get_combined_bar_value()
            bar_max = self.get_combined_bar_max()
            if bar_value <= 0 or bar_max <= 0:
                return 0
            return bar_value / bar_max

        def roll_votes(self):
            """
            Roll one yes/no vote per author-defined bar from that bar's fill ratio.

            Returns:
                list[str]: ``\"yes\"`` / ``\"no\"`` entries, one per bar.
            """
            votes = []
            for bar in self.get_bars():
                if bar.max <= 0:
                    probability = 0.0
                else:
                    probability = clamp_value(bar.value / bar.max, 0, 1)
                votes.append("yes" if renpy.random.random() < probability else "no")
            return votes

        def apply_vote_failure_penalty(self, amount: float = -15):
            """
            Push all bars after a failed PTA vote.

            Args:
                amount (float): Delta applied to every bar (default -15).
            """
            self.change_bar_value("ALL", amount)

        def get_unlock_content_effects(self):
            """
            Effects applied by unlock resolutions, excluding UnlockableUnlockEffect.

            Vote-passed and positive resolutions may share effect instances; results
            are de-duplicated by identity.

            Returns:
                list[Effect]: Content effects to revert on group upgrade.
            """
            seen = set()
            effects = []
            for resolution_key in ("vote_passed", "positive_resolution"):
                resolution = self.resolutions.get(resolution_key)
                if resolution is None:
                    continue
                for effect in resolution.effects.effects:
                    if isinstance(effect, UnlockableUnlockEffect):
                        continue
                    effect_id = id(effect)
                    if effect_id in seen:
                        continue
                    seen.add(effect_id)
                    effects.append(effect)
            return effects

        def revert_unlock_content_effects(self, **kwargs):
            """
            Revert transient unlock effects from this unlockable.

            Permanent effects no-op in ``revert()``. Does not clear the unlocked flag.
            """
            for effect in self.get_unlock_content_effects():
                effect.revert(**kwargs)

        def apply_group_upgrade_transition(self, **kwargs):
            """
            Atomically prepare a group upgrade: revert the previous member's content effects.

            Called from ``UnlockableUnlockEffect`` before this level's effects apply.
            """
            if self.group_index == -1 or unlockable_manager is None:
                return
            previous = unlockable_manager.get_previous_group_member(
                self.unlockable_key,
                self.group_index,
            )
            if previous is None:
                return
            previous.revert_unlock_content_effects(**kwargs)

    class UnlockableScheduleVoteEffect(SituationEffect):
        def __init__(self, situation_key: str):
            super().__init__()
            self.situation_key = situation_key

        @property
        def local_key(self):
            return "unlockable_schedule_vote"

        @property
        def description(self):
            return "Schedules the PTA vote."

        def clone(self):
            return UnlockableScheduleVoteEffect(self.situation_key)

        def update_data(self, other: SituationEffect):
            if isinstance(other, UnlockableScheduleVoteEffect):
                self.situation_key = other.situation_key
            return

        def run_self_test(self):
            return []

        def apply(self, **kwargs):
            key = self.situation_key
            if self.passive is not None and self.passive.situation is not None:
                key = self.passive.situation.key
            if get_game_data("voteProposal") is not None:
                return self
            unlockable = None
            if situation_manager is not None:
                unlockable = situation_manager.get_situation(key)
            if isinstance(unlockable, Unlockable) and not unlockable.reserve_vote_money():
                return self
            ScheduleVoteEffect(key).apply(**kwargs)
            return self

        def revert(self, **kwargs):
            key = self.situation_key
            if self.passive is not None and self.passive.situation is not None:
                key = self.passive.situation.key
            ScheduleVoteEffect(key).revert(**kwargs)
            return self

    class UnlockableManager:
        def __init__(self):
            self.unlockables = {}

        def add_unlockable(self, unlockable: Unlockable):
            """
            Register an unlockable (insert or update) and its situation.

            Args:
                unlockable (Unlockable): Unlockable template to add or sync.
            """
            self.load_unlockable(unlockable)

        def load_unlockable(self, unlockable: Unlockable):
            """
            Load or update an unlockable definition, mirroring SituationManager.load_situation.

            Syncs the situation via SituationManager, then points the manager at the live instance.

            Args:
                unlockable (Unlockable): Fresh template from load_unlockables.
            """
            situation_manager.load_situation(unlockable)
            live = situation_manager._situations.get(unlockable.key, unlockable)
            self._store_live(live)

        def _store_live(self, unlockable: Unlockable):
            """
            Keep the manager map pointing at the live Unlockable instance.

            Args:
                unlockable (Unlockable): Live instance stored in situation_manager.
            """
            if not isinstance(unlockable, Unlockable):
                return
            if unlockable.group_index != -1:
                members = self.unlockables.get(unlockable.unlockable_key)
                if members is None or isinstance(members, Unlockable):
                    members = []
                    self.unlockables[unlockable.unlockable_key] = members
                replaced = False
                for i, member in enumerate(members):
                    if member.group_index == unlockable.group_index:
                        members[i] = unlockable
                        replaced = True
                        break
                if not replaced:
                    members.append(unlockable)
                members.sort(key=lambda x: x.level)
            else:
                self.unlockables[unlockable.unlockable_key] = unlockable

        def get_current_level_of_unlockable(self, unlockable_key: str):
            return get_game_data(unlockable_key + "_level")

        def run_unlockables_test(self):
            error_messages = []
            for unlockable_key in self.unlockables.keys():
                if not self.group_has_consecutive_levels(unlockable_key):
                    error_messages.append(f"Group {unlockable_key} has non-consecutive levels")
                    for unlockable in self.get_unlockables_by_key(unlockable_key):
                        situation_manager.invalidate_situation(unlockable)
            return error_messages

        def group_has_consecutive_levels(self, unlockable_key):
            """
            Check if all unlockables in the given group have consecutive levels.

            Levels may start at any index (e.g. 3..10) but must have no gaps.

            Args:
                unlockable_key (str): Group / unlockable key.

            Returns:
                bool: True if levels are consecutive, or the entry is not a group.
            """
            members = self.get_unlockables_by_key(unlockable_key)
            if not members:
                return False
            if len(members) == 1 and members[0].group_index == -1:
                return True
            levels = sorted(unlockable.level for unlockable in members)
            if not levels:
                return False
            return levels == list(range(levels[0], levels[0] + len(levels)))

        def apply_group_chain_conditions(self):
            """
            Auto-insert GameDataConditions so later group members require the previous level.
            """
            for unlockable_key in list(self.unlockables.keys()):
                members = self.get_unlockables_by_key(unlockable_key)
                if len(members) <= 1:
                    continue
                if members[0].group_index == -1:
                    continue
                members = sorted(members, key=lambda member: member.level)
                level_data_key = unlockable_key + "_level"
                for i, member in enumerate(members):
                    if i == 0:
                        continue
                    prev_level = members[i - 1].group_index
                    already = False
                    for condition in member.conditions.get_conditions():
                        if getattr(condition, "type", None) == "game_data" and getattr(condition, "key", None) == level_data_key:
                            already = True
                            break
                    if not already:
                        member.conditions.add_conditions(GameDataCondition(level_data_key, prev_level))

        def get_current_unlockables(self):
            unlockables = []
            for unlockable_key in self.unlockables.keys():
                unlockables.append(self.get_default_member(unlockable_key))
            return [u for u in unlockables if u is not None]

        def get_current_unlockable_by_key(self, key: str):
            return self.get_default_member(key)

        def get_unlockables_by_key(self, key: str):
            """
            Return all unlockables for a key as a list.

            Args:
                key (str): Unlockable key (group key).

            Returns:
                list[Unlockable]: Members for the key, or empty list if missing.
            """
            unlockable = self.unlockables.get(key)
            if unlockable is None:
                return []
            if isinstance(unlockable, Unlockable):
                return [unlockable]
            return list(unlockable)

        def get_unlockable_by_key(self, key: str, index: int = -1):
            """
            Look up an unlockable by key and optional group index.

            Args:
                key (str): Unlockable key.
                index (int): Group index. -1 returns the sole member or default member.

            Returns:
                Unlockable | None: Matching unlockable, or None.
            """
            members = self.get_unlockables_by_key(key)
            if not members:
                return None
            if len(members) == 1 and members[0].group_index == -1:
                return members[0]
            if index == -1:
                return self.get_default_member(key)
            for member in members:
                if member.group_index == index:
                    return member
            return None

        def get_group_member(self, unlockable_key: str, index: int):
            """
            Get a specific group member by index.

            Args:
                unlockable_key (str): Group key.
                index (int): group_index to find.

            Returns:
                Unlockable | None: Matching member, or None.
            """
            return self.get_unlockable_by_key(unlockable_key, index)

        def get_previous_group_member(self, unlockable_key: str, group_index: int):
            """
            Return the group member with the highest index below ``group_index``.

            Args:
                unlockable_key (str): Group key.
                group_index (int): Current member's group index.

            Returns:
                Unlockable | None: Previous chain member, or None if this is the first.
            """
            previous_members = [
                member
                for member in self.get_unlockables_by_key(unlockable_key)
                if member.group_index != -1 and member.group_index < group_index
            ]
            if not previous_members:
                return None
            return max(previous_members, key=lambda member: member.group_index)

        def get_default_member(self, unlockable_key: str):
            """
            Pick the unlockable shown by default for a list key.

            Smallest incomplete (not unlocked) index; if all unlocked, the highest index.
            A cheat force-visible (override_visible) member takes precedence.

            Args:
                unlockable_key (str): Unlockable / group key.

            Returns:
                Unlockable | None: Default member.
            """
            members = self.get_unlockables_by_key(unlockable_key)
            if not members:
                return None
            if len(members) == 1 and members[0].group_index == -1:
                return members[0]
            # Cheat override: a force-visible member takes precedence so it can be
            # surfaced and inspected even when its group predecessor is not unlocked.
            override_members = [m for m in members if getattr(m, "override_visible", False)]
            if override_members:
                for member in override_members:
                    if not member.is_unlocked():
                        return member
                return override_members[-1]
            for member in members:
                if not member.is_unlocked():
                    return member
            return members[-1]

        def get_navigable_indices(self, unlockable_key: str):
            """
            Indices the detail view may step through for a group.

            Includes all unlocked members plus the lowest incomplete member, and any
            cheat force-visible (override_visible) members.

            Args:
                unlockable_key (str): Group key.

            Returns:
                list[int]: Sorted navigable group indices. Empty for non-groups.
            """
            members = self.get_unlockables_by_key(unlockable_key)
            if not members:
                return []
            if len(members) == 1 and members[0].group_index == -1:
                return []
            # Cheat override: force-visible members are always navigable, even when
            # their group predecessor is not unlocked yet.
            indices = [m.group_index for m in members if m.is_unlocked() or getattr(m, "override_visible", False)]
            for member in members:
                if not member.is_unlocked():
                    if member.group_index not in indices:
                        indices.append(member.group_index)
                    break
            return sorted(indices)

        def get_type_keys(self):
            """
            Collect unique type_keys from registered unlockables.

            Returns:
                list[str]: Sorted type_key values.
            """
            type_keys = set()
            for unlockable_key in self.unlockables.keys():
                members = self.get_unlockables_by_key(unlockable_key)
                if members:
                    type_keys.add(members[0].type_key)
            return sorted(type_keys)

        def parse_display(self, display: str):
            """
            Split a journal display string into unlockable key and optional view index.

            Args:
                display (str): ``key`` or ``key:view_index``.

            Returns:
                tuple[str, int | None]: (unlockable_key, view_index or None).
            """
            if display is None or display == "":
                return ("", None)
            if ":" not in display:
                return (display, None)
            key, index_str = display.rsplit(":", 1)
            if index_str.isdigit() or (index_str.startswith("-") and index_str[1:].isdigit()):
                return (key, int(index_str))
            return (display, None)

        def resolve_display(self, display: str):
            """
            Resolve a journal display value to a concrete Unlockable.

            Args:
                display (str): ``key`` or ``key:view_index``.

            Returns:
                Unlockable | None: Resolved unlockable, or None if missing/invalid.
            """
            unlockable_key, view_index = self.parse_display(display)
            if unlockable_key == "":
                return None
            if view_index is not None:
                target = self.get_group_member(unlockable_key, view_index)
            else:
                target = self.get_default_member(unlockable_key)
            if target is None or getattr(target, "invalid", False):
                return None
            return target

        def get_list_entries(self, type_filter: str = ""):
            """
            Build incomplete and completed journal list entries.

            One row per unlockable_key. Visibility uses the default member's conditions.
            Invalid / orphaned unlockables (missing definition) are skipped.

            Args:
                type_filter (str): If set, only include this type_key. Empty = all.

            Returns:
                tuple[list[tuple[str, str]], list[tuple[str, str]]]:
                    (incomplete, completed) as (title, unlockable_key) pairs.
            """
            incomplete = []
            completed = []
            for unlockable_key in sorted(self.unlockables.keys()):
                members = self.get_unlockables_by_key(unlockable_key)
                if not members:
                    continue
                if type_filter and members[0].type_key != type_filter:
                    continue
                target = self.get_default_member(unlockable_key)
                if target is None or getattr(target, "invalid", False) or not target.is_visible():
                    continue
                title = target.get_title()
                if target.is_unlocked():
                    completed.append((title, unlockable_key))
                else:
                    incomplete.append((title, unlockable_key))
            return (incomplete, completed)

        def build_display(self, unlockable_key: str, view_index: int = None):
            """
            Build a journal display string for an unlockable selection.

            Args:
                unlockable_key (str): Unlockable key.
                view_index (int | None): Optional group index to pin.

            Returns:
                str: Display value for open_journal.
            """
            if view_index is None:
                return unlockable_key
            return f"{unlockable_key}:{view_index}"

    def register_unlockables(*unlockables: Unlockable):
        """
        Load or update unlockable templates. Call from label load_unlockables.

        Args:
            *unlockables (Unlockable): Unlockable definitions to register.
        """
        global unlockable_manager
        if unlockable_manager is None:
            unlockable_manager = UnlockableManager()
        # Gated on the current mod being active (like event `add_event`): a disabled
        # mod's unlockables are not registered.
        if is_mod_active(active_mod_key):
            for unlockable in unlockables:
                unlockable_manager.load_unlockable(unlockable)
            unlockable_manager.apply_group_chain_conditions()
            unlockable_manager.run_unlockables_test()

    def is_unlockable_unlocked(key: str, index: int = -1) -> bool:
        """
        Return whether an unlockable is unlocked.

        Args:
            key (str): Unlockable key (group key).
            index (int): Optional group index. ``-1`` uses the default member.

        Returns:
            bool: True if the unlockable exists and is unlocked.
        """
        if unlockable_manager is None:
            return False
        unlockable = unlockable_manager.get_unlockable_by_key(key, index)
        return unlockable is not None and unlockable.is_unlocked()

    unlockable_manager = UnlockableManager()


###############################################
# region LEGACY Rule / Club save stubs -------- #
###############################################

init -6 python:
    from deprecated import deprecated

    # Full definitions archived under journal/legacy_definitions_archive/.
    # These classes exist only so old saves can unpickle.

    @deprecated(version='0.2.3', reason="Replaced by Unlockable(type_key='rule'); kept for save compatibility.")
    class Rule(Journal_Obj):
        """Legacy journal rule. Kept so existing saves can unpickle."""

        def __init__(self, name: str = "", title: str = ""):
            super().__init__(name, title)
            self._unlocked = False

        def get_type(self) -> str:
            return "rule"

    @deprecated(version='0.2.3', reason="Replaced by Unlockable(type_key='club'); kept for save compatibility.")
    class Club(Journal_Obj):
        """Legacy journal club. Kept so existing saves can unpickle."""

        def __init__(self, name: str = "", title: str = ""):
            super().__init__(name, title)
            self._unlocked = False

        def get_type(self) -> str:
            return "club"

    def clean_legacy_journal_objects():
        """
        Drop legacy Rule/Club entries and obsolete journal buildings from the save.

        Map buildings live on ``building_manager``. Unlock state lives on Unlockables.
        """
        global rules, clubs, buildings
        rules = {}
        clubs = {}
        buildings = {}

# endregion
###############################################

#######################
# region LABELS ----- #
#######################

label load_unlockables:
    $ set_current_mod('base')

    if not unlockable_manager:
        $ unlockable_manager = UnlockableManager()

    if not situation_manager:
        $ situation_manager = SituationManager()

    # Temporary school-level progress group (mirrors old level_3..level_10 rules).
    # One journal list entry ("level"); group_index matches the target school level.
    $ register_unlockables(
        Unlockable("rule", "level", "Level 3", True,
            SituationDescription([
                "!!! THIS IS A TEMPORARY UNLOCKABLE. IT WILL BE REMOVED IN THE FUTURE !!!",
                "!!! It is highly recommended to save the game and back it up before unlocking this. !!!",
                "Progress the school to level 3.",
                "This unlockable is only temporary to allow players to progress the school to higher levels.",
                "This will be removed in the future and replaced by proper level transition events.",
                "Not all events are available at higher levels.",
            ]),
            LevelCondition("2"),
            LevelEffect("set_school_level_3", 3, "SET", "school"),
            LevelEffect("set_parent_level_3", 3, "SET", "parent"),
            LevelEffect("set_teacher_level_3", 3, "SET", "teacher"),
            LevelEffect("set_secretary_level_7", 7, "SET", "secretary"),
            Picto("teachers"),
            Picto("parents"),
            Picto("students"),
            Picto("vote"),
            Picto("dresscode"),
            thumbnail="images/journal/rules/level_3.webp",
            group_index=3,
        ),
        Unlockable("rule", "level", "Level 4", True,
            SituationDescription([
                "!!! THIS IS A TEMPORARY UNLOCKABLE. IT WILL BE REMOVED IN THE FUTURE !!!",
                "!!! It is highly recommended to save the game and back it up before unlocking this. !!!",
                "Progress the school to level 4.",
                "This unlockable is only temporary to allow players to progress the school to higher levels.",
                "This will be removed in the future and replaced by proper level transition events.",
                "Not all events are available at higher levels.",
            ]),
            LevelEffect("set_school_level_4", 4, "SET", "school"),
            LevelEffect("set_parent_level_4", 4, "SET", "parent"),
            LevelEffect("set_teacher_level_4", 4, "SET", "teacher"),
            LevelEffect("set_secretary_level_8", 8, "SET", "secretary"),
            Picto("teachers"),
            Picto("parents"),
            Picto("students"),
            Picto("vote"),
            Picto("dresscode"),
            thumbnail="images/journal/rules/level_4.webp",
            group_index=4,
        ),
        Unlockable("rule", "level", "Level 5", True,
            SituationDescription([
                "!!! THIS IS A TEMPORARY UNLOCKABLE. IT WILL BE REMOVED IN THE FUTURE !!!",
                "!!! It is highly recommended to save the game and back it up before unlocking this. !!!",
                "Progress the school to level 5.",
                "This unlockable is only temporary to allow players to progress the school to higher levels.",
                "This will be removed in the future and replaced by proper level transition events.",
                "Not all events are available at higher levels.",
            ]),
            LevelEffect("set_school_level_5", 5, "SET", "school"),
            LevelEffect("set_parent_level_5", 5, "SET", "parent"),
            LevelEffect("set_teacher_level_5", 5, "SET", "teacher"),
            LevelEffect("set_secretary_level_9", 9, "SET", "secretary"),
            Picto("teachers"),
            Picto("parents"),
            Picto("students"),
            Picto("vote"),
            Picto("dresscode"),
            thumbnail="images/journal/rules/level_5.webp",
            group_index=5,
        ),
        Unlockable("rule", "level", "Level 6", True,
            SituationDescription([
                "!!! THIS IS A TEMPORARY UNLOCKABLE. IT WILL BE REMOVED IN THE FUTURE !!!",
                "!!! It is highly recommended to save the game and back it up before unlocking this. !!!",
                "Progress the school to level 6.",
                "This unlockable is only temporary to allow players to progress the school to higher levels.",
                "This will be removed in the future and replaced by proper level transition events.",
                "Not all events are available at higher levels.",
            ]),
            LevelEffect("set_school_level_6", 6, "SET", "school"),
            LevelEffect("set_parent_level_6", 6, "SET", "parent"),
            LevelEffect("set_teacher_level_6", 6, "SET", "teacher"),
            LevelEffect("set_secretary_level_10", 10, "SET", "secretary"),
            Picto("teachers"),
            Picto("parents"),
            Picto("students"),
            Picto("vote"),
            Picto("dresscode"),
            thumbnail="images/journal/rules/level_6.webp",
            group_index=6,
        ),
        Unlockable("rule", "level", "Level 7", True,
            SituationDescription([
                "!!! THIS IS A TEMPORARY UNLOCKABLE. IT WILL BE REMOVED IN THE FUTURE !!!",
                "!!! It is highly recommended to save the game and back it up before unlocking this. !!!",
                "Progress the school to level 7.",
                "This unlockable is only temporary to allow players to progress the school to higher levels.",
                "This will be removed in the future and replaced by proper level transition events.",
                "Not all events are available at higher levels.",
            ]),
            LevelEffect("set_school_level_7", 7, "SET", "school"),
            LevelEffect("set_parent_level_7", 7, "SET", "parent"),
            LevelEffect("set_teacher_level_7", 7, "SET", "teacher"),
            LevelEffect("set_secretary_level_10", 10, "SET", "secretary"),
            Picto("teachers"),
            Picto("parents"),
            Picto("students"),
            Picto("vote"),
            Picto("dresscode"),
            thumbnail="images/journal/rules/level_7.webp",
            group_index=7,
        ),
        Unlockable("rule", "level", "Level 8", True,
            SituationDescription([
                "!!! THIS IS A TEMPORARY UNLOCKABLE. IT WILL BE REMOVED IN THE FUTURE !!!",
                "!!! It is highly recommended to save the game and back it up before unlocking this. !!!",
                "Progress the school to level 8.",
                "This unlockable is only temporary to allow players to progress the school to higher levels.",
                "This will be removed in the future and replaced by proper level transition events.",
                "Not all events are available at higher levels.",
            ]),
            LevelEffect("set_school_level_8", 8, "SET", "school"),
            LevelEffect("set_parent_level_8", 8, "SET", "parent"),
            LevelEffect("set_teacher_level_8", 8, "SET", "teacher"),
            LevelEffect("set_secretary_level_10", 10, "SET", "secretary"),
            Picto("teachers"),
            Picto("parents"),
            Picto("students"),
            Picto("vote"),
            Picto("dresscode"),
            thumbnail="images/journal/rules/level_8.webp",
            group_index=8,
        ),
        Unlockable("rule", "level", "Level 9", True,
            SituationDescription([
                "!!! THIS IS A TEMPORARY UNLOCKABLE. IT WILL BE REMOVED IN THE FUTURE !!!",
                "!!! It is highly recommended to save the game and back it up before unlocking this. !!!",
                "Progress the school to level 9.",
                "This unlockable is only temporary to allow players to progress the school to higher levels.",
                "This will be removed in the future and replaced by proper level transition events.",
                "Not all events are available at higher levels.",
            ]),
            LevelEffect("set_school_level_9", 9, "SET", "school"),
            LevelEffect("set_parent_level_9", 9, "SET", "parent"),
            LevelEffect("set_teacher_level_9", 9, "SET", "teacher"),
            LevelEffect("set_secretary_level_10", 10, "SET", "secretary"),
            Picto("teachers"),
            Picto("parents"),
            Picto("students"),
            Picto("vote"),
            Picto("dresscode"),
            thumbnail="images/journal/rules/level_9.webp",
            group_index=9,
        ),
        Unlockable("rule", "level", "Level 10", True,
            SituationDescription([
                "!!! THIS IS A TEMPORARY UNLOCKABLE. IT WILL BE REMOVED IN THE FUTURE !!!",
                "!!! It is highly recommended to save the game and back it up before unlocking this. !!!",
                "Progress the school to level 10.",
                "This unlockable is only temporary to allow players to progress the school to higher levels.",
                "This will be removed in the future and replaced by proper level transition events.",
                "Not all events are available at higher levels.",
            ]),
            LevelEffect("set_school_level_10", 10, "SET", "school"),
            LevelEffect("set_parent_level_10", 10, "SET", "parent"),
            LevelEffect("set_teacher_level_10", 10, "SET", "teacher"),
            LevelEffect("set_secretary_level_10", 10, "SET", "secretary"),
            Picto("teachers"),
            Picto("parents"),
            Picto("students"),
            Picto("vote"),
            Picto("dresscode"),
            thumbnail="images/journal/rules/level_10.webp",
            group_index=10,
        ),
    )

# endregion
#######################
