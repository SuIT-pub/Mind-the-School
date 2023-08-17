init -6 python:
    import re
    class Rule:
        def __init__(self, name, title):
            self._name = name
            self._title = title
            self._description = ""
            self._image_path_alt = "images/journal/empty_image.png"
            self._image_path = "images/journal/empty_image.png"
            self._unlocked = {
                "high_school": False,
                "middle_school": False,
                "elementary_school": False,
            }
            self._unlock_conditions = []

        def _update(self, title, data = None):
            if data != None:
                self.__dict__.update(data)

            self._title = title

            if not hasattr(self, '_description'):
                self._description = ""
            if not hasattr(self, '_image_path'):
                self._image_path = "images/journal/empty_image.png"
            if not hasattr(self, '_image_path_alt'):
                self._image_path_alt = "images/journal/empty_image.png"
            if not hasattr(self, '_unlocked'):
                self._unlocked = {
                    "high_school": False,
                    "middle_school": False,
                    "elementary_school": False,
                }
            if not hasattr(self, '_unlock_conditions'):
                self._unlock_conditions = []
        
        def get_name(self):
            return self._name

        def get_title(self):
            return self._title

        def get_type(self):
            return "rule"

        def get_description(self):
            return self._description

        def get_image(self, school, level):
            for i in reversed(range(0, level + 1)):
                image = self._image_path.replace("<school>", school).replace("<level>", str(i))
                if renpy.exists(image):
                    return image
            for i in range(0, 10):
                image = self._image_path.replace("<school>", school).replace("<level>", str(i))
                if renpy.exists(image):
                    return image
            return self._image_path_alt

        def get_full_image(self, school, level):
            image = self.get_image(school, level)
            full_image = image.replace(".", "_full.")

            if renpy.exists(full_image):
                return full_image
            return None



        def unlock(self, school, unlock = True):
            if school in self._unlocked:
                self._unlocked[school] = unlock

        def is_unlocked(self, school):
            if school in self._unlocked:
                return self._unlocked[school]
            else:
                return False

        def is_visible(self, school):
            for condition in self._unlock_conditions:
                if condition.is_blocking(school):
                    return False
            return True

        def can_be_unlocked(self, school):
            if school not in schools.keys():
                return False

            for condition in self._unlock_conditions:
                if condition.is_fullfilled(school):
                    continue
                return False

            return True

        def get_list_conditions(self):
            output = []
            for condition in self._unlock_conditions:
                if not condition.is_set_blocking() and condition.display_in_list:
                    output.append(condition)

            return output

        def get_desc_conditions(self):
            output = []
            for condition in self._unlock_conditions:
                if not condition.is_set_blocking() and condition.display_in_desc:
                    output.append(condition)

            return output


    #############################################
    # Rules Global Methods
    
    def get_unlocked_rules_by_school(school):
        output = []

        for rule in rules.values():
            if rule.is_unlocked(school) and rule.get_name() not in output:
                output.append(rule.get_name())
        
        return output

    def get_visible_unlocked_rules_by_school(school):
        output = []

        for rule in rules.values():
            if (rule.is_visible(school) and 
            rule.is_unlocked(school) and
            rule.get_name() not in output):
                output.append(rule.get_name())

        return output

    def get_visible_locked_rules_by_school(school):
        output = []

        for rule in rules.values():
            if (rule.is_visible(school) and 
            not rule.is_unlocked(school) and
            rule.get_name() not in output):
                output.append(rule.get_name())

        return output

    def get_visible_rules_by_school(school, include_unlocked = False):
        output = []

        for rule in rules.values():
            if (rule.is_visible(school) and 
            (not rule.is_unlocked(school) or include_unlocked) and
            rule.get_name() not in output):
                output.append(rule.get_name())

        return output
    
    def get_visible_unlocked_rules():
        output = []

        for rule in rules.values():
            if (rule.is_visible("high_school") and 
            rule.is_unlocked("high_school") and
            rule.get_name() not in output):
                output.append(rule.get_name())
                continue
            
            if loli_content >= 1:
                if (rule.is_visible("middle_school") and 
                rule.is_unlocked("middle_school") and
                rule.get_name() not in output):
                    output.append(rule.get_name())
                    continue

            if loli_content == 2:
                if (rule.is_visible("elementary_school") and 
                rule.is_unlocked("elementary_school") and
                rule.get_name() not in output):   
                    output.append(rule.get_name())
                    continue

        return output

    def get_visible_locked_rules():
        output = []

        for rule in rules.values():
            if (rule.is_visible("high_school") and 
            not rule.is_unlocked("high_school") and
            rule.get_name() not in output):
                output.append(rule.get_name())
                continue
            
            if loli_content >= 1:
                if (rule.is_visible("middle_school") and 
                not rule.is_unlocked("middle_school") and
                rule.get_name() not in output):
                    output.append(rule.get_name())
                    continue

            if loli_content == 2:
                if (rule.is_visible("elementary_school") and 
                not rule.is_unlocked("elementary_school") and
                rule.get_name() not in output):   
                    output.append(rule.get_name())
                    continue

        return output

    def get_visible_rules(include_unlocked = False):
        output = []

        for rule in rules.values():
            if (rule.is_visible("high_school") and 
            (not rule.is_unlocked("high_school") or include_unlocked) and
            rule.get_name() not in output):
                output.append(rule.get_name())
                continue
            
            if loli_content >= 1:
                if (rule.is_visible("middle_school") and 
                (not rule.is_unlocked("middle_school") or include_unlocked) and
                rule.get_name() not in output):
                    output.append(rule.get_name())
                    continue

            if loli_content == 2:
                if (rule.is_visible("elementary_school") and 
                (not rule.is_unlocked("elementary_school") or include_unlocked) and
                rule.get_name() not in output):   
                    output.append(rule.get_name())
                    continue

        return output

    def get_unlockable_rules():
        output = []

        for rule in rules.values():
            high_unlock = rule.can_be_unlocked("high_school")
            high_unlocked = rule.is_unlocked("high_school")

            if (high_unlock and 
            not high_unlocked and 
            rule.get_name() not in output):
                output.append(rule.get_name())
                continue

            if loli_content >= 1:
                middle_unlock = rule.can_be_unlocked("middle_school")
                middle_unlocked = rule.is_unlocked("middle_school")

                if (middle_unlock and 
                not middle_unlocked and 
                rule.get_name() not in output):
                    output.append(rule.gwt_name())
                    continue

            if loli_content == 2:
                elementary_unlock = rule.can_be_unlocked("elementary_school")
                elementary_unlocked = rule.is_unlocked("elementary_school")

                if (elementary_unlock and 
                not elementary_unlocked and 
                rule.get_name() not in output):
                    output.append(rule.get_name())
                    continue

        return output

    def get_unlockable_rules_by_school(school):
        output = []

        for rule in rules.values():
            unlock = rule.can_be_unlocked(school)
            unlocked = rule.is_unlocked(school)

            if (unlock and not unlocked and rule.get_name() not in output):
                output.append(rule.get_name())
                continue

        return output

    def get_rule(rule_name):
        if not rules or rule_name not in rules.keys():
            return None
        return rules[rule_name]

    def is_rule_unlocked(rule_name, school):
        if rule_name not in rules.keys():
            return False
        return rules[rule_name].is_unlocked(school)

    def is_rule_visible(rule_name, school):
        if rule_name not in rules.keys():
            return False
        return rules[rule_name].is_visible(school)

    def load_rule(name, title, data = None):
        if name not in rules.keys():
            rules[name] = Rule(name, title)

        rules[name]._update(title, data)

    def remove_rule(name):
        if name in rules.keys():
            del(rules[name])

label load_rules:
    $ remove_rule("service_uniform")

    $ load_rule("theoretical_sex_ed", "Theoretical Sex Education", {
        '_description': ("Students get a new subject in which they deal with the"
            " topic of the human body and human reproduction."
            " All on a theoretical basis, of course."),
        '_unlock_conditions': [
            LevelCondition("2+"),
            LockCondition(),
        ],
        '_image_path': 'images/journal/rules/theoretical_sex_ed.png',
        '_image_path_alt': 'images/journal/rules/theoretical_sex_ed.png',
    })
    $ load_rule("theoretical_digital_material", "Digital Material", {
        '_description': "The Theoretical Sex Education-Class gets expanded " +
            "by using digital reference material like educational videos " +
            "about reproduction.",
        '_unlock_conditions': [
            LevelCondition("3+"),
            RuleCondition("theoretical_sex_ed", blocking = True),
            LockCondition(),
        ],
        '_image_path': 'images/journal/rules/theoretical_digital_sex_ed.png',
        '_image_path_alt': 'images/journal/rules/theoretical_digital_sex_ed.png',
    })
    $ load_rule("theoretical_teacher_material", "Use Teacher for learning", {
        '_description': "The teacher volunteer to use their own bodies to " +
            "give the students the best way to show them the human body.",
        '_unlock_conditions': [
            RuleCondition("theoretical_digital_material", blocking = True),
            LockCondition(),
        ],
        '_image_path': 'images/journal/rules/theoretical_teacher_sex_ed_<level>.png',
        '_image_path_alt': 'images/journal/rules/theoretical_teacher_sex_ed_3.png',
    })
    $ load_rule("theoretical_student_material", "Use Students for learning", {
        '_description': "The students learn about the human body, and the " +
            "differences each individual has, by presenting them with " +
            "their own bodies.\n\nWhile it may be a bit shameful for the " +
            "students, it also is a great way to build some confidence " +
            "over their own bodies and to accept that every body is " +
            "beautiful and should be displayed as such.",
        '_unlock_conditions': [
            RuleCondition("theoretical_teacher_material", blocking = True),
            LockCondition(),
        ],
        '_image_path': 'images/journal/rules/theoretical_student_sex_ed_<school>_<level>.png',
        '_image_path_alt': 'images/journal/rules/theoretical_student_sex_ed_high_school_3.png',
    })

    $ load_rule("practical_sex_ed", "Practical Sex Education", {
        '_description': "Everyone who wanted some hands-on experience " +
            "during Sex Ed now has the chance!\n\nIn the Practical Sex " + 
            "Ed-Classes students now get the chance to experiment " +
            "actively by exploring ways of masturbation. Even though " +
            "it's still limited to self-pleasuring out of safety concerns.",
        '_unlock_conditions': [
            LevelCondition("4+"),
            RuleCondition("theoretical_sex_ed", blocking = True),
            LockCondition(),
        ],
        '_image_path': 'images/journal/rules/practical_sex_ed_<school>_<level>.png',
        '_image_path_alt': 'images/journal/rules/practical_sex_ed_high_school_6.png',
    })

    $ load_rule("practical_teacher_material", "Use Teacher for learning", {
        '_description': "The teachers once again volunteer to help give " +
            "the students the best learning experience as possible.\n\n" +
            "Now the students get the opportunity to sexually experiment " +
            "with their teacher. Nobody can teach sex better than someone " +
            "in bed with years of hands-on experience.",
        '_unlock_conditions': [
            LevelCondition("5+"),
            RuleCondition("practical_sex_ed", blocking = True),
            RuleCondition("theoretical_teacher_material", blocking = True),
            LockCondition(),
        ],
        '_image_path': 'images/journal/rules/practical_sex_ed_teacher_<level>.png',
        '_image_path_alt': 'images/journal/rules/practical_sex_ed_teacher_5.png',
    })

    $ load_rule("practical_student_material", "Use Students for learning", {
        '_description': "After learning from the teachers how to have sex, " +
            "the students now learn how to learn the preferences of your " +
            "sex partner.\nSo the students now get to experiment on " +
            "each other.",
        '_unlock_conditions': [
            RuleCondition("practical_teacher_material", blocking = True),
            RuleCondition("theoretical_student_material", blocking = True),
            LockCondition(),
        ],
        '_image_path': 'images/journal/rules/practical_sex_ed_students_<school>_<level>.png',
        '_image_path_alt': 'images/journal/rules/practical_sex_ed_students_high_school_6.png',
    })

    $ load_rule("student_student_relation", "Students Relations", {
        '_description': ("Allows for students to have a relationship between"
            " each other and to openly show it."),
        '_unlock_conditions':[
            LockCondition(),
        ]
    })

    $ load_rule("student_teacher_relation", "Students-Teacher Relations", {
        '_description': ("Allows for teacher to engage in a relationship with"
            " students."),
        '_unlock_conditions':[
            LockCondition(),
        ]
    })

    $ load_rule("relaxed_uniform", "Relaxed Uniform", {
        '_description': "The students are free to be more relaxed about how to wear the uniform.",
        '_unlock_conditions': [
            LevelCondition("3+"),
        ],
        '_image_path': 'images/journal/rules/relaxed_uniform_<school>.png',
        '_image_path_alt': 'images/journal/rules/relaxed_uniform_high_school.png',
    })

    $ load_rule("sexy_uniform", "Sexy Uniform", {
        '_description': "A new uniform rule with a minimum amount of skin that has to be shown",
        '_unlock_conditions': [
            LevelCondition("5+"),
            RuleCondition("relaxed_uniform", blocking = True),
        ],
        '_image_path': 'images/journal/rules/sexy_uniform_<school>.png',
        '_image_path_alt': 'images/journal/rules/sexy_uniform_high_school.png',
    })

    $ load_rule("nude_uniform", "Nude Uniform", {
        '_description': "The best uniform there is with covering as little as possible.",
        '_unlock_conditions': [
            LevelCondition("8+"),
            RuleCondition("sexy_uniform", blocking = True),
        ],
        '_image_path': 'images/journal/rules/nude_uniform_<school>.png',
        '_image_path_alt': 'images/journal/rules/nude_uniform_high_school.png',
    })

    return