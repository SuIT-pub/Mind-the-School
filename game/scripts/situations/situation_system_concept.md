# Situation System — Konzeptdokument

## Überblick

Das Situation-System ersetzt das bestehende Quest-System als primäres Spielerführungssystem. Statt einer Checkliste mit Goals und Tasks sieht der Spieler einen bidirektionalen Fortschrittsbalken mit narrativen Hinweisen. Situations geben dem Spieler ein Ziel, ohne ihm jeden Schritt vorzukauen — sie respektieren die Sandbox-Philosophie des Spiels.

---

## Kernprinzip

Eine Situation repräsentiert ein laufendes Problem oder eine Entwicklung an der Schule, die der Spieler aktiv beeinflussen kann. Der Fortschritt wird als Balken dargestellt, der sich in positive oder negative Richtung bewegen kann. Am Ende steht eine positive oder negative Resolution mit konkreten Konsequenzen.

Der Spieler arbeitet nicht eine Liste ab. Er reagiert auf eine Lage.

---

## Der Balken

### Grundstruktur

- Wertebereich: -100 bis +100
- Startwert: konfigurierbar pro Situation (oft leicht negativ, um dem Spieler ein Problem zu geben)
- Nullpunkt: Zentrum des Balkens
- Anzeige im Journal: visueller Balken mit negativem Ende (rot) und positivem Ende (grün)
- Der exakte Zahlenwert wird dem Spieler NICHT angezeigt — nur die Balkenposition
- Optionale beschreibende Labels am Balken (z.B. "angespannt" / "stabil" / "gelöst")

### Balkenbewegung

Der Balken bewegt sich durch drei Mechanismen:

**1. Aktive Events:** Story-relevante Szenen und Situations-Events, die der Spieler durch Exploration erlebt. Jedes Event hat einen definierten Effekt auf den Balken (positiv oder negativ, unterschiedliche Stärke).

**2. Passive Optionen:** Vom Spieler gewählte Langzeitstrategien (siehe eigener Abschnitt), die den Balken langsam in eine Richtung driften lassen.

**3. Natürlicher Drift:** Ohne Spielereingriff driftet der Balken langsam in Richtung negativ — Probleme lösen sich nicht von selbst. Die Driftgeschwindigkeit ist pro Situation konfigurierbar.

### Rückschwung

Der Balken kann in beide Richtungen schwingen. Fortschritt ist nicht permanent. Wenn der Spieler eine Situation vernachlässigt, driftet der Balken zurück Richtung negativ. Das gibt dem Spieler einen Grund, regelmäßig nach aktiven Situations zu sehen, ohne Zeitdruck zu erzeugen.

---

## Schwellensystem

Schwellen (Thresholds) sind definierte Punkte auf dem Balken, an denen etwas passiert. Es gibt zwei Typen:

### Auto-Fire-Schwellen

Wenn der Balken den Schwellenwert erstmals erreicht, wird automatisch ein Event ausgelöst. Der Spieler hat nichts Bestimmtes getan um dieses Event auszulösen — er hat verschiedene Dinge getan die den Balken bewegt haben, und als Konsequenz passiert etwas. Das fühlt sich organisch an.

**Verwendung:** Momente die als Reaktion auf den Gesamtfortschritt passieren sollen. Emiko meldet sich mit einer Idee. Ein Lehrer ändert seine Meinung. Schüler reagieren auf die veränderte Stimmung.

### Blocking-Schwellen

Der Balken kann nicht über diesen Punkt hinaus steigen, bis eine bestimmte Bedingung erfüllt ist. Diese Bedingung kann sein: ein spezifisches Event muss ausgelöst werden, eine Condition muss erfüllt sein (z.B. ProgressCondition, StatCondition), oder eine Kombination.

**Verwendung:** Narrativ kritische Beats die in einer bestimmten Reihenfolge passieren MÜSSEN. Die PTA-Abstimmung MUSS stattfinden. Das Lehrertreffen MUSS vor der PTA kommen. Der Spieler MUSS das Material schreiben. Blocking-Schwellen sind im Grunde Quest-Goals, die sich nicht wie Goals anfühlen.

### Zusammenspiel

Die narrative Reihenfolge ergibt sich automatisch aus der Schwellenposition auf dem Balken. Wenn das Lehrertreffen bei +15 liegt und die PTA bei +35, kann die PTA nicht vor dem Lehrertreffen stattfinden — der Balken erreicht +35 nicht vor +15. Die Kette existiert, der Spieler sieht sie nur nicht als Kette.

### Negative Schwellen

Auch auf der negativen Seite des Balkens können Schwellen liegen. Diese dienen als Warnsystem:

- **Blocking-Schwelle bei z.B. -25:** Der Balken stoppt kurz. Der Hinweistext warnt den Spieler: "Die Situation eskaliert. Handle jetzt oder die Chance ist vertan." Der Spieler hat ein Zeitfenster um gegenzusteuern.
- **Anders als positive Blocking-Schwellen:** Negative Blocking-Schwellen lösen sich nach einer definierten Zeit von selbst — wenn der Spieler nicht reagiert, rutscht der Balken weiter. Positive Blocking-Schwellen bleiben permanent bestehen bis die Bedingung aktiv erfüllt wird.

---

## Hinweissystem

Statt Goals und Tasks zeigt die Situation im Journal drei Dinge:

1. **Den Balken** mit seiner aktuellen Position
2. **Einen narrativen Hinweistext** der sich mit der Balkenposition ändert
3. **Die aktive passive Option** (falls vorhanden)

### Hinweistext-Logik

Jede Schwelle hat zwei Hinweistexte:

- **hint_approach:** Wird angezeigt solange der Balken UNTER der Schwelle liegt. Deutet vage die Richtung an, ohne den exakten Schritt zu verraten. Beispiel: "Die Lehrer scheinen offener für neue Ideen. Weiter so."
- **hint_reached:** Wird angezeigt wenn der Balken die Schwelle erreicht hat (bei Blocking-Schwellen). Sagt konkret was zu tun ist. Beispiel: "Die Lehrer erwarten einen Lehrplan-Entwurf. Arbeite im Büro daran."

Der Spieler sieht immer nur den Hinweistext der nächsten relevanten Schwelle. Unterhalb einer Schwelle sieht er hint_approach. Bei einer Blocking-Schwelle sieht er hint_reached. Zwischen zwei Schwellen (nach Überwindung einer Blocking-Schwelle) wechselt der Text zum hint_approach der nächsten.

### Unterschied zu Quest-Tasks

Eine Quest-Task sagt: "Geh ins Büro, wähl Arbeit, trigger Event X."
Ein Hinweistext sagt: "Die Lehrer erwarten einen Lehrplan-Entwurf."

Beides führt zum gleichen Ergebnis. Aber der Hinweistext lässt dem Spieler die Illusion der Entdeckung — er weiß WAS er tun soll, muss aber selbst herausfinden WO und WIE.

---

## Passive Optionen (Stellaris-Ansatz)

Jede Situation (außer Tutorial-Situations) bietet dem Spieler drei Strategien, von denen eine aktiv sein kann. Jede Option hat Vor- und Nachteile. Der Spieler kann jederzeit zwischen Optionen wechseln.

### Struktur einer passiven Option

- **Name und Beschreibung:** Was die Strategie repräsentiert
- **Balkendrift:** Richtung und Geschwindigkeit der passiven Balkenbewegung
- **Kosten:** Finanziell (monatlich/wöchentlich), zeitlich (Aktionsslots), oder keine
- **Nebeneffekte:** Stat-Modifikationen, Event-Frequenz-Änderungen, Auswirkungen auf andere Situations

### Design-Prinzipien

- Keine Option ist die "offensichtlich beste" Wahl
- Optionen repräsentieren unterschiedliche Philosophien, nicht unterschiedliche Effizienzgrade
- Eine Option sollte kostenlos sein (aber langsam oder mit Risiko)
- Optionen können Wechselwirkungen mit anderen Situations haben (strategische Tiefe)
- Tutorial-Situations haben KEINE passiven Optionen — der Spieler soll zuerst aktives Engagement lernen

### Einführung ins Spiel

Die erste Situation (Tutorial: "New Management") hat keine passiven Optionen. Die zweite Situation (z.B. "Cafeteria Crisis") führt die passiven Optionen ein — idealerweise narrativ durch Emiko oder den inneren Monolog des Protagonisten.

---

## Event-Injection

Situations injizieren temporäre Events in die bestehenden Gebäude-Pools. Diese Events existieren NUR während die Situation aktiv ist. Wenn die Situation resolved, verlassen sie den Pool.

### Mechanik

- Situations-Events haben selector_value 3 (Zufallspool) und koexistieren mit normalen Building-Events
- Der Spieler besucht ein Gebäude und bekommt ENTWEDER ein normales Event ODER ein Situations-Event
- Situations-Events bewegen den Balken und liefern gleichzeitig Content
- Wenn der Balken stark positiv ist, feuern positive Flavor-Events (Bestätigung)
- Wenn der Balken stark negativ ist, feuern negative Eskalations-Events (Warnung)
- Positive und negative Situations-Events füllen die Sandbox-Lücke zwischen Story-Beats

### Warum das den Grind reduziert

Das Hauptproblem bei Level 2-3 ist die dünne Event-Dichte: wenige neue reguläre Events, Story-Chains sind einmalig und sequenziell. Situations-Events lösen das, indem sie während ihrer Laufzeit die Pools temporär vergrößern. Die Sandbox fühlt sich voller an, ohne dass permanent mehr Events nötig sind.

### Balance: Gute vs. Schlechte Spieler

Sorge: Gute Spieler, die eine Situation schnell lösen, sehen weniger Content als schlechte Spieler, die mehr negative Events erleben.

Lösung: Situations-Events feuern UNABHÄNGIG von der Balkenrichtung. Es gibt positive Events (die bei positivem Balken feuern), negative Events (bei negativem Balken), und neutrale Events (die immer feuern). Gute Spieler sehen andere Events als schlechte — nicht weniger. Die Erfahrung ist anders, nicht ärmer.

Zusätzlich: Story-Schwellen-Events feuern auf JEDEM Weg zur Resolution. Der gute Spieler verpasst keine narrativen Beats — nur die Eskalationsszenen die bei Vernachlässigung auftreten.

---

## Stacking-Mechanik

Situations können sich stapeln. Es gibt kein hartes Limit für gleichzeitig aktive Situations. Die Konsequenz: ungelöste Situations häufen sich an und beeinflussen sich gegenseitig negativ.

### Natürlicher Schwierigkeitsgrad

- Mehr aktive Situations = mehr Events die Aufmerksamkeit fordern
- Passive Optionen mit Kosten summieren sich (finanzieller Druck)
- Negativer Drift in vernachlässigten Situations kann Kettenreaktionen auslösen
- Der Spieler hat einen natürlichen Anreiz, Situations aktiv zu lösen statt sie aufzuschieben

### Sicherheitsmechanismen

- Stat-Floors: Kein Stat kann durch Situations-Penalties allein unter einen Mindestwert fallen (z.B. 5 oder 10)
- Kaskadierende Resolution-Verzögerung: Wenn eine Situation negativ resolved, pausieren andere aktive Situations kurz ihre Timer — Atempause für den Spieler
- Story-getriebenes Pacing: Situations werden durch Story-Events ausgelöst, die bereits gebalanced sind — das natürliche Spieltempo verhindert extremes Stacking in normalem Spielverlauf

---

## Situations-Verkettung

Situations existieren nicht isoliert. Die Resolution einer Situation kann Bedingungen für nachfolgende Situations setzen.

### Mechanik

- Jede Resolution setzt Flags (z.B. `body_conflict_resolved = "positive"`)
- Nachfolgende Situations können diese Flags prüfen (als Startbedingung oder Balken-Startmodifikation)
- Positive Resolution einer früheren Situation kann den Startbalken einer späteren Situation verbessern
- Negative Resolution kann den Start verschlechtern oder zusätzliche Blocking-Schwellen hinzufügen

### Beispiel

"Social Sorting" (Level 1-2) resolved positiv → "Body Conflict" (Level 2) startet mit Balken bei -5 statt -20, weil die sozialen Grundlagen gelegt sind.

"New Management" (Tutorial) resolved positiv → spätere PTA-Situations starten mit leichtem Bonus, weil die Schule dem Headmaster vertraut.

---

## Resolution

Jede Situation hat eine positive und eine negative Resolution-Schwelle.

### Positive Resolution

Trigger: Balken überschreitet die positive Resolutions-Schwelle (nach Überwindung aller Blocking-Schwellen davor).

Effekte (situationsabhängig):
- Stat-Boni (Happiness, Inhibition, Education etc.)
- Flags für nachfolgende Situations
- Freischaltung neuer Events oder Event-Varianten
- Content-Belohnungen (Szenen die nur bei positiver Resolution spielbar sind)
- Finanzielle Effekte (reduzierte laufende Kosten, Einmalbonus)

### Negative Resolution

Trigger: Balken unterschreitet die negative Resolutions-Schwelle, ODER Timer läuft ab mit Balken unter einem Mindest-Schwellenwert.

Effekte (situationsabhängig):
- Stat-Penalties (Happiness-Drop, Inhibition-Anstieg etc.)
- Negative Flags für nachfolgende Situations
- Verschlossene Event-Varianten (die positive Version ist nicht mehr zugänglich)
- Finanzielle Konsequenzen (erhöhte laufende Kosten)
- Im Tutorial-Fall: Game Over

### Wichtig

Es gibt KEIN Level-Regression durch Situations. Die Konsequenzen sind Stat-Änderungen, Flags, und Content-Zugang — nie ein Level-Rückschritt.

---

## Integration mit dem PTA-System

PTA-relevante Freischaltungen (Regeln, Clubs, Gebäude) werden zu einem Subtyp: PTA-Situations.

### Unterschiede zur normalen Situation

**Drei Teilwerte statt einem Balken:**

Der Gesamtbalken setzt sich aus drei Komponenten zusammen — Lehrer-Zustimmung, Eltern-Zustimmung, Schüler-Zustimmung. Dem Spieler wird nur der Gesamtbalken angezeigt, aber der Hinweistext kann andeuten wo der Widerstand liegt ("Die Lehrer scheinen offen, aber die Eltern haben Bedenken").

Verschiedene Aktionen beeinflussen verschiedene Teilwerte:
- Gespräche mit Lehrern → Lehrer-Teilwert
- Adelaide helfen → Eltern-Teilwert
- Counseling mit Schülern → Schüler-Teilwert
- Allgemeine Arbeit (Office Work, Patrouille) → alle Teilwerte leicht

**Diskussions-Integration:**

Jeden Freitag, wenn eine PTA-Situation aktiv ist, feuert ein Diskussions-Fragment in der Diskussionsphase des PTA-Meetings. Der Inhalt hängt vom Balkenstand ab:
- Niedriger Balken: Thema stößt auf Widerstand, Gegenargumente, verschränkte Arme
- Mittlerer Balken: Sachliche Diskussion, einzelne Unterstützer, konstruktive Fragen
- Hoher Balken: Fast schon Vorabstimmung, Mehrheit ist überzeugt

Mehrere PTA-Situations können gleichzeitig Diskussions-Fragmente liefern — das Meeting wird lebendiger.

**Abstimmung als strategische Entscheidung:**

Der Spieler kann jederzeit eine Abstimmung planen, sobald die PTA-Situation aktiv ist. Die Erfolgswahrscheinlichkeit hängt direkt vom Balkenstand ab:
- Niedriger Balken (z.B. +10): ~30% Erfolg — hohes Risiko
- Mittlerer Balken (z.B. +30): ~60% Erfolg — machbar aber unsicher
- Hoher Balken (z.B. +50): ~85% Erfolg — wahrscheinlich
- Sehr hoher Balken (z.B. +65): ~95% Erfolg — fast sicher

Der Spieler entscheidet selbst, wann er bereit ist. Kein harter Gate — nur Risikomanagement.

**Scheitern der Abstimmung:**

Wenn die Abstimmung scheitert:
- Der Balken fällt um einen definierten Betrag zurück (z.B. -15)
- Die PTA ist skeptischer geworden — der nächste Versuch braucht mehr Überzeugungsarbeit
- Verhindert Spam-Strategie (jede Woche abstimmen lassen bis es klappt)
- Realistisch: eine abgelehnte Vorlage ist schwerer erneut einzubringen

**Nur ein Proposal pro Meeting:**

Wie bisher kann pro PTA-Meeting nur über ein Thema abgestimmt werden. Bei mehreren reifen PTA-Situations muss der Spieler priorisieren. Das gibt dem Freitagstermin strategisches Gewicht.

### Was das für bestehende PTA-Objekte bedeutet

- Journal-Regeln (school_jobs, theoretical_sex_ed, student_relations) werden zu PTA-Situations
- Die Condition-Kategorien (misc, social, feasibility, academic) werden durch die drei Teilwerte ersetzt
- Vote-Comments bleiben und werden in Diskussions-Fragmenten und Vote-Events genutzt
- Gebäude-Votes werden ebenfalls PTA-Situations, aber kürzer (weniger Meetings, niedrigere Schwellen)

---

## Integration mit Stats

Stats sollten Situations-Content flavorn, nicht gaten. Das bedeutet: Events innerhalb einer Situation feuern unabhängig von Stats, aber die VERSION des Events (Dialogvariante, Ausgang, Charakterreaktion) kann sich nach Stats richten.

### Stat-Rollen im Situations-Kontext

**Education:** Scorecard des Protagonisten. Steigt passiv wenn Happiness hoch ist. Beeinflusst wie Schüler mit Situations-Content interagieren (hohe Education = schärfere Fragen, bessere Einsichten).

**Happiness:** Frühwarnsystem. Sinkt bei negativen Situations-Entwicklungen. Niedrige Happiness macht Charaktere resistenter gegen positive Veränderungen — Events bei niedrigem Happiness haben rauere, weniger kooperative Varianten.

**Charm:** Sozialer Ansteckungsvektor. Hoher Charm bei einem Charakter beeinflusst Follower-Archetype-Charaktere in ihrem Umfeld. Relevant für Situations die auf soziale Dynamiken setzen (Body Conflict, Social Sorting).

**Inhibition & Corruption:** Die Lücke zwischen beiden Stats erzeugt vier Quadranten mit unterschiedlichen Event-Varianten:
- Hohe Corruption + Hohe Inhibition: will, aber schämt sich (Schuld-Variante)
- Niedrige Inhibition + Niedrige Corruption: körperlich offen, sexuell passiv (Body-Positive-Variante)
- Hohe Corruption + Niedrige Inhibition: will und schämt sich nicht (enthusiastische Variante)
- Niedrige Corruption + Hohe Inhibition: Baseline (konservative Variante)

**Reputation:** Noch nicht implementiert. Wenn es soweit ist, kann es als passiver Situations-Effekt eingebunden werden (bestimmte passive Optionen beeinflussen Reputation, PTA-Situations haben Reputations-Risiko).

**Money:** Kauft Gelegenheiten, nicht nur laufende Kosten:
- Passive Optionen mit Geldkosten
- Facility-Upgrades als Situations-Effekte (z.B. Gym-Renovierung beeinflusst Body-Conflict-Situation)
- School-Events als einmalige Investments (Strandausflug, Kulturfest)
- Gezielte Geschenke/Investitionen in Charaktere
- Potion-Zutaten als wiederkehrender Geld-Sink

### Stat-basierte passive Balkenbewegung

Nicht jedes Event kann einen manuellen Situations-Einfluss definieren — es gibt ~45+ reguläre Events, 4 Unterrichtsfächer mit Fragmenten, Office-Work, Counseling. Alle davon verändern Stats. Es wäre absurd, in jedem dieser Events manuell zu definieren welche Situations beeinflusst werden.

**Lösung:** Jede Situation definiert, welche Stats sie beeinflussen und mit welchem Gewicht.

Wenn `change_stats_with_modifier` aufgerufen wird, prüft der SituationManager nach der normalen Stat-Änderung alle aktiven Situations. Ist ein geänderter Stat für eine Situation relevant, wird ein kleiner Bruchteil der Änderung als Balkenbewegung übersetzt.

**Gewichtung pro Situation (Beispiele):**

Body Conflict:
- Happiness: Gewicht 1.0 (voller Einfluss, glücklichere Schüler = weniger toxische Dynamik)
- Inhibition: Gewicht 0.8, invertiert (sinkende Inhibition = Offenheit = Konflikt entschärft sich)
- Charm: Gewicht 0.3 (leichter Einfluss, soziale Kompetenz)
- Education: Gewicht 0 (irrelevant für diesen Konflikt)

Sex-Ed (PTA-Situation):
- Education: Gewicht 0.8 (bildungsaffine Schule = offener für neuen Lehrplan)
- Inhibition: Gewicht 0.6, invertiert
- Happiness: Gewicht 0.5
- Teilwerte differenzierbar: Education beeinflusst Lehrer-Teilwert stärker als Eltern-Teilwert

New Management (Tutorial):
- Alle Stats: Gewicht 0.3 (alles was die Schule verbessert, hilft dem Headmaster)

**Skalierung ist kritisch:**

Die Umrechnung von Stat-Änderung zu Balkenbewegung MUSS klein sein. Ein SMALL-Happiness-Boost bewegt den Balken vielleicht um +0.5 bis +1. Der stat-basierte Drift soll sich anfühlen wie Hintergrundgeräusch — er summiert sich über viele Events, ist aber nie der Haupttreiber. Der Spieler merkt: "Ich habe diese Woche viel patrouilliert und unterrichtet, und irgendwie hat sich die Situation verbessert, obwohl ich nichts Spezifisches dafür getan habe."

### Flag-System für Situations-Events

Drei Fälle bei Stat-Änderungen:

**Fall 1 — Normales Event ohne Situations-Bezug (Standardfall):**
Kein Flag. Die Stat-Änderung fließt automatisch in alle relevanten Situations über deren Gewichtungen. Betrifft die große Mehrheit aller Events. Der Event-Autor muss nichts über Situations wissen.

**Fall 2 — Situations-Event mit manuellem Balken-Push:**
Flag mit der zugehörigen Situation: "Dieses Event gehört zur Body-Conflict-Situation." Die Stat-Änderung beeinflusst NICHT die Body-Conflict-Situation automatisch (dort gilt der manuelle Push). Sie beeinflusst aber ALLE ANDEREN aktiven Situations normal über deren Gewichtungen.

Warum nicht komplett stumm schalten: Ein Body-Conflict-Event das Happiness erhöht, sollte die New-Management-Situation oder die Sex-Ed-Situation trotzdem mitbewegen. Nur die zugeordnete Situation wird ausgenommen, weil dort der Effekt manuell kontrolliert wird.

**Fall 3 — System-Event ohne Situations-Einfluss:**
Generelles "no situation influence" Flag. Für Events wie Gehaltsauszahlung, Lieferungen, oder technische System-Events die keinen narrativen Einfluss haben sollten.

**Integration in change_stats_with_modifier:**

Der bestehende Aufruf bleibt kompatibel. Ein optionaler Parameter wird ergänzt:

```
call change_stats_with_modifier('main',
    happiness = SMALL,
    charm = TINY,
    situation_exclude = "body_conflict"  # Optional: diese Situation nicht automatisch beeinflussen
) from _call_my_event_stats
```

Ohne `situation_exclude`: Fall 1 (alle Situations werden beeinflusst).
Mit `situation_exclude = "situation_key"`: Fall 2 (genannte Situation ausgenommen).
Mit `situation_exclude = "all"`: Fall 3 (keine Situation beeinflusst).

---

## Quest-System-Ersatz

Das Situation-System ersetzt das Quest-System vollständig für alle Story- und Help-Quests.

### Was durch Situations ersetzt wird

| Altes System | Neues System |
|---|---|
| Quest mit Goals und Tasks | Situation mit Balken und Schwellen |
| Goal-Checkliste im Journal | Narrativer Hinweistext |
| Task-Bedingung (EventTask, ConditionTask) | Blocking-Schwelle mit Event oder Condition |
| Quest-Fortschrittsanzeige (grün/rot) | Balkenposition |
| Effect-Ketten (QuestVisibleEffect → QuestActivateEffect) | Schwellen-Trigger |
| Help-Quests (Cafeteria, Schuljobs) | Kleine Situations mit kurzer Laufzeit |

### Was NICHT ersetzt wird

- **MaxGame-Quests** (max_stats, max_events): Reine Checklisten ohne Balken-Mechanik. Bleiben als separate Journal-Seite ("Fortschritt" oder "Sammlung")
- **Progress-System**: Bleibt parallel bestehen für Events die unabhängig von Situations funktionieren müssen

### Vorteile gegenüber dem Quest-System

- Flachere Architektur (Situation→Balken→Schwellen statt Quest→Goal→Task→Effects)
- Spieler bekommt Orientierung ohne Checkliste
- Sandbox-Philosophie bleibt erhalten
- Events zwischen Story-Beats bewegen den Balken (statt toter Raum)
- Passive Optionen geben dem Spieler strategische Tiefe
- Situations füllen Event-Pools temporär (weniger Grind)

---

## Journal-Darstellung

### Situations-Seite

Die Situations-Seite ersetzt die Quest-Seite im Journal. Anzeige:

- Liste aller aktiven Situations (links)
- Ausgewählte Situation (rechts): Titel, Beschreibung, Balken, aktueller Hinweistext, aktive passive Option mit Wechselmöglichkeit
- Abgeschlossene Situations: Kurze Zusammenfassung der Resolution (positiv/negativ)

### Balken-Darstellung

- Horizontaler Balken mit roter (links/negativ) und grüner (rechts/positiv) Einfärbung
- Marker für aktuelle Position
- Keine Zahlenwerte sichtbar
- Optional: beschreibende Labels an verschiedenen Balken-Positionen

---

## Potion-Testing als Mini-Situations (Rekurrierend)

Ein Sondertypus: bei jeder Serumverfeinerung öffnet sich eine kurze Mini-Situation die den Testerfolg trackt.

### Eigenschaften

- Kürzere Laufzeit als normale Situations (3-5 Events, wenige Tage)
- Kleinerer Balken-Bereich (z.B. -30 bis +30)
- Keine passiven Optionen (zu kurz)
- Charakteristiken ändern sich je nach Testparametern:
  - Test an Emiko (willige Testperson): engerer Balken, weniger Risiko, kürzere Laufzeit
  - Beimischung in Kaffee (mehrere Personen): breiterer Balken, mehr Risiko, längere Laufzeit
  - Test an spezifischer Schülerin: mittleres Risiko, charakterspezifische Events
- Frühe Tests: breitere Balken (mehr Unsicherheit, größere Ausschläge)
- Spätere Tests: engere Balken (Protagonist lernt dazu, Ergebnisse vorhersagbarer)
- Negative Resolution: Protagonist lernt aus Fehler (nächste Formel berücksichtigt Problem)
- Positive Resolution: Verfeinerungs-Fortschritt, nächste Potion-Stufe freigeschaltet

---

## Zusammenfassung der Architektur-Elemente

| Element | Funktion |
|---|---|
| **Situation** | Kern-Klasse, verwaltet Balken, Schwellen, passive Optionen, Event-Injection |
| **PTASituation** | Subtyp mit drei Teilwerten, Diskussions-Fragmenten, Vote-Integration |
| **Threshold** | Schwellenpunkt auf dem Balken mit Typ (auto_fire/blocking), Event/Condition, zwei Hinweistexten |
| **PassiveOption** | Strategie-Wahl mit Drift-Rate, Kosten, Nebeneffekten |
| **SituationManager** | Globaler Manager, prüft Schwellen, verwaltet aktive Situations, integriert in Event-System |

### Integration Points (Hooks ins bestehende System)

| Stelle | Integration |
|---|---|
| `begin_event` / `end_event` | Situations-Balken bewegen, Schwellen prüfen |
| `time_check_events` | Passive Drift anwenden, Auto-Fire-Schwellen prüfen, Timer für zeitlimitierte Situations |
| `map_overview` | Alle Schwellen prüfen, Situations-Events in Building-Pools registrieren |
| PTA-Meeting (Diskussionsphase) | PTA-Situations-Fragmente einfügen |
| PTA-Meeting (Abstimmungsphase) | Vote-Wahrscheinlichkeit aus Situations-Teilwerten berechnen |
| Journal UI | Situations-Seite rendern (Balken, Hinweise, passive Optionen) |
| Building Event Selection | Situations-Events im Pool berücksichtigen |
