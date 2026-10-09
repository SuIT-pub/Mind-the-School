#############################################
# region Situation Test Lab ----- #
#
# Debug-only Situation that exercises every part of the Situation system:
# multi-bar + weights, start-value modifiers, stat weights, base wear on two
# intervals, auto thresholds (one-shot, repeatable, downward, multi-bound),
# blocking thresholds (plain + timed release with hold), conditional
# descriptions, teasers (game-data, event-seen, photo), passives (bar drift,
# stat modifier, game data, regular stat change, general bridge), measures
# (duration/cooldown/quota, instant event, cancel), event pools, and all four
# resolution types (grace timer + delta_lock, latch, deadline, condition).
#
# Started from Journal -> Cheats -> Debug -> "Situation Test Lab". It is
# registered on every load (so saves keep it) but stays inactive and hidden
# until the lab activates it. Every runtime key contains "sit_test" so the lab
# reset can wipe game data, timers, counters and latches in one sweep.

init 1 python:
    set_current_mod('base')

    SIT_TEST_KEY = "sit_test_lab"

    # Threshold / resolution / measure scenes: only fired by EventEffects.
    sit_test_events = EventStorage("sit_test_events", "misc")
    sit_test_events.add_event(
        Event(2, "sit_test_thresh_auto", override_location="misc"),
        Event(2, "sit_test_thresh_repeat", override_location="misc"),
        Event(2, "sit_test_thresh_warning", override_location="misc"),
        Event(2, "sit_test_thresh_timed", override_location="misc"),
        Event(2, "sit_test_measure_event", override_location="misc"),
        Event(2, "sit_test_resolve_positive", override_location="misc"),
        Event(2, "sit_test_resolve_negative", override_location="misc"),
        Event(2, "sit_test_resolve_deadline", override_location="misc"),
        Event(2, "sit_test_resolve_condition", override_location="misc"),
        # Stand-in for a regular game event (queue regression, test N1).
        Event(2, "sit_test_normal_event", override_location="misc"),
    )

    # Pool events: Office building -> Look around, only while the lab is active
    # and the combined bar sits inside the pool window.
    office_building_events["look_around"].add_event(Event(
        3,
        "sit_test_pool_low",
        SituationPoolCondition(SIT_TEST_KEY, "sit_test_pool_low")))
    office_building_events["look_around"].add_event(Event(
        3,
        "sit_test_pool_high",
        SituationPoolCondition(SIT_TEST_KEY, "sit_test_pool_high")))

    SIT_TEST_EVENT_LABELS = [
        "sit_test_thresh_auto",
        "sit_test_thresh_repeat",
        "sit_test_thresh_warning",
        "sit_test_thresh_timed",
        "sit_test_measure_event",
        "sit_test_resolve_positive",
        "sit_test_resolve_negative",
        "sit_test_resolve_deadline",
        "sit_test_resolve_condition",
        "sit_test_pool_low",
        "sit_test_pool_high",
        "sit_test_normal_event",
    ]

    def get_sit_test_deadline() -> Time:
        """
        Deadline for the lab's DeadlineResolution.

        Set by the lab on a fresh run (now + 3 days). Without one the deadline
        sits far in the future so the resolution never fires by accident.

        Returns:
            Time: The deadline.
        """
        deadline = get_game_data("sit_test_deadline")
        if isinstance(deadline, Time):
            return Time(deadline)
        return Time("1-1-2999-1")

    def build_situation_test_lab() -> Situation:
        """
        Fresh template of the Situation Test Lab.

        Returns:
            Situation: Unregistered situation definition.
        """
        return Situation(SIT_TEST_KEY, "Situation Test Lab",
            SituationDescription([
                "Debug situation. Exercises every building block of the Situation system.",
                "Drive it from Journal -> Cheats -> Debug -> Situation Test Lab.",
            ]),
            SituationDescription(
                "Conditional description: gate 1 has been opened.",
                GameDataCondition("sit_test_gate_1_open", True),
            ),

            # --- Bars: weighted multi-bar, start modifiers, stat weights, wear ---
            Bar("main",
                weight=2,
                limits=(-30, 40),
                start_base=0,
                start_modifiers=[
                    StartModifier("+", 2),
                    StartModifier("+", 0.02, stat=HAPPINESS),
                    StartModifier("range_percent", 2),
                ],
                stat_weights={HAPPINESS: 0.5, INHIBITION: -0.3},
                regular_decrease_rate=-0.5,
            ),
            Bar("side",
                weight=1,
                limits=(-20, 20),
                start_base=-2,
                stat_weights={EDUCATION: 0.5},
                regular_decrease_rate=-1,
                regular_decrease_interval="daily",
            ),

            # --- Auto thresholds ---
            AutoThreshold(
                "Test: repeatable auto threshold (hold 3) at main 5.",
                EventEffect("sit_test_thresh_repeat"),
                main=5,
                default_hold=3,
            ),
            AutoThreshold(
                "Test: one-shot auto threshold at main 10.",
                EventEffect("sit_test_thresh_auto"),
                main=10,
            ),
            AutoThreshold(
                "Test: multi-bound auto threshold at main 15 AND side 10.",
                ValueEffect("sit_test_multi_fired", True),
                main=15,
                side=10,
            ),
            AutoThreshold(
                "Test: downward warning at main -15.",
                EventEffect("sit_test_thresh_warning"),
                main=-15,
                direction=-1,
            ),

            # --- Blocking thresholds ---
            BlockingThreshold(
                "Test: blocking gate 1 ahead at main 20.",
                "Gate 1 reached. Open it from the lab (Gates & flags).",
                GameDataCondition("sit_test_gate_1_open", True),
                main=20,
                visible_range=10,
            ),
            BlockingThreshold(
                "Test: timed gate 2 ahead at main 30.",
                "Gate 2 reached. Open it from the lab, or wait 2 daytimes for the timed release.",
                GameDataCondition("sit_test_gate_2_open", True),
                TimerCondition("sit_test_gate_2_timer", daytime=2),
                EventEffect("sit_test_thresh_timed"),
                main=30,
                default_hold=2,
            ),

            # --- Passives (Layer 2) ---
            PassiveOption("sit_test_passive_drift", "Drift: main +1 per daytime.",
                SituationEffectBarChangeModifier("main", 1, "+", "daytime_change"),
            ),
            PassiveOption("sit_test_passive_stat", "Stat modifier + game data flag.",
                SituationEffectStatChangeModifier(HAPPINESS, 1, "+"),
                SituationEffectSetGameData("sit_test_passive_flag", 1, "Sets sit_test_passive_flag"),
            ),
            PassiveOption("sit_test_passive_regular", "Regular stat change: Happiness +1 daily.",
                SituationEffectRegularStatChange(HAPPINESS, 1, "daily"),
            ),
            PassiveOption("sit_test_passive_general", "General bridge: plain ValueEffect.",
                SituationEffectGeneral(
                    "sit_test_general_value",
                    [ValueEffect("sit_test_general_flag", True)],
                    ["Sets sit_test_general_flag"],
                ),
            ),

            # --- Measures (Layer 3) ---
            MeasureOption(
                "sit_test_measure_push",
                "Push side: +3 per daytime for 2 daytimes. Cooldown 1 daytime, max 2 uses.",
                TimerCondition("sit_test_measure_push_duration", daytime=2),
                TimerCondition("sit_test_measure_push_cooldown", daytime=1),
                ManualCounterCondition("sit_test_measure_push_count", 2),
                instant=[SituationEffectSetGameData("sit_test_measure_push_ping", 1, "Sets sit_test_measure_push_ping")],
                permanent=[SituationEffectBarChangeModifier("side", 3, "+", "daytime_change")],
            ),
            MeasureOption(
                "sit_test_measure_event",
                "Instant measure: plays a test event.",
                None,
                instant=[
                    SituationEffectGeneral(
                        "sit_test_measure_event_call",
                        [EventEffect("sit_test_measure_event")],
                        ["Plays sit_test_measure_event"],
                        revert=False,
                    )
                ],
            ),
            MeasureOption(
                "sit_test_measure_cancel",
                "Instant measure: cancels the situation.",
                None,
                instant=[SituationEffectCancelSituation()],
            ),

            # --- Event pools (Office building -> Look around) ---
            SituationPool("sit_test_pool_low", -26, 0),
            SituationPool("sit_test_pool_high", 1, 33),

            # --- Teasers ---
            Teaser(
                "sit_test_teaser_observation",
                "Test teaser (observation), unlocked by a game-data flag.",
                GameDataCondition("sit_test_teaser_flag", True),
                interpretation="Interpretation line of the observation teaser.",
                note_type="observation",
            ),
            Teaser(
                "sit_test_teaser_suspicion",
                "Test teaser (suspicion), unlocked by the same flag.",
                GameDataCondition("sit_test_teaser_flag", True),
                note_type="suspicion",
                layout="text_aside",
            ),
            Teaser(
                "sit_test_teaser_photo",
                "Test teaser (insight) with a photo.",
                GameDataCondition("sit_test_teaser_flag", True),
                interpretation="Photo layout check.",
                note_type="insight",
                image="images/misc/Test_16_9.png",
                layout="photo_top",
            ),
            Teaser(
                "sit_test_teaser_event_seen",
                "Test teaser (setback), unlocked once the one-shot threshold event was seen.",
                EventSeenCondition(True, "sit_test_thresh_auto"),
                note_type="setback",
            ),

            # --- Resolutions ---
            PositiveResolution(
                "ALL",
                TimerCondition("sit_test_positive_grace", daytime=1),
                ValueEffect("sit_test_resolved", "positive"),
                ModifierEffect("sit_test_positive_buff", HAPPINESS, Modifier_Obj("sit_test_positive_buff", "+", 1)),
                EventEffect("sit_test_resolve_positive"),
                delta_lock=True,
            ),
            NegativeResolution(
                "ANY",
                TimerCondition("sit_test_negative_grace", daytime=1),
                ValueEffect("sit_test_resolved", "negative"),
                EventEffect("sit_test_resolve_negative"),
                grace_count=1,
            ),
            DeadlineResolution(
                get_sit_test_deadline(),
                ValueEffect("sit_test_resolved", "deadline"),
                EventEffect("sit_test_resolve_deadline"),
            ),
            ConditionResolution(
                "sit_test_condition_resolution",
                GameDataCondition("sit_test_force_condition", True),
                ValueEffect("sit_test_resolved", "condition"),
                EventEffect("sit_test_resolve_condition"),
            ),

            thumbnail="images/misc/Test_16_9.png",
        )

    # The lab label starts with hide_all(), which also hides the notify screen.
    # Lab messages are therefore queued here and shown after hide_all().
    _sit_test_pending_notify = []

    def sit_test_notify(message: str):
        _sit_test_pending_notify.append(message)

    def show_sit_test_notify():
        if _sit_test_pending_notify:
            renpy.notify("\n".join(_sit_test_pending_notify))
            del _sit_test_pending_notify[:]

    def get_sit_test_situation():
        if situation_manager is None:
            return None
        return situation_manager.get_situation(SIT_TEST_KEY)

    # Event flag used by the lab's flag tests (testplan section R).
    SIT_TEST_FLAG = "sit_test_camp"

    def toggle_sit_test_situation_flag():
        """Runtime only: switch the lab's situation flag between None and SIT_TEST_FLAG (a load restores None)."""
        situation = get_sit_test_situation()
        situation.flag = None if situation.flag == SIT_TEST_FLAG else SIT_TEST_FLAG
        situation.sync_flag_pause()
        return situation.flag

    def reset_situation_test_lab():
        """
        Wipe every runtime trace of the lab and register a fresh template.

        Cancels the live situation (passives, measures, tracked modifiers),
        drops pending threshold checks, resolution modifiers and queued lab
        events, deletes all "sit_test" game data (flags, timers, counters,
        latches), clears the seen state of the lab events, clears the lab's
        event flag, then replaces the live situation with a fresh, inactive
        definition.
        """
        if get_current_flag() == SIT_TEST_FLAG:
            set_current_flag(None)
        live = get_sit_test_situation()
        if live is not None:
            if live.state == "active":
                live.cancel()
            for resolution in live.resolutions.values():
                lifecycle_registry.clear(owner=resolution.counter_key)

        prefix = "situation:" + SIT_TEST_KEY + ":"
        for check_key in list(situation_manager.threshold_checks.keys()):
            if check_key.startswith(prefix):
                del situation_manager.threshold_checks[check_key]
                lifecycle_registry.ping(check_key, REMOVE)

        if situation_manager.has_pending_events():
            situation_manager.pending_events = [
                entry for entry in situation_manager.pending_events
                if not str(entry[0]).startswith("sit_test")
            ]

        for key in list(gameData.keys()):
            if "sit_test" in key:
                del gameData[key]

        seen_events = get_game_data("seen_events") or {}
        for event_label in SIT_TEST_EVENT_LABELS:
            seen_events.pop(event_label, None)
            seenEvents.pop(event_label, None)
        set_game_data("seen_events", seen_events)

        # A negative lab resolution starts the global breather, which suspends
        # base wear until the next days pass. End it so a fresh run starts clean.
        if situation_manager.is_resolution_breather_active():
            situation_manager.resolution_breather_active = False
            situation_manager.resolution_breather_days = 0
            situation_manager._resume_all_decrease_modifiers()
            log("Situation Test Lab reset ended the resolution breather.", category="situation")

        if SIT_TEST_KEY in situation_manager._situations:
            del situation_manager._situations[SIT_TEST_KEY]
        situation_manager.load_situation(build_situation_test_lab())
        log("Situation Test Lab reset.", category="situation")

    def start_situation_test_lab():
        """Fresh run: reset, set the deadline to now + 3 days, activate."""
        reset_situation_test_lab()
        deadline = Time("now")
        deadline.add_time(day=3)
        set_game_data("sit_test_deadline", deadline)

        situation = get_sit_test_situation()
        if situation is None or getattr(situation, "invalid", False):
            renpy.notify("Situation Test Lab failed its self-test. Check the logs (category: situation).")
            return
        situation.resolutions["deadline_resolution"].value = Time(deadline)
        situation.activate()
        log("Situation Test Lab started.", category="situation")

    def push_sit_test_bar(bar_key: str, delta: float):
        situation_manager.apply_progress_change(f"situation:{SIT_TEST_KEY}:{bar_key}", delta)

    def run_sit_test_checks():
        """Run the same situation checks end_event runs (events get queued)."""
        situation_manager.check_all_thresholds()
        situation_manager.check_passives()
        situation_manager.check_teasers()
        situation_manager.check_resolutions()

    def force_sit_test_deadline():
        """Move the deadline one day into the past so it fires on the next check."""
        situation = get_sit_test_situation()
        if situation is None:
            return
        deadline = Time("now")
        deadline.add_time(day=-1)
        set_game_data("sit_test_deadline", deadline)
        situation.resolutions["deadline_resolution"].value = Time(deadline)

    def get_sit_test_status_pages() -> List[str]:
        """
        Human-readable status of the lab, split into sections for the
        sit_test_status screen.
        The full state is also written to the log (category: situation).

        Returns:
            List[str]: Status pages.
        """
        situation = get_sit_test_situation()
        if situation is None:
            return ["Situation Test Lab is not registered."]

        def fmt(value):
            return f"{value:.1f}" if isinstance(value, float) else str(value)

        stats = {
            "happiness": float(get_stat_number(HAPPINESS)),
            "inhibition": float(get_stat_number(INHIBITION)),
            "education": float(get_stat_number(EDUCATION)),
        }
        # What the daily / daytime modifier tick would add to Happiness right now.
        daily_happiness = float(apply_stat_modifier(HAPPINESS, 0, "daily"))
        daytime_happiness = float(apply_stat_modifier(HAPPINESS, 0, "daytime_change"))
        if situation_manager.is_resolution_breather_active():
            breather = f"ACTIVE, {situation_manager.get_resolution_breather_display_days()} day(s)"
        else:
            breather = "off"

        def fmt_time(t):
            return f"{t.get_day()}.{t.get_month()}.{t.get_year()} dt {t.get_daytime()}" if isinstance(t, Time) else "-"

        if situation.is_paused():
            pause_text = f"YES since {fmt_time(situation.pause_started)} ({'+'.join(situation.get_pause_reasons())})"
        else:
            pause_text = "no"

        bar_lines = []
        for bar in situation.bars.values():
            bar_lines.append(f"{bar.key}: {fmt(bar.value)} ({bar.min} .. {bar.max}), tendency {fmt(bar.tendency)}")
        page_1 = "\n".join([
            f"State: {situation.state} / {situation.visibility_state}" + ("  (INVALID)" if getattr(situation, "invalid", False) else ""),
            f"Combined: {fmt(situation.get_combined_bar_value())}",
        ] + bar_lines + [
            f"Passive: {situation.active_passive or '-'}   Measure: {situation.active_measure or '-'}",
            f"Teasers active: {sum(1 for t in situation.teasers.values() if t.active)}/{len(situation.teasers)}",
            f"Stats: Happiness {fmt(stats['happiness'])}   Inhibition {fmt(stats['inhibition'])}   Education {fmt(stats['education'])}",
            f"Happiness modifiers per day: {fmt(daily_happiness)}   per daytime: {fmt(daytime_happiness)}",
            f"Resolution breather: {breather} (pauses base wear)",
            f"Paused: {pause_text}   paused daytimes total: {situation.get_paused_daytimes()}",
            f"Event flag: {get_current_flag()}   situation flag: {situation.flag} (exclusive {situation.flag_exclusive})",
        ])

        threshold_lines = []
        for threshold in sorted(situation.thresholds.values(), key=lambda t: t.bounds.get("main", 0)):
            bounds = ",".join(f"{k}:{v}" for k, v in threshold.bounds.items())
            kind = "block" if threshold.is_blocking() else "auto"
            pending = " PENDING" if threshold.key in situation_manager.threshold_checks else ""
            threshold_lines.append(f"{bounds} [{kind}] reached={threshold.reached} hold={threshold.hold}{pending}")
        page_2 = "Thresholds:\n" + "\n".join(threshold_lines)

        # Lifecycle entries owned by the lab (passive/measure/resolution modifiers).
        tracked = sorted(key for key in lifecycle_registry.entries.keys() if "sit_test" in key)
        hibernated = sorted(
            key for key in tracked
            if lifecycle_registry.entries[key].state == LIFECYCLE_HIBERNATED
        )
        # Start time of every lab timer (measure duration/cooldown, grace, timed release).
        timers = {
            key[len("timer_"):]: fmt_time(value)
            for key, value in gameData.items()
            if key.startswith("timer_") and "sit_test" in key
        }

        deadline_text = "-"
        deadline_resolution = situation.resolutions.get("deadline_resolution")
        if deadline_resolution is not None and isinstance(deadline_resolution.value, Time):
            d = deadline_resolution.value
            deadline_text = f"{d.get_day()}.{d.get_month()}.{d.get_year()} daytime {d.get_daytime()}"
            if situation.get_paused_daytimes() > 0:
                effective = Time(d)
                effective.add_time(daytime = situation.get_paused_daytimes())
                deadline_text += f"  → effective {fmt_time(effective)} (+{situation.get_paused_daytimes()} paused)"

        resolution_lines = []
        for resolution in situation.resolutions.values():
            resolution_lines.append(f"{resolution.key}: reached={resolution.is_reached()} grace={resolution._grace_active}")
        page_3 = "\n".join(
            ["Resolutions:"] + resolution_lines + [
                f"Resolved flag: {get_game_data('sit_test_resolved', '-')}   Multi fired: {get_game_data('sit_test_multi_fired', False)}",
                f"Deadline: {deadline_text}",
                f"Queued situation events: {len(getattr(situation_manager, 'pending_events', None) or [])}",
                f"Tracked lab modifiers: {len(tracked)}   hibernated: {len(hibernated)}",
                "Timers (started):",
            ] + [f"  {key}: {value}" for key, value in sorted(timers.items())]
        )

        log_json("sit_test_status", {
            "state": situation.state,
            "bars": {bar.key: bar.value for bar in situation.bars.values()},
            "thresholds": {t.key: {"reached": t.reached, "hold": t.hold} for t in situation.thresholds.values()},
            "threshold_holds": dict(situation.threshold_holds),
            "resolutions": {r.key: {"reached": r.is_reached(), "grace": r._grace_active} for r in situation.resolutions.values()},
            "game_data": {k: str(v) for k, v in gameData.items() if "sit_test" in k},
            "tracked_modifiers": tracked,
            "hibernated_modifiers": hibernated,
            "paused": situation.is_paused(),
            "pause_reasons": list(situation.get_pause_reasons()),
            "flag": situation.flag,
            "current_flag": get_current_flag(),
            "pause_started": fmt_time(situation.pause_started),
            "paused_daytimes": situation.get_paused_daytimes(),
            "timers": timers,
            "stats": stats,
            "happiness_modifiers": {"daily": daily_happiness, "daytime_change": daytime_happiness},
            "breather": breather,
            "deadline": deadline_text,
        }, category="situation")

        # Shown with substitute False, so only text tags need escaping.
        return [page.replace("{", "{{") for page in [page_1, page_2, page_3]]

# endregion
###################################


###################################
# region Lab control label ----- #

screen sit_test_status(pages):
    # Scrollable status overlay; the say window is too small for the full state.
    modal True
    zorder 100
    add Solid("#000000c0")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1500
        ysize 900
        padding (30, 30)
        background Solid("#1b1b1bf0")

        vbox:
            spacing 20
            text "Situation Test Lab - Status" size 32 color "#ffffff"

            viewport:
                ysize 720
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    spacing 24
                    for page in pages:
                        text page substitute False size 24 color "#e0e0e0"

            textbutton "Close":
                text_size 28
                text_color "#ffffff"
                text_hover_color "#ffd54f"
                xalign 1.0
                action Return()

label situation_test_lab:
    $ hide_all()
    $ show_sit_test_notify()

    if get_sit_test_situation() is None:
        "Situation Test Lab is not registered - its self-test failed on load. See log.txt (category: situation)."
        jump map_entry

    menu:
        "Situation Test Lab — what now?"

        "Lifecycle":
            menu:
                "Reset + activate (fresh run)":
                    $ start_situation_test_lab()
                    $ sit_test_notify("Fresh run started.")
                "Reset only (inactive)":
                    $ reset_situation_test_lab()
                    $ sit_test_notify("Lab reset.")
                "Pause":
                    if get_sit_test_situation().pause():
                        $ sit_test_notify("Lab paused.")
                    else:
                        $ sit_test_notify("Not paused (not active, or already paused manually).")
                "Resume":
                    if get_sit_test_situation().resume():
                        if get_sit_test_situation().is_paused():
                            $ sit_test_notify("Manual pause removed, still paused by the event flag.")
                        else:
                            $ sit_test_notify("Lab resumed.")
                    else:
                        $ sit_test_notify("Not resumed (no manual pause).")
                "Set event flag 'sit_test_camp'":
                    $ set_current_flag(SIT_TEST_FLAG)
                    $ sit_test_notify("Event flag: sit_test_camp")
                "Clear event flag":
                    $ set_current_flag(None)
                    $ sit_test_notify("Event flag cleared.")
                "Toggle lab situation flag (None / sit_test_camp)":
                    $ sit_test_notify("Lab situation flag: " + str(toggle_sit_test_situation_flag()))
                "Back":
                    pass

        # Push actions are split into two submenus; one long menu runs off the screen.
        "Push bar: main":
            menu:
                "main +5":
                    $ push_sit_test_bar("main", 5)
                "main +15":
                    $ push_sit_test_bar("main", 15)
                "main -5":
                    $ push_sit_test_bar("main", -5)
                "main -15":
                    $ push_sit_test_bar("main", -15)
                "Back":
                    pass

        "Push: side / ALL / Happiness":
            menu:
                "side +5":
                    $ push_sit_test_bar("side", 5)
                "side -5":
                    $ push_sit_test_bar("side", -5)
                "ALL +80 (to max)":
                    $ push_sit_test_bar("ALL", 80)
                "ALL -80 (to min)":
                    $ push_sit_test_bar("ALL", -80)
                "Happiness +10 (stat weights)":
                    $ change_stat(HAPPINESS, 10)
                "Happiness -10 (stat weights)":
                    $ change_stat(HAPPINESS, -10)
                "Back":
                    pass

        "Gates, flags & events":
            menu:
                "Play normal event (Happiness +2)":
                    call sit_test_normal_event from _call_sit_test_normal_event
                "Open gate 1 (main 20)":
                    $ set_game_data("sit_test_gate_1_open", True)
                "Open gate 2 (main 30, timed)":
                    $ set_game_data("sit_test_gate_2_open", True)
                "Unlock flag teasers":
                    $ set_game_data("sit_test_teaser_flag", True)
                "Back":
                    pass

        "Resolutions":
            menu:
                "Force condition resolution":
                    $ set_game_data("sit_test_force_condition", True)
                "Move deadline into the past":
                    $ force_sit_test_deadline()
                "Back":
                    pass

        "Run checks now":
            $ run_sit_test_checks()

        "Show status":
            call screen sit_test_status(get_sit_test_status_pages())

        "Advance one daytime (leaves lab)":
            jump new_daytime

        "Leave":
            jump map_entry

    # Bar pushes and checks queue threshold/resolution events; play them now.
    $ run_sit_test_checks()
    call drain_situation_events from _call_drain_situation_events_test_lab
    jump situation_test_lab

# endregion
###################################


###################################
# region Lab events ----- #

label sit_test_thresh_auto (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)
    subtitles "TEST — one-shot AutoThreshold (main 10) fired. Must play exactly once per run."
    $ end_event('none', **kwargs)
    return

label sit_test_thresh_repeat (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)
    subtitles "TEST — repeatable AutoThreshold (main 5, hold 3) fired. Re-arms after main drops below 2."
    $ end_event('none', **kwargs)
    return

label sit_test_thresh_warning (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)
    subtitles "TEST — downward AutoThreshold (main -15) fired."
    $ end_event('none', **kwargs)
    return

label sit_test_thresh_timed (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)
    subtitles "TEST — timed BlockingThreshold (main 30) released by its timer."
    $ end_event('none', **kwargs)
    return

label sit_test_measure_event (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)
    subtitles "TEST — instant measure event played."
    $ end_event('none', **kwargs)
    return

label sit_test_resolve_positive (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)
    subtitles "TEST — PositiveResolution fired (after the 1-daytime grace). The situation must now be completed."
    $ end_event('none', **kwargs)
    return

label sit_test_resolve_negative (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)
    subtitles "TEST — NegativeResolution fired (latch exhausted or grace expired)."
    $ end_event('none', **kwargs)
    return

label sit_test_resolve_deadline (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)
    subtitles "TEST — DeadlineResolution fired."
    $ end_event('none', **kwargs)
    return

label sit_test_resolve_condition (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)
    subtitles "TEST — ConditionResolution fired."
    $ end_event('none', **kwargs)
    return

label sit_test_normal_event (**kwargs):
    # Behaves like a regular game event: the stat change mid-event crosses a
    # threshold, its event is queued and must play right after end_event.
    $ begin_event(no_gallery = True, **kwargs)
    subtitles "TEST — normal event: Happiness +2 (main +1 via stat weight)."
    call change_stats_with_modifier(happiness = 2) from _call_sit_test_normal_event_stats
    subtitles "TEST — normal event ends now. A crossed threshold event must follow directly."
    $ end_event('none', **kwargs)
    return

label sit_test_pool_low (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)
    subtitles "TEST — pool event (combined bar -26 .. 0)."
    $ end_event('new_daytime', **kwargs)
    return

label sit_test_pool_high (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)
    subtitles "TEST — pool event (combined bar 1 .. 33)."
    $ end_event('new_daytime', **kwargs)
    return

# endregion
###################################
