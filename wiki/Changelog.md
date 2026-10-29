# Changelog

Every released version of Mind the School, newest first. The game's main menu shows
the latest few under **What's new**; this page keeps the full history.

---

## Bugfix Update 0.2.1B_1

- Made a small optimization, reducing the size of save files
- Fixed a mixup of yoga outfit numbers
- Fixed missing images in an event

## Minor Update 0.2.1B

- Fixed missing character names in some events
- Fixed some stat changes missing in some events

## Minor Update 0.2.1A

- Fixed the Truth or Dare event chain not triggering
- Fixed the New Yoga Outfit event chain not triggering
- Fixed some keywords not being named correctly
- Added missing events and images for sex ed teaching
- Added a debug feature in the journal for reading in-game values

## Major Update 0.2.1

### Stats

- 1379 new images, bringing the total to 7233
- 21 new animations, bringing the total to 203
- 2 new event chains
- 20 new events, one of them with over 12 fragments

### Events

- Added an event chain for new yoga outfits
  - 10 new events
- Added an event chain for Truth or Dare
  - 4 new events
  - 12 new event fragments
- 2 new events in the gym
- 2 new events in the school building
- 1 new event in the office building
- Reworked teaching P.E. classes to fit the new image creation workflow
- Improved composite events to allow easier use of fragments

### New features

- Added ambient sound to the map and the location overview

### Changes

- Changed the methods for creating menus
- Unified the stat sets of students, parents and teachers into one single set
- Reworked the PTA voting system

### Stats system

- Stats for students, teachers and parents have been merged into one set representing the entire school
- Each party keeps its own set of stats for compatibility reasons
- None of these sets are in use except the student set, which is now the main set
- All parties still keep their own progression level

### PTA

- The voting system and probability calculation have been overhauled to match the new stat system
- Instead of all parties voting on the same set of conditions based on their own stats, each party now votes on its own set of conditions together with one shared set
- The probability calculation has been simplified
- The calculation is still in a testing phase
  - The probability shown in the journal may not match the one measured in the PTA itself
  - The journal's probability is based on the voting probability of all three parties, while in the PTA each party calculates its own probability separately

### Characters

- Introducing Linh Nguyen
- Enhanced character retrieval for use in events

### GUI

- Added a button to skip to the next day in the map overview
- The main menu background can now be switched between different animations
- The main menu background can now be switched between animated and static

### Quest system

- Updated the quest system to include the new events
- A rework of the quest system is planned for 0.2.2, so please don't report bugs related to the quest system; they will be worked on in the next big update
- The quest system only reflects the current state of the game and has no influence on it, so events still work even if the quest system doesn't update

### Misc

- Fixed multiple bugs

---

## Minor Update 0.2.0C

- Added live notifications to the main menu
- Fixed the replay gallery crashing to the map overview when handling decisions during a replay
- Fixed events in the school dorm and school building showing at levels they are not planned for
- Fixed missing images in a school dorm event

## Quick Fix 0.2.0B_1

- Fixed an event in the courtyard showing at a level it is not planned for
- Fixed an error in the gym after level 6 has been reached

## Minor Update 0.2.0B

- Fixed missing thumbnails for quests
- Fixed tutorials repeating and not returning to the correct screen
- Fixed missing animations during the P.E. teaching warm-up
- Fixed a missing image in the school dorm "Walk in on Girl" event
- Temporary fix for certain buildings or rules having their probabilities calculated incorrectly: they are now 100% by default

## Quick Fix 0.2.0A_1

- More fixes for the probability calculation

## Quick Fix 0.2.0A

- Fixed a bug preventing the player from queueing the rule to progress to level 4 and higher
- Small changes to the probability calculation for unlockables (the calculation is still a work in progress)
- Fixed mods not being registered correctly

## Major Update 0.2.0

### Stats

- 3445 more images, bringing the total to 5815
- 54 more animations, bringing the total to 182
- 18 new events

### Events

- Added an event chain for transitioning the school to level 2
  - 13 new events in the transition event chain
- 2 new events in the cafeteria
- 1 new event in the courtyard
- 2 new events in the school dormitory
- Fully reworked all 71 regular events and created variants of them for every school level up to level 10
  - Some events now have a spicy animation at the higher levels
  - This was done to fit the events to my new (and hopefully last) workflow for rendering images, which for the first time let me render the events for all levels
- Events can now have priority over other events
- The higher-level variants of the events can be seen thanks to temporary rules that let the player raise the school level above 2

### New features

- Implemented a modding framework
- Implemented a new quest system
- Implemented a character overview
- Reworked the main menu

### Changes

- Reworked the journal design
- Improved the map
- Improved the PTA event system

### Gallery

- Because all events were reworked, the existing replay gallery data will be wiped
- Added versioning for the gallery and for individual events

### Modding

- A new modding framework has been added
- It allows the creation of new events, characters and more
- A manual on how to create a mod can be found in the [Modding](Modding) guide
- Added a mod manager to the main menu for activating and deactivating mods

### Quests

- A quest system has been implemented for you clueless folks
- The new quest overview can be found in the journal
- The overview shows quests for solving the current event chains
- Clicking the small info button in the quest overview displays more quests
  - These quests help with unlocking certain things or give a general overview of which events have been seen
- Some quests might not update correctly or might have display issues when using save games from old versions

### Character overview

- A character overview can now be found in the journal (thanks to Shojua for suggesting it; if you have ideas yourself, leave your suggestion on the Discord)
- The overview lists all regular in-game characters
- Clicking a character shows a detailed overview of that character together with a small image gallery
- An image marked as favorite becomes that character's thumbnail in the overview

### Main menu

- The main menu has been made nicer
- An animated background has been added

### School map

- The school map has changed its highlighting
- Locations that have an event are now highlighted with a marker
- Pin-style markers have been added to better show where the different facilities are

### Journal

- When a proposal that costs money is queued, that money is put aside until the vote, so money meant for the proposal can't be spent elsewhere
- Added temporary rules that let the player raise the game's level up to the maximum of 10

### Misc

- Tons of bug fixes

### Note for save games from 0.1.4 and before

I made sure to keep all save files created from 0.1.2 onwards compatible. Old saves
should have no problems loading. For the selection of the new proficiencies, you'll
get a prompt to select one.

**Important:** you may get an error while loading, telling you that an image file
couldn't be loaded. In that case, just click **Ignore**. You'll get a missing
background in the proficiency selection, but after that everything should work
properly. If the school map looks a bit buggy after loading, that fixes itself after
entering a location or opening the journal.

These are all visual bugs. They only occur directly after loading an old game and
won't influence or corrupt the game itself. If you run into bugs not listed here,
hit me up wherever you like, but preferably on Discord 🙂

---

## Minor Update 0.1.4C

- Added a changelog to the main menu
- Added social media buttons to the main menu
- Disabled the cafeteria upgrade
- Fixed a wrong label used in the Aona bra event
- Fixed a missing image in one of the cafeteria events

## Quick Fix 0.1.4A_1

- Fixed an error preventing some people from entering the office
- A quick patch for 0.1.4A was shared on Discord

## Quick Fix 0.1.4A

- Fixed an error when loading an old save game saved during an event
- Small cleanup of the game distribution

## Major Update 0.1.4

- Added 1242 images, doubling the image count to 2370 in total
- Added 128 new animations (most of them for the movie sandbox)
- Added about 10 new regular events
- Added about 5 new work events
- Added some repeatable naughty time with the secretary
- Improved the notification system
- Improved the image system
- Improved the gallery system
- Implemented event composites
- Introduced subject proficiencies for the headmaster
- Introduced a new subject: History
- Introduced the movie sandbox system
- Reworked the tutorial
- Reworked the school map
- Reworked the journal
- Reworked the stat changes of some events to make them less brutal
- Tons of prep work needed for a special project planned for 0.1.5
- Lots of bug fixing
- Lots of improvements to existing systems in the game code

### Note for save games from 0.1.3

I made sure to keep all save files created from 0.1.2 onwards compatible. Old saves
should have no problems loading. For the selection of the new proficiencies, you'll
get a prompt to select one.

**Important:** you may get an error while loading, telling you that an image file
couldn't be loaded. In that case, just click **Ignore**. You'll get a missing
background in the proficiency selection, but after that everything should work
properly. If the school map looks a bit buggy after loading, that fixes itself after
entering a location or opening the journal.

These are all visual bugs. They only occur directly after loading an old game and
won't influence or corrupt the game itself. If you run into bugs not listed here,
hit me up wherever you like, but preferably on Discord 🙂

---

## Minor Update 0.1.3B

- Fixed a crash when the game tries to download the supporter list without an internet connection
- Added the option to turn off downloading the supporter list in the settings; the internal list is used instead
- Possibly fixed a crash on macOS (I can't really test that, so only hope remains)
- Fixed a typo
- Made the bento event more likely to fire

## Major Update 0.1.3

- **Cafeteria:** introduced the cafeteria
- **Cafeteria:** added 6 events to the cafeteria
- **Cafeteria:** added a new rule for the cafeteria and other things (Adelaide seems to be stressed sometimes…)
- **Courtyard:** added 3 events to the courtyard
- **School building:** added 3 new events to the school building
- **School building:** introduced a new introduction event when teaching a class for the first time
- **Gym:** added a new teaching event
- **PTA:** extended the PTA introduction to introduce all teachers and parents
- **Characters:** all the different schools have been merged into one school with different classes. No more stat grinding for every school
- **Journal:** added a budget overview. Always keep your money in check (new ways to earn money come with the next update)
- **Journal:** added a replay gallery to the journal (bottom right tab)
- **Locations:** replaced the background images of all locations
- **Events:** introduced a new system for determining the values and data used by events, particularly useful for adding new events or modding; the gallery uses it too
- **Image system:** improved the image system for more dynamic usage
- **UI:** small changes to the UI for better aesthetics
- **QoL:** added more information to the journal so players aren't confused about what can be unlocked and what can't
- **QoL:** added a bit of extra information during the introduction phase
- **QoL:** special events are now marked: the location glows red and the action is marked with red dots, to show where to find the event
- **Bugfix:** fixed a softlock during the introduction phase when saving and loading (hopefully)
- **Bugfix:** fixed temporary events being replayed when they shouldn't be
- **Known bug:** selecting a value in the gallery sometimes causes an error. I wasn't able to determine why, but it is harmless: just roll back once and it's fixed

## Minor Update 0.1.2B

- Changed the vote button in the journal to show whether a rule (or club, or building) can be unlocked or isn't implemented yet
- Added text to the descriptions of some rules, clubs and buildings, stating that they are not yet implemented and cannot be voted on
- Some events were planned and their dialogue implemented in advance. They shouldn't have been visible yet, as they are meant for later stages of the game. They are now locked and inaccessible, since they are missing images and are subject to change
- Changed the probability of voting on rules and other issues. Each party now has a base probability of 100% if the necessary requirements are fully met. Students, teachers and parents have different stats, so they must be raised separately. Parents' stats can't be raised yet, and the stats of teachers and parents can't be viewed yet; this will change in 0.1.3. The currently unlockable rule can be unlocked relatively easily. The whole vote calculation is subject to change in 0.1.3
- Fixed an event in the office that still fired although it was supposed to be obsolete after a certain rule passed
- Changed the wording of a single sentence in the intro so it makes more sense, both in content and grammar

Because many people were grinding hard to unlock and view things that weren't even
implemented yet, I also added:

- A message shown after the player has watched all events that can be watched. Some events have multiple variants with different images, which are not tracked, so search for them at your own risk
- A message that appears once the stats reach a level beyond which raising them is no longer necessary, because there is nothing new to see or unlock. It pops up once **all** stats have reached that threshold, not for each individual stat: if you only raise Corruption and leave the rest as they are, the message won't appear

## Major Update 0.1.2

- **Events:** 19 new regular events; you find them by visiting various locations and doing stuff
- **UI:** you can now use keyboard shortcuts to visit locations, select options, skip time and open the journal, with various settings for them in the preferences
- **Images:** each character now has their own unique clothing and name

19 new regular events, ~2000 new words, over 400 new images.

**Old save games are NOT compatible!**

## Minor Update 0.1.1A

- **Events:** not really an event, but I added a small epilogue sequence at the end of the game introduction. The previous description of the role the potion will play in the game didn't seem clear enough, so this new sequence hopefully clears that up a bit 🙂
- **Characters:** the characters now have names!
- **UI:** the ability to hide the GUI has been re-added after making it work properly
- **UI:** added transitions between images. You can disable them or change their speed in the preferences, if you like your juicy transitions a bit faster
- **UI:** the textbox background can now be changed in the preferences as well: original, 50% transparency or no box at all
- **Images:** the image format has been changed, reducing the final size by ~70%
- **Bugs:** the headmaster's name was not used consistently throughout the game; this has been fixed
- **Bugs:** there seemed to be a case where images were missing. I found something that could have caused it and fixed it, but I can't confirm it's definitely fixed, as I can't reproduce the problem
- **Bugs:** the first event on day 1 sometimes didn't fire, and the player was thrown into free roaming with nothing to do until day 2. I couldn't reproduce that either, but the other events worked fine for the reporter, so I changed the way the day 1 events are called

## Version 0.1.1

The introduction to the game, up until the free-roaming phase.

- Tutorial
- Background images for free roaming
- 413 images, 8 animations, 6000 words
