################################
# region Journal Alert System #
################################
# Attention flags for journal surfaces. Topics are registered at init (not saved).
# Pending item ids live on journal_alert_manager and persist with the save.
# The map journal button shows icons/journal_icon_highlight.webp while any
# pending item exists; opening that item in the journal clears it.

init -20 python:
    JOURNAL_ALERT_TOPICS = {}

    JOURNAL_MAP_ICON_IDLE = "icons/journal_icon_idle.webp"
    JOURNAL_MAP_ICON_HIGHLIGHT = "icons/journal_icon_highlight.webp"

    class JournalAlertTopic:
        """
        Declares one journal surface that can raise map/journal attention flags.

        Args:
            key (str): Topic id used when raising/clearing (``situations``,
                ``unlockables``, …).
            page (int): Primary journal page. Opening this page with an empty
                display clears the topic-level ``""`` item, and the whole topic
                if ``clear_on_page`` is True.
            extra_item_pages (tuple): Additional pages that can acknowledge a
                specific item (e.g. unlockables opened via the situations page).
            extract_item (callable | None): ``display -> item_id``. Defaults to
                using the display string as-is.
            clear_on_page (bool): If True, opening the primary page with an
                empty display clears every pending item for this topic.
        """

        def __init__(
            self,
            key,
            page,
            extra_item_pages=(),
            extract_item=None,
            clear_on_page=False,
        ):
            self.key = key
            self.page = int(page)
            self.extra_item_pages = tuple(extra_item_pages or ())
            self.extract_item = extract_item
            self.clear_on_page = bool(clear_on_page)

        def item_from_display(self, display):
            """
            Map a journal ``display`` value to a pending item id.

            Args:
                display (str): The ``open_journal`` display argument.

            Returns:
                str: Item id, or ``""`` if display is empty.
            """
            if display is None or display == "":
                return ""
            if self.extract_item is not None:
                item = self.extract_item(display)
                if item is None:
                    return ""
                return str(item)
            return str(display)

        def listens_to_page(self, page):
            """
            Whether this topic should react to a journal page opening.

            Args:
                page (int): Journal page number.

            Returns:
                bool: True if this is the primary page or an extra item page.
            """
            page = int(page)
            return page == self.page or page in self.extra_item_pages

    class JournalAlertManager:
        """
        Save-backed pending alerts, keyed by topic then item id.

        An empty item id ``""`` is a topic-level ping (no specific row). Named
        items stay pending until that row is opened in the journal.
        """

        def __init__(self):
            self.pending = {}

        def _ensure_pending(self):
            if not hasattr(self, "pending") or self.pending is None:
                self.pending = {}
            return self.pending

        def raise_alert(self, topic, item=""):
            """
            Mark a topic (and optional item) as unseen.

            Args:
                topic (str): Registered topic key.
                item (str): Specific journal row id. ``""`` is topic-level.
            """
            topic = str(topic)
            item = "" if item is None else str(item)
            pending = self._ensure_pending()
            items = pending.setdefault(topic, [])
            if item not in items:
                items.append(item)

        def clear_alert(self, topic, item=None):
            """
            Clear one item, or the whole topic if ``item`` is None.

            Args:
                topic (str): Topic key.
                item (str | None): Item id to remove, or None to drop the topic.
            """
            topic = str(topic)
            pending = self._ensure_pending()
            if topic not in pending:
                return
            if item is None:
                del pending[topic]
                return
            item = str(item)
            items = pending[topic]
            if item in items:
                items.remove(item)
            if not items:
                del pending[topic]

        def has_alert(self, topic=None, item=None):
            """
            Whether any (or a specific) alert is still pending.

            Args:
                topic (str | None): Limit to one topic. None = any topic.
                item (str | None): Limit to one item. None = any item in scope.

            Returns:
                bool: True if a matching pending item exists.
            """
            pending = self._ensure_pending()
            if topic is None:
                return any(items for items in pending.values())
            items = pending.get(str(topic), [])
            if item is None:
                return bool(items)
            return str(item) in items

        def get_pending_items(self, topic):
            """
            Pending item ids for a topic.

            Args:
                topic (str): Topic key.

            Returns:
                list[str]: Copy of the pending item list (may include ``""``).
            """
            pending = self._ensure_pending()
            return list(pending.get(str(topic), []))

        def acknowledge(self, page, display=""):
            """
            Clear alerts that the opened journal view covers.

            Opening a topic's primary page with an empty display clears only the
            topic-level ``""`` ping, unless the topic sets ``clear_on_page``.
            Opening a specific item clears that item (and the topic-level ping)
            on the primary page and on ``extra_item_pages``.

            Args:
                page (int): Journal page number.
                display (str): Journal display / selected row.
            """
            display = "" if display is None else str(display)
            for topic in JOURNAL_ALERT_TOPICS.values():
                if not topic.listens_to_page(page):
                    continue
                if display == "":
                    if page != topic.page:
                        continue
                    self.clear_alert(topic.key, "")
                    if topic.clear_on_page:
                        self.clear_alert(topic.key)
                    continue
                item = topic.item_from_display(display)
                if item == "":
                    continue
                if page == topic.page or page in topic.extra_item_pages:
                    self.clear_alert(topic.key, item)
                    self.clear_alert(topic.key, "")

    def register_journal_alert_topic(
        key,
        page,
        extra_item_pages=(),
        extract_item=None,
        clear_on_page=False,
    ):
        """
        Register (or replace) a journal alert topic.

        Call from ``init python`` so the topic exists on every load. Pending
        items are not stored here — they live on ``journal_alert_manager``.

        Args:
            key (str): Topic id.
            page (int): Primary journal page.
            extra_item_pages (tuple): Extra pages that can clear a specific item.
            extract_item (callable | None): Maps ``display`` to an item id.
            clear_on_page (bool): Empty primary-page open clears the whole topic.

        Returns:
            JournalAlertTopic: The registered topic.
        """
        topic = JournalAlertTopic(
            key,
            page,
            extra_item_pages=extra_item_pages,
            extract_item=extract_item,
            clear_on_page=clear_on_page,
        )
        JOURNAL_ALERT_TOPICS[key] = topic
        return topic

    def raise_journal_alert(topic, item=""):
        """
        Raise a journal attention flag.

        Args:
            topic (str): Topic key (must be registered to be acknowledged by page).
            item (str): Specific row id, or ``""`` for a topic-level ping.
        """
        if journal_alert_manager is None:
            return
        journal_alert_manager.raise_alert(topic, item)

    def clear_journal_alert(topic, item=None):
        """
        Clear a journal attention flag.

        Args:
            topic (str): Topic key.
            item (str | None): Item id, or None to clear the whole topic.
        """
        if journal_alert_manager is None:
            return
        journal_alert_manager.clear_alert(topic, item)

    def journal_has_alert(topic=None, item=None):
        """
        Whether the journal currently has unseen changes.

        Args:
            topic (str | None): Limit to one topic.
            item (str | None): Limit to one item.

        Returns:
            bool: True if a matching alert is pending.
        """
        if journal_alert_manager is None:
            return False
        return journal_alert_manager.has_alert(topic, item)

    def get_journal_map_icon():
        """
        Idle map icon, swapping in the highlight asset while any alert is pending.

        Returns:
            str: Image path relative to ``images/``.
        """
        if journal_has_alert():
            return JOURNAL_MAP_ICON_HIGHLIGHT
        return JOURNAL_MAP_ICON_IDLE

    def notify_situation_journal_alert(situation):
        """
        Raise the alert topic that belongs to a Situation or Unlockable.

        Args:
            situation: A ``Situation`` (or subclass such as ``Unlockable``).
        """
        if situation is None:
            return
        topic = situation.get_journal_alert_topic()
        raise_journal_alert(topic, situation.key)

    def acknowledge_journal_alerts(page, display=""):
        """
        Clear alerts covered by an opened journal view.

        Args:
            page (int): Journal page number.
            display (str): Journal display / selected row.
        """
        if journal_alert_manager is None:
            return
        journal_alert_manager.acknowledge(page, display)

init python:
    def _journal_alert_item_from_situation_display(display):
        key, _tab = parse_situation_journal_display(display)
        return key

    register_journal_alert_topic(
        "situations",
        page=8,
        extract_item=_journal_alert_item_from_situation_display,
    )
    register_journal_alert_topic(
        "unlockables",
        page=4,
        extra_item_pages=(8,),
        extract_item=_journal_alert_item_from_situation_display,
    )

default journal_alert_manager = JournalAlertManager()

# endregion
################################
