####################################################################################
## This script is a modified version of the original script by Remix              ##
####################################################################################
## MIT License                                                                    ##
##                                                                                ##
## Copyright (c) 2020 Remix                                                       ##
##                                                                                ##
## Permission is hereby granted, free of charge, to any person obtaining a copy   ##
## of this software and associated documentation files (the "Software"), to deal  ##
## in the Software without restriction, including without limitation the rights   ##
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      ##
## copies of the Software, and to permit persons to whom the Software is          ##
## furnished to do so, subject to the following conditions:                       ##
##                                                                                ##
## The above copyright notice and this permission notice shall be included in all ##
## copies or substantial portions of the Software.                                ##
##                                                                                ##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     ##
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       ##
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    ##
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         ##
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  ##
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  ##
## SOFTWARE.                                                                      ##
####################################################################################
####################################################################################

# Global list of notifications
default notify_messages = []

# Duration the full ATL takes
default notify_duration = 8

# Max number we store for reviewing in the history screen
default notify_history_length = 20

default stat_notifications = {}

init -99 python:
    import time as time_lib

    def add_stat_notification(char: str, stat: str, value: int):
        key = char + ":" + stat
        if key not in stat_notifications:
            stat_notifications[key] = 0
        stat_notifications[key] += value

    def reset_stat_notifications():
        global stat_notifications
        stat_notifications = {}

    def add_notify_message(msg=None):
        if not msg:
            return

        global notify_messages

        notify_messages.append((msg, -1))

        # just keep notify_history_length number of messages
        notify_messages = notify_messages[-notify_history_length:]

    def finish_notify(trans, st, at):
        global notify_messages
        global notify_duration

        max_start = time_lib.time() - 4

        notify_messages = [n for n in notify_messages if n[1] > max_start]

        if not [k for k in notify_messages if k[1] > max_start]:

            # If the notification list is now empty, hide the screen
            renpy.hide_screen("notify_container")
            renpy.restart_interaction()

        return None

    def call_notify():
        global notify_messages

        max_start = time_lib.time() - 4

        for key in stat_notifications.keys():
            value = stat_notifications[key]
            char, stat = key.split(":")
            char_name = char
            char_obj = get_character_by_key(char)
            if char_obj != None:
                char_name = char_obj.get_title()

            notify_str = char_name + ": " + get_stat_icon(Stat_Data[stat].get_title(), size = ICON_XSMALL)
            notify_val = " {color=#00a000}" + "{:.2f}".format(value) + "{/color}"
            if ((value > 0 and stat == "inhibition") or (value < 0 and stat != "inhibition")):
                notify_val = " {color=#a00000}" + "{:.2f}".format(value) + "{/color}"
            add_notify_message(notify_str + " " + notify_val)

        reset_stat_notifications()

        for i in range(len(notify_messages)):
            
            if notify_messages[i][1] == -1:
                notify_messages[i] = (notify_messages[i][0], time_lib.time())

                if i > 0 and notify_messages[i-1][1] >= notify_messages[i][1]:
                    notify_messages[i] = (notify_messages[i][0], notify_messages[i][1] + 0.01)

        notify_messages = [n for n in notify_messages if n[1] > max_start]

        renpy.show_screen('notify_container')

        renpy.restart_interaction()



style notify_item_frame:

    background Frame("gui/notify.png", 10, 10)

    padding (16, 2, 32, 2)
    minimum (20,20)
    # xanchor 0.5


style notify_item_text:

    xsize None 
    align (0.5,0.5) 

    # just standard font specific stuff
    color "#FFF"
    outlines [(abs(2), "#000", abs(0), abs(0))]
    # font ""
    size 20


transform notify_appear():

    yzoom 0.0 alpha 0.5

    linear 0.2 yzoom 1.0 alpha 1.0

    pause 4.0

    linear 0.2 yzoom 0.0 alpha 0.0

    function finish_notify


screen notify_item(msg, use_atl=True):

    style_prefix "notify_item"

    frame:

        if use_atl: # ATL not used for history

            at notify_appear

        # else:
        #     xpos 0.5

        text msg


screen notify_container():

    fixed:

        pos (0, 10)

        vbox:

            xmaximum 400
            spacing 5

            # We index on the time the notification was added as that
            # is unique. Using index helps manage the ATL nicely
            for msg_info in notify_messages:

                if msg_info[1] > time_lib.time() - notify_duration:

                    use notify_item(msg_info[0])


screen notify_history():

    viewport:
        area (0, 150, 320, 380)
        # scrollbars "vertical"
        draggable True
        mousewheel True
        yinitial 1.0

        vbox:
            xfill True
            spacing 5

            for msg_info in notify_messages:

                use notify_item(msg_info[0], False)