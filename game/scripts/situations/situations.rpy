init python:
    
    situation_manager = None

init -99 python:
    
    class SituationTeaser:
        def __init__(self, key: str, teaser: str, *conditions: Condition):
            self.key = key
            self.teaser = teaser
            self.conditions = ConditionStorage(*conditions)
            self.active = False
            self.values = {}
            self.text = self.teaser
            self.activation_order = -1

            self.situation = None
        
        def update_data(self, teaser: SituationTeaser):
            self.key = teaser.key
            self.teaser = teaser.teaser
            self.conditions = teaser.conditions
            if not hasattr(self, 'activation_order'):
                self.activation_order = -1
            if self.active:
                self.text = interpolate_string(self.teaser, **self.values)

        def __str__(self):
            return "situation_teaser:" + self.situation.key + ":" + self.key

        def check_conditions(self, **kwargs):
            return self.conditions.is_fulfilled(**kwargs)

        def activate(self, **kwargs):
            self.active = True
            if self.situation is not None:
                # Count how many teasers are already active (excluding this one, since self.active just set to True)
                order = 0
                for teaser in self.situation.teasers.values():
                    if teaser is not self and teaser.active:
                        order += 1
                self.activation_order = order
       
            interpolation_keys = get_interpoaltion_keys(self.teaser)
            for key in interpolation_keys:
                if key in kwargs.keys():
                    self.values[key] = kwargs[key]
            self.text = interpolate_string(self.teaser, **self.values)
            return self




    class SituationThreshold:
        def __init__(self, threshold: int, approach_hint: str, threshold_hint: str, direction: int = 1, *elements: Condition | Effect, thumbnail: str = None):
            self.threshold = threshold
            self.approach_hint = approach_hint
            self.threshold_hint = threshold_hint
            self.direction = direction
            self.blocking = ConditionStorage()
            self.effects = []
            self.reached = False
            self.bar = None
            self.thumbnail = thumbnail

            for element in elements:
                if isinstance(element, Condition):
                    self.add_blocking(element)
                elif isinstance(element, Effect):
                    self.add_effect(element)

        @property
        def key(self):
            if self.bar is None or self.bar.situation is None:
                return str(self.threshold)
            return "situation:" + self.bar.situation.key + ":" + self.bar.key + ":" + str(self.threshold)

        def update_data(self, threshold: SituationThreshold):
            self.threshold = threshold.threshold
            self.approach_hint = threshold.approach_hint
            self.threshold_hint = threshold.threshold_hint
            self.direction = threshold.direction
            self.blocking = threshold.blocking
            self.effects = threshold.effects
            return self

        def add_blocking(self, *blocking: Condition):
            self.blocking.add_conditions(*blocking)
            return self

        def add_effect(self, *effects: Effect):
            self.effects.extend(effects)
            return self

        def trigger_threshold(self):
            if self.reached:
                return

            if len(self.blocking) > 0:
                situation_manager.add_threshold_check(self)
            else:
                self.reached = True
                self.trigger_effects()
            return

        def trigger_effects(self):
            for effect in self.effects:
                effect.apply()

    class SituationPassive:
        def __init__(self, name: str, description: str, *effects: Effect):
            self.name = name
            self.description = description
            self.effects = list(effects)
            self.situation = None

        def update_data(self, passive: SituationPassive):
            self.name = passive.name
            self.description = passive.description
            self.effects = passive.effects
            return self

        def add_effect(self, *effects: Effect):
            self.effects.extend(effects)
            return self

        def run_effects(self):
            for effect in self.effects:
                effect.apply()

        def revert_effects(self):
            for effect in self.effects:
                effect.revert()

    class SituationBar:
        def __init__(self, key: str, *thresholds: SituationThreshold):
            self.key = key

            self.min = -100
            self.max = 100
            self.value = 0
            
            self.thresholds = {}

            self.stat_weights = {}

            self.tendency = 0
            self.changes = [] # last 5 bar changes

            self.situation = None
            
            for threshold in thresholds:
                self.add_threshold(threshold)

        
        def update_data(self, bar: SituationBar):
            self.key = bar.key
            self.min = bar.min
            self.max = bar.max
            self.stat_weights = bar.stat_weights
            # Sync thresholds with bar's thresholds
            new_keys = set(bar.thresholds.keys())
            old_keys = set(self.thresholds.keys())
            
            # Update existing thresholds and add new ones
            for key in new_keys:
                if key in self.thresholds:
                    self.thresholds[key].update_data(bar.thresholds[key])
                else:
                    self.add_threshold(bar.thresholds[key])
            
            # Remove thresholds that are no longer present in bar
            for key in list(self.thresholds.keys()):
                if key not in new_keys:
                    del self.thresholds[key]

            return self

        def __str__(self):
            return "situation:" + self.situation.key + ":" + self.key

        def load_start_value(self):
            # logik wie man den startwert laden soll
            pass

        def add_stat_weight(self, stat: str, weight: int):
            self.stat_weights[stat] = weight
            return self

        def add_threshold(self, threshold: SituationThreshold):
            threshold.bar = self
            self.thresholds[threshold.key] = threshold
            return self

        def reindex_thresholds(self):
            thresholds = list(self.thresholds.values())
            self.thresholds = {}
            for threshold in thresholds:
                self.add_threshold(threshold)
            return self
        
        def set_limits(self, min: int, max: int):
            self.min = min
            self.max = max
            return self

        def get_next_threshold(self, value: float, direction: int = 1, include_reached: bool = False):
            current_threshold = None
            for threshold in self.thresholds.values():
                if (threshold.direction == 1 and direction > 0) or (threshold.direction == -1 and direction < 0):
                    if direction > 0 and threshold.threshold >= value and (current_threshold == None or threshold.threshold < current_threshold.threshold) and (include_reached or not threshold.reached):
                        current_threshold = threshold
                    elif direction < 0 and threshold.threshold <= value and (current_threshold == None or threshold.threshold > current_threshold.threshold) and (include_reached or not threshold.reached):
                        current_threshold = threshold
            return current_threshold

        def apply_progress_change(self, value: float):
            out_value = 0
            remainder = value
            out_blocked = False

            while remainder != 0:
                out_value, remainder, out_blocked = self.clamp_progress_change(remainder)
                self.value += out_value
                if out_blocked:
                    break

            self.changes.append(out_value)
            if len(self.changes) > 5:
                self.changes.pop(0)
            self.tendency = sum(self.changes) / len(self.changes)

        def get_current_thumbnail(self):
            thumbnail_out = None
            threshold = self.get_next_threshold(self.value, self.tendency)
            if threshold is None:
                threshold = self.get_next_threshold(self.value, -self.tendency)
            if threshold is not None:
                thumbnail_out = threshold.thumbnail
            return thumbnail_out

        def clamp_progress_change(self, value: float, clamp_threshold: bool = True):
            out_value = value
            out_blocked = False
            next_threshold = None

            new_value = self.value + value

            if clamp_threshold:
                next_threshold = self.get_next_threshold(self.value, value)
            if next_threshold == None:
                if value > 0 and new_value > self.max:
                    out_value = self.max - self.value
                    out_blocked = True
                elif value < 0 and new_value < self.min:
                    out_value = self.min - self.value
                    out_blocked = True
            else:
                if value > 0 and new_value >= next_threshold.threshold and self.value <= next_threshold.threshold:
                    out_value = next_threshold.threshold - self.value
                    next_threshold.trigger_threshold()
                    if len(next_threshold.blocking) > 0:
                        out_blocked = True
                elif value < 0 and new_value <= next_threshold.threshold and self.value >= next_threshold.threshold:
                    out_value = next_threshold.threshold - self.value
                    next_threshold.trigger_threshold()
                    if len(next_threshold.blocking) > 0:
                        out_blocked = True

            remainder = value - out_value
            if out_blocked:
                remainder = 0

            return out_value, remainder, out_blocked


    class SituationEventPools:
        def __init__(self, key: str, min: int, max: int):
            self.key = key
            self.min = min
            self.max = max
            self.situation = None

        def __str__(self):
            return "situation_pool:" + self.situation.key + ":" + self.key

        def update_data(self, pool: SituationEventPools):
            self.key = pool.key
            self.min = pool.min
            self.max = pool.max
            return self

    class Situation:
        def __init__(self, key: str, name: str, description: str, *elements: SituationBar | SituationPassive | SituationEventPools | SituationTeaser, thumbnail: str = None):
            self.key = key
            self.name = name
            self.description = description
            self.effects = {}
            self.bars = {}
            self.passives = {}
            self.deadline = None
            self.event_pools = {}
            self.comments = []
            self.teasers = {}
            self.pause_until = None
            self.state = "inactive"
            self.thumbnail = thumbnail

            for element in elements:
                if isinstance(element, SituationBar):
                    self.add_bar(element)
                elif isinstance(element, SituationPassive):
                    self.add_passive(element)
                elif isinstance(element, SituationEventPools):
                    self.add_event_pool(element)
                elif isinstance(element, SituationTeaser):
                    self.add_teaser(element)

        @property
        def visible(self):
            log_val("self.visibility_state", self.visibility_state)
            return self.visibility_state == "active" or self.visibility_state == "teaser_active"

        @property
        def visibility_state(self):
            log_val("self.state", self.state)
            if self.state == "completed":
                return "completed"
            elif self.state == "active":
                return "active"
            elif any(teaser.active for teaser in self.teasers.values()):
                return "teaser_active"
            else:
                return "inactive"

        def activate(self):
            self.state = "active"
            return self

        def update_data(self, situation: Situation):
            self.key = situation.key
            self.name = situation.name
            self.description = situation.description
            self.effects = situation.effects
            self.deadline = situation.deadline
            self.comments = situation.comments
            self.thumbnail = situation.thumbnail

            # Sync bars with situation's bars
            new_keys = set(situation.bars.keys())
            old_keys = set(self.bars.keys())
            for key in new_keys:
                if key in self.bars:
                    self.bars[key].update_data(situation.bars[key])
                else:
                    self.add_bar(situation.bars[key])
            for key in list(self.bars.keys()):
                if key not in new_keys:
                    del self.bars[key]

            # Sync passives with situation's passives
            new_keys = set(situation.passives.keys())
            old_keys = set(self.passives.keys())
            for key in new_keys:
                if key in self.passives:
                    self.passives[key].update_data(situation.passives[key])
                else:
                    self.add_passive(situation.passives[key])

            for key in list(self.passives.keys()):
                if key not in new_keys:
                    del self.passives[key]

            # Sync event pools with situation's event pools
            new_keys = set(situation.event_pools.keys())
            old_keys = set(self.event_pools.keys())
            for key in new_keys:
                if key in self.event_pools:
                    self.event_pools[key].update_data(situation.event_pools[key])
                else:
                    self.add_event_pool(situation.event_pools[key])
            for key in list(self.event_pools.keys()):
                if key not in new_keys:
                    del self.event_pools[key]

            # Sync teasers with situation's teasers (preserve active state via update_data)
            new_keys = set(situation.teasers.keys())
            for key in new_keys:
                if key in self.teasers:
                    self.teasers[key].update_data(situation.teasers[key])
                else:
                    self.add_teaser(situation.teasers[key])
            for key in list(self.teasers.keys()):
                if key not in new_keys:
                    del self.teasers[key]

        def add_teaser(self, teaser: SituationTeaser):
            teaser.situation = self
            self.teasers[teaser.key] = teaser
            return self

        def check_teasers(self, **kwargs):
            for teaser in self.teasers.values():
                if teaser.check_conditions(**kwargs):
                    teaser.activate(**kwargs)
            return self

        def get_active_teasers(self):
            return sorted([teaser for teaser in self.teasers.values() if teaser.active], key=lambda x: x.activation_order)

        def add_comments(self, *comments: str):
            self.comments.extend(comments)
            return self

        def add_event_pool(self, event_pool: SituationEventPools):
            event_pool.situation = self
            self.event_pools[event_pool.key] = event_pool
            return self

        def add_deadline(self, deadline: Time):
            self.deadline = deadline
            return self

        def add_bar(self, bar: SituationBar):
            bar.situation = self
            self.bars[bar.key] = bar
            bar.reindex_thresholds()
            return self

        def get_bar(self, key: str):
            if key not in self.bars.keys():
                return None
            return self.bars[key]

        def add_effect(self, key: str, *effects: Effect):
            if key not in self.effects:
                self.effects[key] = []
            self.effects[key].extend(effects)
            return self

        def add_passive(self, passive: SituationPassive):
            passive.situation = self
            self.passives[passive.name] = passive
            return self

        def set_passive(self, passive: string):
            for passive in self.passives:
                if passive.name == passive:
                    passive.run_effects()
                else:
                    passive.revert_effects()

        def apply_progress_change(self, key: str, value: float):
            if key not in self.bars.keys():
                return
            self.bars[key].apply_progress_change(value)

        def get_current_thumbnail(self):
            thumbnail_out = self.thumbnail
            for bar in self.bars.values():
                bar_thumbnail = bar.get_current_thumbnail()
                if bar_thumbnail is not None:
                    thumbnail_out = bar_thumbnail
            return thumbnail_out


    ###################################
    # region Definition helpers ----- #
    # Definition helpers — declarative syntax for load_situations authors.
    # Chain methods (add_*, set_*) return self; __init__ must not return self.

    def AutoThreshold(threshold, approach_hint, direction=1, thumbnail=None, *effects):
        """Auto-fire threshold with empty threshold_hint."""
        return SituationThreshold(threshold, approach_hint, "", direction, *effects, thumbnail=thumbnail)

    def BlockingThreshold(threshold, approach_hint, threshold_hint, direction=1, thumbnail=None, *conditions):
        """Blocking threshold — progress stops until a Condition is fulfilled."""
        return SituationThreshold(threshold, approach_hint, threshold_hint, direction, *conditions, thumbnail=thumbnail)

    def Bar(key, *thresholds, limits=(-100, 100), stat_weights=None):
        """
        Standard main bar with limits and stat weights.

        Bar("main",
            BlockingThreshold(-5, "...", "...", PlaceholderCondition()),
            AutoThreshold(10, "..."),
            limits=(-30, 60),
            stat_weights={HAPPINESS: 0.5},
        )
        """
        bar = SituationBar(key, *thresholds).set_limits(limits[0], limits[1])
        if stat_weights:
            for stat, weight in stat_weights.items():
                bar.add_stat_weight(stat, weight)
        return bar

    def SituationPool(key, bar_min, bar_max):
        return SituationEventPools(key, bar_min, bar_max)

    def PassiveOption(key, description, *effects):
        return SituationPassive(key, description, *effects)

    def Teaser(key, text, *conditions):
        """Pre-activation hint shown before the situation becomes active."""
        return SituationTeaser(key, text, *conditions)

    def activate_situation_teaser(situation_key, teaser_key, **kwargs):
        """Manually activate a teaser (e.g. from the Ren'Py console). Does not activate the situation."""
        if situation_manager is None:
            return None
        situation = situation_manager.get_situation(situation_key)
        if situation is None or teaser_key not in situation.teasers:
            return None
        return situation.teasers[teaser_key].activate(**kwargs)

    def register_situations(*situations):
        """Load or update templates. Call from label load_situations."""
        for situation in situations:
            situation_manager.load_situation(situation)

    # endregion Definition helpers ---#
    ###################################

    class SituationManager:
        def __init__(self):
            self.situations = {}
            self.threshold_checks = {}

        def load_situation(self, situation: Situation):
            if situation.key in self.situations.keys():
                self.situations[situation.key].update_data(situation)
            else:
                self.situations[situation.key] = situation
            return self

        def get_situation(self, key: str):
            if key not in self.situations.keys():
                return None
            return self.situations[key]

        def apply_progress_change(self, key: str, value: float):
            parts = key.split(":")
            if len(parts) == 3:
                keyword, situation_key, bar_key = parts[0], parts[1], parts[2]
            elif len(parts) == 2 and parts[0] == "situation":
                keyword, situation_key, bar_key = parts[0], parts[1], "main"
            elif len(parts) == 2:
                keyword, situation_key, bar_key = "situation", parts[0], parts[1]
            else:
                return
            if keyword != "situation":
                return
            if situation_key not in self.situations.keys():
                return
            self.situations[situation_key].apply_progress_change(bar_key, value)
            return

        def add_threshold_check(self, SituationThreshold: SituationThreshold):
            self.threshold_checks[SituationThreshold.key] = SituationThreshold
            return self

        def check_threshold(self, key: str, **kwargs):
            if key not in self.threshold_checks.keys():
                return
            threshold = self.threshold_checks[key]
            if threshold.blocking.is_fulfilled(**kwargs):
                threshold.trigger_effects()
                threshold.reached = True
                del self.threshold_checks[key]

            return

        def check_all_thresholds(self, **kwargs):
            for key in list(self.threshold_checks.keys()):
                self.check_threshold(key, **kwargs)
            return

        def get_completed_situations(self):
            return [situation for situation in self.situations.values() if situation.state == "completed"]

        def get_visible_situations(self, include_completed: bool = False):
            return [situation for situation in self.situations.values() if situation.visible or (include_completed and situation.state == "completed")]

        def get_visible_teaser_titles(self, *situations: Situation):
            out = []
            for situation in situations:
                if situation.visibility_state == "active" or situation.state == "completed":
                    out.append((situation.name, situation.key))
                elif situation.visibility_state == "teaser_active":
                    out.append(("????????", situation.key))
            return out


label load_situations:
    $ set_current_mod('base')

    if not situation_manager:
        $ situation_manager = SituationManager()

    $ register_situations(
        Situation("cafeteria_crisis", "Cafeteria Crisis", "Die Schule hat keine richtige Mensa. Die Schüler sind auf den teuren Kiosk angewiesen. Adelaide Hall hat sich bereiterklärt zu helfen, aber sie hat keine Erfahrung in Großküchen-Management. Der Protagonist muss die Mensa auf die Beine stellen und Adelaide unterstützen.",
            Teaser("kiosk_complaints", "Im Kiosk wird lautstark über die Preise diskutiert. Für ein normales Mittagessen zahlen die Schülerinnen anscheinend das Doppelte."),
            Teaser("abandoned_kitchen", "Neben dem Hof steht ein leerstehendes Gebäude. An der Tür klebt noch ein vergilbter Speiseplan — dort muss früher eine Küche gewesen sein."),
            Teaser("adelaide_offers", "Adelaide Hall hat Gerüchte über das Essensproblem mitbekommen. Sie würde helfen, sagt sie — wenn die Schule sie lässt."),
            Bar("main",
                BlockingThreshold(-5, "Die Schüler brauchen einen festen Ort zum Mittagessen. Irgendwo auf dem Campus müsste sich etwas finden lassen — ich muss nur noch genauer hinschauen.", "Das leerstehende Gebäude neben dem Hof — dort war früher eine Küche. Ich sollte es inspizieren und prüfen, ob es sich für eine Mensa eignet", PlaceholderCondition()),
                AutoThreshold(10, "Wenn ich die Mensa-Idee vorantreibe, wird sich sicher jemand aus dem PTA-Kreis melden. Ich sollte offen für Angebote sein."),
                BlockingThreshold(20, "Eine Schulküche ist kein Alleingang. Die Elternvertretung muss mitziehen — ich brauche ihre Zustimmung, bevor es weitergeht.", "Die PTA muss der Mensa-Eröffnung zustimmen. Ich sollte eine Abstimmung planen und genug Unterstützung zusammentragen.", PlaceholderCondition()),
                AutoThreshold(35, "Mit der Zustimmung der PTA kann der Umbau beginnen. Die Küche wird eine Weile brauchen, bis sie wieder einsatzbereit ist."),
                BlockingThreshold(40, "Adelaide hat sich bereit erklärt zu helfen, aber Großküchen-Management ist neu für sie. Irgendwann wird sie konkrete Unterstützung brauchen.", "Adelaide steckt beim Essensplan fest. Ich sollte im Büro arbeiten oder in der Mensa nach ihr sehen und ihr helfen.", PlaceholderCondition()),
                AutoThreshold(50, "Wenn Küche und Plan stehen, kommt der entscheidende Test — der erste richtige Mittagsservice für die Schülerinnen."),
                AutoThreshold(60, "Die Mensa läuft. Noch ein paar Schritte, dann hat sich Adelaide eingearbeitet und das Ganze trägt sich von selbst."),
                limits=(-30, 60),
                stat_weights={HAPPINESS: 0.5, EDUCATION: 0.2, REPUTATION: 0.2},
            ),
            PassiveOption("leave_adelaide", "Adelaide alleine lassen", DummyEffect()),
            PassiveOption("hire_staff", "Zusätzliches Personal einstellen", DummyEffect()),
            PassiveOption("train_adelaide", "Adelaide persönlich einarbeiten", DummyEffect()),
            SituationPool("Lieferproblem", 35, 54),
            SituationPool("Schülerbeschwerden", -10, 54),
            SituationPool("Adelaide überfordert", 10, 48),
            SituationPool("Lehrer-Feedback", -5, 54),
            thumbnail="images/journal/buildings/office 10.webp",
        ).add_effect("positive_resolution", DummyEffect()).add_effect("negative_resolution", DummyEffect()),
        # Trigger: sb_event_6. Startwert -20 (bzw. -10/-30 via social_sorting) bei Aktivierung setzen.
        Situation("body_conflict", "Body Conflict", "Körperbezogene Konflikte zwischen Schülerinnen eskalieren. Aona nutzt ihre körperliche Entwicklung als Statuswaffe. Miwa ist das primäre Ziel, aber die toxische Dynamik betrifft die ganze Schule. Der Protagonist muss entscheiden, wie er damit umgeht.",
            Teaser("gym_tension", "Im Sportunterricht herrscht eine merkwürdige Spannung. Mädchen vergleichen sich offen — und manche zwingen andere in die Defensive."),
            Teaser("changing_room_rumors", "Gerüchte aus der Umkleide: Jemand prahlt mit ihrem Körper und macht andere klein. Das klingt nach mehr als nur Kinderkram."),
            Teaser("miwa_withdraws", "Miwa meidet den Speisesaal. Sie isst allein oder gar nicht. Etwas passiert da, das ich noch nicht benennen kann."),
            Bar("main",
                AutoThreshold(-45, "Es wird hässlich zwischen Aona und Miwa. Wenn das so weitergeht, bricht jemand zusammen.", direction=-1),
                AutoThreshold(-35, "Aona wird immer dreister. Das muss jemand stoppen, bevor die ganze Schule mitschuldig wird.", direction=-1),
                AutoThreshold(0, "Nicht alles bleibt im Verborgenen. Irgendwann muss jemand das Problem beim Namen nennen."),
                BlockingThreshold(20, "Aona ist das Zentrum all dessen. Ohne ein Gespräch mit ihr komme ich hier nicht weiter.", "Ich muss mit Aona sprechen — ein Beratungsgespräch im Büro, nicht eine Standpauke.", PlaceholderCondition()),
                AutoThreshold(35, "Miwa scheint langsam wieder aufzutauchen. Vielleicht ist da mehr Hoffnung als ich dachte."),
                BlockingThreshold(50, "Es braucht einen Abschluss. Aona und Miwa müssen sich irgendwann stellen — ob sie wollen oder nicht.", "Der Moment ist da. Aona und Miwa müssen sich gegenüberstehen — wie das ausgeht, liegt auch an mir.", PlaceholderCondition()),
                AutoThreshold(60, "Die Schule verändert sich. Körper unterscheiden die Mädchen nicht mehr — zumindest nicht so, wie es Aona wollte."),
                limits=(-50, 60),
                stat_weights={HAPPINESS: 1.0, INHIBITION: -0.8, CHARM: 0.3},
            ),
            PassiveOption("wait_and_observe", "Abwarten und beobachten", DummyEffect()),
            PassiveOption("fund_counseling", "Schulberatung finanzieren", DummyEffect()),
            PassiveOption("accelerate_exposure", "Exposure beschleunigen", DummyEffect()),
            SituationPool("gym_enter_changing_tension", -50, 54),
            SituationPool("cafeteria_look_around_dynamics", -40, 54),
            SituationPool("school_dormitory_peek_students_night_talk", -35, 50),
            SituationPool("courtyard_patrol_bodies", -45, 54),
            SituationPool("school_building_teach_class_body", -25, 54),
            SituationPool("office_building_counselling_teacher", 0, 54),
            thumbnail="images/journal/buildings/office 10.webp",
        ).add_effect("positive_resolution", DummyEffect()).add_effect("negative_resolution", DummyEffect()),
    )
    