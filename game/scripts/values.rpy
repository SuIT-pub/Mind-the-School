init python:
    # 0 = no loli content (High School age: 18-22)
    # 1 = slight loli content (Middle School age: 13-17, High School age: 18-22)
    # 2 = hard loli content (Elementary School age: 8-12, Middle School age: 13-17, High School age: 18-22)
    loli_content = 0
    cheat_mode = False
    nude_vision = 2

    def set_game_data(key, value):
        gameData[key] = value

    def start_progress(key):
        gameData[key] = 1

    def advance_progress(key, delta = 1):
        if key not in gameData.keys():
            gameData[key] = 0
        gameData[key] += delta

    def get_progress(key):
        if key not in gameData.keys():
            return -1
        return gameData[key]

    def get_game_data(key):
        if key in gameData.keys():
            return gameData[key]
        return None

    def contains_game_data(key):
        return key in gameData.keys()

    def get_image_with_level(image_path, level):

        path = image_path.replace("<nude>", "0")

        for i in reversed(range(0, level + 1)):
            image = path.replace("<level>", str(i))
            if renpy.loadable(image):
                return image_path.replace("<level>", str(i))
        for i in range(0, 10):
            image = path.replace("<level>", str(i))
            if renpy.loadable(image):
                return image_path.replace("<level>", str(i))
        
        return image_path

    def get_random_school():
        return get_random_choice("high_school", "middle_school", "elementary_school")

    def get_random_choice(*choice):
        return renpy.random.choice(list(choice))

    def log_val(key, value):
        print(key + ": " + str(value))

    def log(msg):
        print(msg)
       

default intro_dev_message = "This version of the game only includes content up to day 10, when free roaming begins. You can still play and roam from there, but there will be no content."


default rules = {}
default buildings = {}
default clubs = {}
default charList = {
    'schools': {},
    'staff': {},
}
default money = Stat("money", 1000)
default time = Time()
default stat_data = {}
default gameData = {}

default character.dev = Character(
    "Suit-Kun",
    who_color = "#00ff11",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.principal = Character(
    "Principal",
    who_color = "#ffffff",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.principal_whisper = Character(
    "Principal",
    who_color = "#ffffff",
    what_color = "#ffffff",
    what_size = 15,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.principal_shout = Character(
    "Principal",
    who_color = "#ffffff",
    what_color = "#ffffff",
    what_size = 35,
    what_outlines=[( 1, "#000000", 0, 0 )],
)
default character.principal_thought = Character(
    "Principal",
    who_color = "#ffffff",
    what_color = "#ffffff",
    what_size = 28,
    italics = True,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.secretary = Character(
    "Secretary",
    who_color = "#c71585",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.secretary_whisper = Character(
    "Secretary",
    who_color = "#c71585",
    what_color = "#ffffff",
    what_size = 15,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.secretary_shout = Character(
    "Secretary",
    who_color = "#c71585",
    what_color = "#ffffff",
    what_size = 35,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.teacher = Character(
    "Teacher", 
    who_color = "#00ced1",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.parent = Character(
    "Parent",
    who_color = "#e6e6fa",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0)],
)
default character.examiner = Character(
    "Examiner",
    who_color = "#f5deb3",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.regional = Character(
    "Region Manager",
    who_color = "#4169e1",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.sgirl = Character(
    "School Girl",
    who_color = "#8a2be2",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.sboy = Character(
    "School Boy",
    who_color = "#008000",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.crowd = Character(
    "Crowd",
    what_color = "#ffd700",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.crowd_whisper = Character(
    "Crowd",
    what_color = "#ffd700",
    what_size = 15,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.crowd_shout = Character(
    "Crowd",
    what_color = "#ffd700",
    what_size = 35,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.subtitles = Character(
    None,
    # window_background = None,
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
    what_xalign = 0.5,
    what_textalign = 0,
    what_layout = 'subtitle'
)
default character.subtitles_Empty = Character(
    None,
    window_background = None,
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
    what_xalign = 0.5,
    what_textalign = 0,
    what_layout = 'subtitle'
)

default character.nv_text = Character(None, kind=nvl, what_text_align=0.5, what_xalign=0.5)
