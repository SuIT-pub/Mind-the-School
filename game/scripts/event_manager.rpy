#########################################
#   ----- Event Date Structure -----
#
# day.month.year.daytime.weekday.levels.isPrio
#
# all values can be changed with x, those will then fit all values. 
# ex.: 1.x.x.x.x.x:x:x.x will be available at anytime on the first of each month 
# 5.2.x.2.x.x:x:x.x will be available at any 5th febuary at noon
# the levels are represented by 3 values (high school, middle school and elementary school level)
# a level of 10 will be represented by an 'A'
# weekdays will be represented by a number with 1 representing monday, 2 tuesday, etc.
# 'd' and 'w' are also valid. 'd' stands for workdays and 'w' for weekends
# so x.x.x.x.d.x:x:x.x will always be available on monday to friday
# while x.x.x.x.w.x:x:x.x will only be available on saturday and sunday
# isPrio decides if the event will be played no matter what or if it only part of a randomized set
# if 1, it will be played in Order, if it is 0, it will only be part of a set where one event will be randomly selected


init -999 python:
    import re
    called_event = False

    def get_events_area_count(area, events):
        # try to narrow event-list down to area
        if area in events and area != "fallback":
            return get_events_count(events[area])

        return 0

    def get_level(level_val, school):
        
        if level_val == "x":
            return level_to_string(school)

        level_str = re.findall('\d+', level_val)
        if level_str:
            level = int(''.join(level_str))
            
            if ((level_val.endswith('-') and level_to_num(school) <= level) or
                (level_val.endswith('+') and level_to_num(school) >= level)
            ):
                return level_to_string(school)
            else:
                if '-' in level_val:
                    level_split = level_val.split('-')
                    if (len(level_split) == 2 and 
                        level_split[0].isdecimal() and 
                        level_split[1].isdecimal() and
                        int(level_split[0]) <= level_to_num(school) <= int(level_split[1])
                    ):
                        return level_to_string(school)
                elif ',' in level_val:
                    split_values = level_val.split(',')
                    split_values = [value.strip() for value in split_values]
                    if level_to_num(school) in split_values:
                        return level_to_string(school)

        return level_val

    def get_stat(stat_val, stat, school_name):
        
        school = get_school(school_name)

        if school == None:
            return stat_val

        if stat_val == "x":
            return school.get_stat_number(stat)

        stat_str = re.findall('\d+', stat_val)
        if stat_str:
            stats = int(''.join(stat_str))

            if ((stat_val.endswith('-') and school.get_stat_number(stat) <= stats) or
                (stat_val.endswith('+') and school.get_stat_number(stat) >= stats)
            ):
                return school.get_stat_string(stat)
            else:
                if '-' in stat_val:
                    stat_split = stat_val.split('-')
                    if (len(stat_split) == 2 and 
                        stat_split[0].isdecimal() and 
                        stat_split[1].isdecimal() and
                        int(stat_split[0]) <= school.get_stat_number(stat) <= int(stat_split[1])
                    ):
                        return school.get_stat_string(stat)
                elif ',' in stat_val:
                    split_values = stat_val.split(',')
                    split_values = [value.strip() for value in split_values]
                    if school.get_stat_number(stat) in split_values:
                        return school.get_stat_string(stat)

        return stat_val

    def get_events_count(events):
        event_amount = 0

        for key, value in events.items():
            my_values = key.split('.')

            if len(my_values) < 7:
                continue

            day     = my_values[0] if my_values[0] != "x" else str(time.day)
            month   = my_values[1] if my_values[1] != "x" else str(time.month)
            year    = my_values[2] if my_values[2] != "x" else str(time.year)
            daytime = my_values[3]

            if ((daytime == "c" and     time.daytime in [2, 4, 5]) or
                (daytime == "f" and     time.daytime in [1, 3, 6]) or
                (daytime == "n" and     time.daytime in [7]      ) or
                (daytime == "d" and not time.daytime in [7]      ) or
                (daytime == "x")
            ):
                daytime = str(time.daytime)

            weekday = my_values[4]

            if ((weekday == "d" and time.get_weekday_num() < 6) or
                (weekday == "w" and time.get_weekday_num() > 5) or
                (weekday == "x")
            ):
                weekday = str(time.get_weekday_num())

            levels  = my_values[5].split(':')
            levels[0] = get_level(levels[0], "high_school")
            levels[1] = get_level(levels[1], "middle_school")
            levels[2] = get_level(levels[2], "elementary_school")

            is_specific = my_values[6]

            if (day             == str(time.day)               and 
                month           == str(time.month)             and 
                year            == str(time.year)              and 
                daytime         == str(time.daytime)           and  
                weekday         == str(time.get_weekday_num()) and
                ':'.join(levels) == level_to_string()          and
                is_specific     == "0"
            ):
                event_amount += len(value)

        return event_amount
    
    def get_specific_temp_events(events):
        my_events = []
        for k in events:
            key_values = k.split('~')
            my_values = key_values[0].split('.')
            
            if len(my_values) < 6:
                continue

            day     = my_values[0] if my_values[0] != "x" else str(time.day)
            month   = my_values[1] if my_values[1] != "x" else str(time.month)
            year    = my_values[2] if my_values[2] != "x" else str(time.year)
            daytime = my_values[3]

            if ((daytime == "c" and     time.daytime in [2, 4, 5]) or
                (daytime == "f" and     time.daytime in [1, 3, 6]) or
                (daytime == "n" and     time.daytime in [7]      ) or
                (daytime == "d" and not time.daytime in [7]      ) or
                (daytime == "x")
            ):
                daytime = str(time.daytime)

            weekday = my_values[4]

            if ((weekday == "d" and time.get_weekday_num() < 6) or
                (weekday == "w" and time.get_weekday_num() > 5) or
                (weekday == "x")
            ):
                weekday = str(time.get_weekday_num())

            levels  = my_values[5].split(':')
            levels[0] = get_level(levels[0], "high_school")
            levels[1] = get_level(levels[1], "middle_school")
            levels[2] = get_level(levels[2], "elementary_school")

            if (day             == str(time.day)               and 
                month           == str(time.month)             and 
                year            == str(time.year)              and 
                daytime         == str(time.daytime)           and  
                weekday         == str(time.get_weekday_num()) and
                ':'.join(levels) == level_to_string()
            ):
                my_events.append((key_values[1], k))
        return my_events


    def get_specific_events(events):
        my_events = []
        for k, v in events.items():
            my_values = k.split('.')
            
            if len(my_values) < 7:
                continue

            day     = my_values[0] if my_values[0] != "x" else str(time.day)
            month   = my_values[1] if my_values[1] != "x" else str(time.month)
            year    = my_values[2] if my_values[2] != "x" else str(time.year)
            daytime = my_values[3]

            if ((daytime == "c" and     time.daytime in [2, 4, 5]) or
                (daytime == "f" and     time.daytime in [1, 3, 6]) or
                (daytime == "n" and     time.daytime in [7]      ) or
                (daytime == "d" and not time.daytime in [7]      ) or
                (daytime == "x")
            ):
                daytime = str(time.daytime)

            weekday = my_values[4]

            if ((weekday == "d" and time.get_weekday_num() < 6) or
                (weekday == "w" and time.get_weekday_num() > 5) or
                (weekday == "x")
            ):
                weekday = str(time.get_weekday_num())

            levels  = my_values[5].split(':')
            levels[0] = get_level(levels[0], "high_school")
            levels[1] = get_level(levels[1], "middle_school")
            levels[2] = get_level(levels[2], "elementary_school")

            is_specific = my_values[6]

            if (day             == str(time.day)               and 
                month           == str(time.month)             and 
                year            == str(time.year)              and 
                daytime         == str(time.daytime)           and  
                weekday         == str(time.get_weekday_num()) and
                ':'.join(levels) == level_to_string()          and
                is_specific     == "1"
            ):
                my_events.extend(v)
        return my_events

    def get_unspecific_events(events):
        my_events = []
        for k, v in events.items():
            my_values = k.split('.')

            if len(my_values) < 7:
                continue

            if my_values[0] != "x" or my_values[1] != "x" or my_values[2] != "x":
                continue

            day     = my_values[0] if my_values[0] != "x" else str(time.day)
            month   = my_values[1] if my_values[1] != "x" else str(time.month)
            year    = my_values[2] if my_values[2] != "x" else str(time.year)
            daytime = my_values[3]

            if ((daytime == "c" and     time.daytime in [2, 4, 5]) or
                (daytime == "f" and     time.daytime in [1, 3, 6]) or
                (daytime == "n" and     time.daytime in [7]      ) or
                (daytime == "d" and not time.daytime in [7]      ) or
                (daytime == "x")
            ):
                daytime = str(time.daytime)

            weekday = my_values[4]

            if ((weekday == "d" and time.get_weekday_num() < 6) or
                (weekday == "w" and time.get_weekday_num() > 5) or
                (weekday == "x")
            ):
                weekday = str(time.get_weekday_num())

            levels  = my_values[5].split(':')
            levels[0] = get_level(levels[0], "high_school")
            levels[1] = get_level(levels[1], "middle_school")
            levels[2] = get_level(levels[2], "elementary_school")

            is_specific = my_values[6]

            if (day             == str(time.day)               and 
                month           == str(time.month)             and 
                year            == str(time.year)              and 
                daytime         == str(time.daytime)           and  
                weekday         == str(time.get_weekday_num()) and
                ':'.join(levels) == level_to_string()          and
                is_specific     == "0"
            ):
                my_events.extend(v)
        return my_events

#################################################################
# try to run event from event-set depending on area, time and day
label event_check_area(area, events):
    $called_event = False

    # try to narrow event-list down to area
    if area in events and area != "fallback":
        call event_check(events[area])

    # if area has no usable event or area is invalid goto fallback event
    if "fallback" in events and not called_event:
        call expression events["fallback"]
    return

###########################################################
# try to run event from event-set depending on time and day
label event_check(events):

    # check for events running only on specific day
    $ my_events = get_specific_events(events)
    if my_events:
        $ i = 0
        while(len(my_events) > i):
            call expression my_events[i]
            $ i += 1
        $ called_event = True
        return

    # check for events that can run on any day
    $ my_events = get_unspecific_events(events)
    if my_events:
        $ called_event = True
        call expression renpy.random.choice(my_events)
        return

    # run fallback event when no other events have been called
    if "fallback" in events:
        $ called_event = True
        call expression events["fallback"]
        return

    return

label temp_event_check(events):

    # check for events running only on specific day
    $ my_events = get_specific_temp_events(events)
    if my_events:
        $ i = 0
        while(len(my_events) > i):
            $ events.remove(my_events[i][1])
            call expression my_events[i][0]
            $ i += 1
        $ called_event = True

        $ temp_time_check_events = events

        return

    return