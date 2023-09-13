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
            self._unlock_conditions = ConditionStorage()
            self._vote_comments = {}
            self._default_comments = {
                "yes": "I vote yes.",
                "no": "I vote no.",
                "veto": "I veto this decision.",
            }
            self._unlock_effects = []

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
                self._unlock_conditions = ConditionStorage()
            if not hasattr(self, '_vote_comments'):
                self._vote_comments = {}
            if not hasattr(self, '_default_comments'):
                self._default_comments = {
                    "yes": "I vote yes.",
                    "no": "I vote no.",
                    "veto": "I veto this decision.",
                }
            if not hasattr(self, '_unlock_effects'):
                self._unlock_effects = []
        
        def get_name(self):
            return self._name

        def get_title(self):
            return self._title

        def get_type(self):
            return "rule"

        def get_description(self):
            return self._description

        def get_description_str(self):
            return "\n\n".join(self._description)

        def get_image(self, school, level):
            for i in reversed(range(0, level + 1)):
                image = self._image_path.replace("<school>", school).replace("<level>", str(i))
                if renpy.loadable(image):
                    return image
            for i in range(0, 10):
                image = self._image_path.replace("<school>", school).replace("<level>", str(i))
                if renpy.loadable(image):
                    return image
            return self._image_path_alt

        def get_full_image(self, school, level):
            image = self.get_image(school, level)
            full_image = image.replace(".", "_full.")

            if renpy.loadable(full_image):
                return full_image
            return None

        def unlock(self, school, unlock = True, apply_effects = False):
            if school in self._unlocked:
                self._unlocked[school] = unlock

            if self._unlocked[school] and apply_effects:
                self.apply_effects()

        def is_unlocked(self, school):
            return school in self._unlocked and self._unlocked[school]

        def is_visible(self, school):
            return school in charList["schools"].keys() and self._unlock_conditions.is_blocking(school)

        def can_be_unlocked(self, school):
            return school in charList["schools"].keys() and self._unlock_conditions.is_fullfilled(school)

        def get_condition_storage(self):
            return self._unlock_conditions

        def get_conditions(self):
            return self._unlock_conditions.get_conditions()

        def get_list_conditions(self):
            return self._unlock_conditions.get_list_conditions()

        def get_desc_conditions(self):
            return self._unlock_conditions.get_desc_conditions()
        
        def get_votable_conditions(self):
            return self._unlock_conditions.get_votable_conditions()

        def get_vote_comments(self, char, result):
            if char not in self._vote_comments.keys():
                return self._default_comments[result]
            return self._vote_comments[char][result]

        def apply_effects(self):
            for effect in self._unlock_effects:
                effect.apply()


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

    $ load_rule("theoretical_sex_ed", "Theoretical Sex Education (TSE)", {
        '_description': [
            "Students get a new subject in which they deal with the topic of the human body and human reproduction. All on a theoretical basis, of course.",
        ],
        '_unlock_conditions': ConditionStorage(
            LevelCondition("2+"),
            StatCondition(20, "inhibition"),
            # LockCondition(),
        ),
        '_image_path': 'images/journal/rules/theoretical_sex_ed.png',
        '_image_path_alt': 'images/journal/rules/theoretical_sex_ed.png',
        '_vote_comments': {
            'teacher': {
                'yes': 'I think it is important to teach the students about the human body and reproduction. It is a natural part of life and should be treated as such. So I vote yes.',
                'no': 'Introducing theoretical sex education in schools could be problematic as it may interfere with family values and parents\' role in guiding their children on sensitive topics. That\'s why I vote against the introduction of theoretical sex education.',
                'veto': 'I am appalled by the mere suggestion of introducing theoretical sex education in schools. This is an absurd notion that undermines the values and principles we strive to instill in our students, and it completely disregards the importance of parental guidance in such delicate matters. As a teacher, I vehemently veto any attempt to implement this nonsensical curriculum.',
            },
            'student': {
                'yes': 'As a student of this school, I strongly support the introduction of theoretical sex education. It is essential for students to have access to comprehensive and accurate information that can help them make informed decisions about their sexual health and well-being. Therefore, I vote yes on this proposal.',
                'no': 'I believe that theoretical sex education goes against my personal beliefs and values. I would prefer to focus on different aspects of education that align more closely with my interests and priorities. Therefore, I vote no on this proposal.',
                'veto': 'I believe introducing theoretical sex education is unnecessary and ridiculous. We should focus on practical, real-life skills instead. I veto this proposal.',
            },
            'parents': {
                'yes': 'I fully support the introduction of theoretical sex education in our school curriculum. It\'s essential for our children to have a comprehensive understanding of the topic to make informed decisions about their health and relationships. That\'s why I vote yes.',
                'no': 'I believe that theoretical sex education is not appropriate for our school, and it should be left to parents to discuss these matters at home. We should prioritize other subjects that are more important for our children\'s education. So I vote no',
                'veto': 'I vehemently oppose the introduction of theoretical sex education in our school; it\'s a ridiculous notion that infringes upon our parental rights and values. Our children\'s education should focus on traditional subjects, leaving discussions about sex to families. I veto.',
            },
        },
    })
    $ load_rule("theoretical_digital_material", "Digital Material for TSE", {
        '_description': [
            "The Theoretical Sex Education-Class gets expanded by using digital reference material like educational videos about reproduction.",
        ],
        '_unlock_conditions': ConditionStorage(
            LevelCondition("3+"),
            RuleCondition("theoretical_sex_ed", blocking = True),
            LockCondition(),
        ),
        '_image_path': 'images/journal/rules/theoretical_digital_sex_ed.png',
        '_image_path_alt': 'images/journal/rules/theoretical_digital_sex_ed.png',
        '_vote_comments': {
            'teacher': {
                'yes': 'I believe incorporating digital materials like pornography into theoretical sex education can provide a more realistic view of the topic, helping students understand the complexities and potential risks associated with it. However, it\'s crucial to ensure age-appropriate content and a responsible approach to such discussions. So I vote yes.',
                'no': 'I firmly oppose the use of digital material like pornography in theoretical sex education. It\'s important to maintain a safe and responsible learning environment, prioritizing age-appropriate and evidence-based resources to educate our students about sexuality. So I vote no.',
                'veto': 'I strongly object to the use of digital material like pornography in theoretical sex education. We must focus on providing accurate, age-appropriate information and promoting healthy discussions rather than exposing our students to explicit content. I veto this decision.',
            },
            'student': {
                'yes': 'I think using digital stuff like porn in sex ed could make it more real and help us see the complicated parts and the risks. But we need to be sure it\'s right for our age and talk about it in a responsible way. So yeah, I\'m saying yes.',
                'no': 'I really don\'t think we should use digital stuff like porn in sex ed. We need to make sure it\'s safe and right for our age, and we should use trusted sources to teach us about sex. That\'s why I\'m saying no.',
                'veto': 'I\'m really against using digital stuff like porn in sex ed. We should give the right info for our age and talk about it in a healthy way, not show explicit stuff to students. I veto this idea.',
            },
            'parents': {
                'yes': 'I think including digital materials like pornography in sex education could offer a more realistic perspective for our children, aiding their understanding of the complexities and potential risks involved. Nevertheless, it\'s vital to make sure the content is suitable for their age and that the discussions are handled responsibly. Thus, I\'m in favor of this approach.',
                'no': 'I\'m strongly against using digital material like pornography in sex education. We need to make sure our children learn about sexuality in a safe and responsible way, using age-appropriate and evidence-based resources. So, my vote is a definite no.',
                'veto': 'I strongly oppose the inclusion of digital materials, such as pornography, in theoretical sex education. It\'s crucial that we concentrate on delivering accurate, age-appropriate information and encouraging healthy discussions, rather than exposing our children to explicit content. I firmly veto this decision.',
            },
        },
    })
    $ load_rule("theoretical_teacher_material", "Use Teacher for learning in TSE", {
        '_description': [
            "The teacher volunteer to use their own bodies to give the students the best way to show them the human body.",
        ],
        '_unlock_conditions': ConditionStorage(
            RuleCondition("theoretical_digital_material", blocking = True),
            LockCondition(),
        ),
        '_image_path': 'images/journal/rules/theoretical_teacher_sex_ed_<level>.png',
        '_image_path_alt': 'images/journal/rules/theoretical_teacher_sex_ed_3.png',
        '_vote_comments': {
            'teacher': {
                'yes': 'I believe that using teachers\' bodies as a reference material in theoretical sex education is a great way to help students understand the concepts better. It can also be a great way to foster a safe and healthy learning environment. I vote for this proposal.',
                'no': 'I do not believe that using the human body as a teaching tool for sex education is appropriate or beneficial for students. It may be seen as exploitative and detract from a student\'s focus on the material. I vote against this proposal.',
                'vote': 'The use of teacher\'s bodies as a reference material for theoretical sex education is not acceptable. I veto this decision.',
            },
            'student': {
                'yes': 'I think using teachers as examples in theoretical sex education can really help us students grasp the concepts better. It could also make our learning environment safer and healthier. So, I\'m all in for this idea!',
                'no': 'As a student of this school, I don\'t think using the human body as a teaching tool in sex education is the right approach. It might make some of us uncomfortable and distract from the main content. So, I\'m voting against this proposal.',
                'veto': 'I\'m a student here, and I believe that using teachers\' bodies as reference material for theoretical sex education is not something I can support. I\'m against this decision and I\'m using my veto.',
            },
            'parents': {
                'yes': 'As a parent, I think it\'s important for my child to have access to comprehensive sexual education. Using teachers\' bodies as reference materials could help to make theoretical concepts more tangible and increase student engagement in class.',
                'no': 'I\'m sorry, but I cannot agree with your decision. It is important for students to be aware of the risks associated with certain sexual activities, and teachers have an obligation to provide them with accurate information. Furthermore, using teachers\' bodies as reference material would hardly be appropriate in a theoretical class setting.',
                'veto': 'As a parent, I strongly object to my child being exposed to their teacher\'s bodies during sexual education classes. Therefore I veto this decision.',
            },
        }
    })
    $ load_rule("theoretical_student_material", "Use Students for learning in TSE", {
        '_description': [
            "The students learn about the human body, and the differences each individual has, by presenting them with their own bodies.",
            "While it may be a bit shameful for the students, it also is a great way to build some confidence over their own bodies and to accept that every body is beautiful and should be displayed as such.",
        ],
        '_unlock_conditions': ConditionStorage(
            RuleCondition("theoretical_teacher_material", blocking = True),
            LockCondition(),
        ),
        '_image_path': 'images/journal/rules/theoretical_student_sex_ed_<school>_<level>.png',
        '_image_path_alt': 'images/journal/rules/theoretical_student_sex_ed_high_school_3.png',
        '_vote_comments': {
            'teacher': {
                'yes': 'I believe that using student bodies as reference materials in theoretical sex education is an excellent way to help young people better understand their bodies, how they work and how to take care of them. It can also provide a safe environment for students to ask questions without feeling ashamed or embarrassed.',
                'no': 'I believe that using student\'s bodies as reference material for theoretical sex education is not only inappropriate, but it also fails to acknowledge the unique and complex nature of each individual.',
                'veto': 'I believe that using student bodies as a reference material for theoretical sex education is both ill-advised and highly irresponsible. Such an experiment could lead to serious repercussions, such as emotional trauma or even physical harm.',
            },
            'student': {
                'yes': 'I think that using our own bodies as examples in theoretical sex education is a really good idea for helping us, young people, to grasp how our bodies function and how to take care of them. This approach could also make it easier for us to ask questions without feeling embarrassed or ashamed in a safe environment.',
                'no': 'I\'m a student here, and I think using our bodies as reference material in theoretical sex education isn\'t the right way to go. It doesn\'t recognize how each one of us is unique and complex.',
                'veto': 'I firmly believe that using student bodies as reference material in theoretical sex education is not advisable and could have significant negative consequences. It may lead to uncomfortable situations and potentially damage the overall learning environment.',
            },
            'parent': {
                'yes': 'I believe that using student bodies as reference materials in theoretical sex education is an excellent way to help young people better understand their bodies, how they work and how to take care of them. It can also provide a safe environment for students to ask questions without feeling ashamed or embarrassed.',
                'no': 'As a parent of a student in this school, I think using student bodies as reference materials in theoretical sex education is a questionable approach. While I understand the importance of comprehensive education, I am concerned that this method might inadvertently lead to uncomfortable situations and potentially compromise the emotional well-being of our children.',
                'veto': 'I do not believe that using student bodies as a reference material for theoretical sex education is a wise decision. Such an experiment could lead to serious repercussions, such as emotional trauma or even physical harm.',
            },
        }
    })

    $ load_rule("practical_sex_ed", "Practical Sex Education (PSE)", {
        '_description': [
            "Everyone who wanted some hands-on experience during Sex Ed now has the chance!",
            "In the Practical Sex Ed-Classes students now get the chance to experiment actively by exploring ways of masturbation. Even though it's still limited to self-pleasuring out of safety concerns.",
        ],
        '_unlock_conditions': ConditionStorage(
            LevelCondition("4+"),
            RuleCondition("theoretical_sex_ed", blocking = True),
            LockCondition(),
        ),
        '_image_path': 'images/journal/rules/practical_sex_ed_<school>_<level>.png',
        '_image_path_alt': 'images/journal/rules/practical_sex_ed_high_school_6.png',
        '_vote_comments': {
            'teacher': {
                'yes': 'I believe that introducing practical sex education in our school is a great idea. It will help to equip students with the knowledge and skills they need to make responsible and informed decisions about their sexual health.',
                'no': 'I don\'t believe that practical sex education should be introduced in our school. It is not appropriate for the students\' age and may lead to potential risks. We should focus on other more important topics that are more relevant to the students\' learning.',
                'veto': 'The introduction of practical sex education in our school would be detrimental to the moral development of our students. It would encourage promiscuity and undermine the values of abstinence and fidelity, which are essential for a healthy society.',
            },
            'student': {
                'yes': 'I believe that practical sex education should be introduced in our school. It will provide students with the knowledge and skills they need to make responsible and informed decisions about their sexual health.',
                'no': 'I don\'t think practical sex education should be introduced in our school. It is not suitable for the students\' age and may lead to potential risks. We should prioritize other more important topics that are more relevant to the students\' learning.',
                'veto': 'Bringing practical sex education into our school could potentially hinder our students\' moral development. It might promote casual relationships and could challenge the importance of abstinence and commitment, which I believe are crucial for a healthy society.',
            },
            'parent': {
                'yes': 'I believe that incorporating practical sex education in our school is a beneficial step. It will empower our children with the knowledge and abilities necessary to make responsible and informed choices regarding their sexual well-being.',
                'no': 'I have reservations about introducing practical sex education in our school. Considering the age of the students, I believe it\'s essential to prioritize other subjects that are more relevant to their learning, ensuring a well-rounded education.',
                'veto': 'As a parent, I strongly oppose the introduction of practical sex education in our school. I believe that this type of education is not suitable for our children and could potentially lead to negative consequences.',
            }
        }
    })

    $ load_rule("practical_teacher_material", "Use Teacher for learning in PSE", {
        '_description': [
            "The teachers once again volunteer to help give the students the best learning experience as possible.",
            "Now the students get the opportunity to sexually experiment with their teacher. Nobody can teach sex better than someone in bed with years of hands-on experience.",
        ],
        '_unlock_conditions': ConditionStorage(
            LevelCondition("5+"),
            RuleCondition("practical_sex_ed", blocking = True),
            RuleCondition("theoretical_teacher_material", blocking = True),
            LockCondition(),
        ),
        '_image_path': 'images/journal/rules/practical_sex_ed_teacher_<level>.png',
        '_image_path_alt': 'images/journal/rules/practical_sex_ed_teacher_5.png',
    })

    $ load_rule("practical_student_material", "Use Students for learning in PSE", {
        '_description': [
            "After learning from the teachers how to have sex, the students now learn how to learn the preferences of your sex partner.\nSo the students now get to experiment on each other.",
        ],
        '_unlock_conditions': ConditionStorage(
            RuleCondition("practical_teacher_material", blocking = True),
            RuleCondition("theoretical_student_material", blocking = True),
            LockCondition(),
        ),
        '_image_path': 'images/journal/rules/practical_sex_ed_students_<school>_<level>.png',
        '_image_path_alt': 'images/journal/rules/practical_sex_ed_students_high_school_6.png',
    })

    $ load_rule("student_student_relation", "Students Relations", {
        '_description': [
            "Allows for students to have a relationship between each other and to openly show it.",
        ],
        '_unlock_conditions':ConditionStorage(
            LockCondition(),
        ),
    })

    $ load_rule("student_teacher_relation", "Students-Teacher Relations", {
        '_description': [
            "Allows for teacher to engage in a relationship with students.",
        ],
        '_unlock_conditions':ConditionStorage(
            LockCondition(),
        ),
    })

    $ load_rule("relaxed_uniform", "Relaxed Uniform", {
        '_description': [
            "The students are free to be more relaxed about how to wear the uniform.",
        ],
        '_unlock_conditions': ConditionStorage(
            LevelCondition("3+"),
        ),
        '_image_path': 'images/journal/rules/relaxed_uniform_<school>.png',
        '_image_path_alt': 'images/journal/rules/relaxed_uniform_high_school.png',
    })

    $ load_rule("sexy_uniform", "Sexy Uniform", {
        '_description': [
            "A new uniform rule with a minimum amount of skin that has to be shown",
        ],
        '_unlock_conditions': ConditionStorage(
            LevelCondition("5+"),
            RuleCondition("relaxed_uniform", blocking = True),
        ),
        '_image_path': 'images/journal/rules/sexy_uniform_<school>.png',
        '_image_path_alt': 'images/journal/rules/sexy_uniform_high_school.png',
    })

    $ load_rule("nude_uniform", "Nude Uniform", {
        '_description': [
            "The best uniform there is with covering as little as possible.",
        ],
        '_unlock_conditions': ConditionStorage(
            LevelCondition("8+"),
            RuleCondition("sexy_uniform", blocking = True),
        ),
        '_image_path': 'images/journal/rules/nude_uniform_<school>.png',
        '_image_path_alt': 'images/journal/rules/nude_uniform_high_school.png',
    })

    return