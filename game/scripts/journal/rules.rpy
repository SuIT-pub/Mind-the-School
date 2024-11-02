init -6 python:
    import re

    ########################
    # region CLASSES ----- #
    ########################

    class Rule(Journal_Obj):
        """
        A subclass of Journal_Obj that represents a rule.
        A rule is a special type of journal object that can be used to unlock new content in the game.

        ### Attributes:
        1. _unlocked: Dict[str, bool] 
            - A dictionary that stores the unlock status of the rule for each school.

        ### Methods:
        1. get_type() -> str
            - Returns the type of the journal object.
        """

        def __init__(self, name: str, title: str):
            super().__init__(name, title)
            self._unlocked = False

        def _update(self, title: str, data: Dict[str, Any] = None) -> None:
            super()._update(title, data)
            if data != None:
                self.__dict__.update(data)
                
            if not hasattr(self, '_unlocked'):
                self._unlocked = False

            if not isinstance(self._unlocked, bool):
                self._unlocked = self._unlocked['high_school'] or self._unlocked['middle_school'] or self._unlocked['elementary_school']

        def is_valid(self):
            """
            Checks whether the rule is valid.
            """

            super().is_valid()

        def get_type(self) -> str:
            """
            Returns the type of the journal object.

            ### Returns:
            1. str
                - The type of the journal object.
                - In this case, it returns "rule".
            """

            return "rule"

    # endregion
    ########################

    #####################################
    # region Rules Global Methods ----- #
    #####################################
    
    def get_rule(rule_name: str) -> Rule:
        """
        Returns the rule with the given name.

        ### Parameters:
        1. rule_name: str
            - The name of the rule to be returned.

        ### Returns:
        1. Rule
            - The rule with the given name.
            - If no rule with the given name exists, returns None.
        """

        if not rules or rule_name not in rules.keys():
            return None
        return rules[rule_name]

    def is_rule_unlocked(rule_name: str) -> bool:
        """
        Returns whether the rule with the given name is unlocked for the given school.

        ### Parameters:
        1. rule_name: str
            - The name of the rule to be checked.
        2. school: str
            - The school to be checked.

        ### Returns:
        1. bool
            - Whether the rule with the given name is unlocked for the given school.
            - If no rule with the given name exists, returns False.
        """

        if rule_name not in rules.keys():
            return False
        return rules[rule_name].is_unlocked()

    def is_rule_visible(rule_name: str, **kwargs) -> bool:
        """
        Returns whether the rule with the given name is visible.
        A rule is visible when it is unlocked for at least one school or when it has no blocking fulfilled conditions.

        ### Parameters:
        1. rule_name: str
            - The name of the rule to be checked.

        ### Returns:
        1. bool
            - Whether the rule with the given name is visible.
            - If no rule with the given name exists, returns False.
        """

        if rule_name not in rules.keys():
            return False
        return rules[rule_name].is_visible(**kwargs)

    def load_rule(name: str, title: str, data: Dict[str, Any] = None):
        """
        Loads and updates a rule with the given name, title and data.

        ### Parameters:
        1. name: str
            - The name of the rule to be loaded.
        2. title: str
            - The title of the rule to be loaded.
        3. data: Dict[str, Any]
            - The data of the rule to be loaded.
        """

        if not is_mod_active(active_mod_key):
            return

        if name not in rules.keys():
            rules[name] = Rule(name, title)

        rules[name]._update(title, data)

        rules[name].is_valid()

    def remove_rule(name: str):
        """
        Removes the rule with the given name.

        ### Parameters:
        1. name: str
            - The name of the rule to be removed.
        """

        if name in rules.keys():
            del(rules[name])

    # endregion
    #####################################

#######################
# region LABELS ----- #

label load_rules ():
    $ set_current_mod('base')

    $ remove_rule("service_uniform")

    $ load_rule("school_jobs", "School Jobs", {
        '_description': [
            "The students get an opportunity to work or help out in certain facilities of the school.",
            "This not only helps the facilities to run more smoothly, but also gives the students a chance to learn new skills and to earn some money.",
        ],
        '_unlock_conditions': ConditionStorage(
            ProgressCondition("unlock_school_jobs", 3, True),
            PTAOverride('parent'),
        ),
        '_image_path': 'images/journal/rules/school_jobs_<level>.webp',
        '_image_path_alt': 'images/journal/rules/school_jobs_1.webp',
    })

    #! locked, currently not implemented
    $ load_rule("theoretical_sex_ed", "Theoretical Sex Education (TSE)", {
        '_description': [
            "Students get a new subject in which they deal with the topic of the human body and human reproduction. All on a theoretical basis, of course.",
        ],
        '_unlock_conditions': ConditionStorage(
            StatCondition(inhibition = '90-', corruption = '10+'),
            ProgressCondition("start_sex_ed", "6", True),
            # PTAOverride('parent', False),
            # PTAOverride('teacher', True),
        ),
        '_image_path': 'images/journal/rules/theoretical_sex_ed.webp',
        '_image_path_alt': 'images/journal/rules/theoretical_sex_ed.webp',
    })

    #! locked, currently not implemented
    $ load_rule("theoretical_digital_material", "Digital Material for TSE", {
        '_description': [
            "The Theoretical Sex Education-Class gets expanded by using digital reference material like educational videos about reproduction.",
        ],
        '_unlock_conditions': ConditionStorage(
            LevelCondition("2+"),
            StatCondition(inhibition = '90-'),
            RuleCondition("theoretical_sex_ed", True),
            # LockCondition(),
        ),
        '_image_path': 'images/journal/rules/theoretical_digital_sex_ed.webp',
        '_image_path_alt': 'images/journal/rules/theoretical_digital_sex_ed.webp',
        '_vote_comments': {
            'teacher': {
                'yes': [
                    'I believe incorporating digital materials like pornography into theoretical sex education can provide a more realistic view of the topic, helping students understand the complexities and potential risks associated with it.', 
                    'However, it\'s crucial to ensure age-appropriate content and a responsible approach to such discussions. So I vote yes.'
                ],
                'no': [
                    'I firmly oppose the use of digital material like pornography in theoretical sex education.', 
                    'It\'s important to maintain a safe and responsible learning environment, prioritizing age-appropriate and evidence-based resources to educate our students about sexuality. So I vote no.'
                ],
                'veto': [
                    'I strongly object to the use of digital material like pornography in theoretical sex education.', 
                    'We must focus on providing accurate, age-appropriate information and promoting healthy discussions rather than exposing our students to explicit content. I veto this decision.'
                ],
            },
            'student': {
                'yes': [
                    'I think using digital stuff like porn in sex ed could make it more real and help us see the complicated parts and the risks.', 
                    'But we need to be sure it\'s right for our age and talk about it in a responsible way. So yeah, I\'m saying yes.'
                ],
                'no': 'I really don\'t think we should use digital stuff like porn in sex ed. We need to make sure it\'s safe and right for our age, and we should use trusted sources to teach us about sex. That\'s why I\'m saying no.',
                'veto': 'I\'m really against using digital stuff like porn in sex ed. We should give the right info for our age and talk about it in a healthy way, not show explicit stuff to students. I veto this idea.',
            },
            'parent': {
                'yes': [
                    'I think including digital materials like pornography in sex education could offer a more realistic perspective for our children, aiding their understanding of the complexities and potential risks involved.', 
                    'Nevertheless, it\'s vital to make sure the content is suitable for their age and that the discussions are handled responsibly. Thus, I\'m in favor of this approach.'
                ],
                'no': [
                    'I\'m strongly against using digital material like pornography in sex education.', 
                    'We need to make sure our children learn about sexuality in a safe and responsible way, using age-appropriate and evidence-based resources. So, my vote is a definite no.'
                ],
                'veto': ['I strongly oppose the inclusion of digital materials, such as pornography, in theoretical sex education.', 
                'It\'s crucial that we concentrate on delivering accurate, age-appropriate information and encouraging healthy discussions, rather than exposing our children to explicit content. I firmly veto this decision.'
                ],
            },
        },
    })

    #! locked, currently not implemented
    $ load_rule("theoretical_teacher_material", "Use Teacher for learning in TSE", {
        '_description': [
            "The teacher volunteer to use their own bodies to give the students the best way to show them the human body.",
        ],
        '_unlock_conditions': ConditionStorage(
            RuleCondition("theoretical_digital_material", True),
            StatCondition(inhibition = '85-'),
            LockCondition(),
        ),
        '_image_path': 'images/journal/rules/theoretical_teacher_sex_ed_<level>.webp',
        '_image_path_alt': 'images/journal/rules/theoretical_teacher_sex_ed_3.webp',
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
            'parent': {
                'yes': 'As a parent, I think it\'s important for my child to have access to comprehensive sexual education. Using teachers\' bodies as reference materials could help to make theoretical concepts more tangible and increase student engagement in class.',
                'no': 'I\'m sorry, but I cannot agree with your decision. It is important for students to be aware of the risks associated with certain sexual activities, and teachers have an obligation to provide them with accurate information. Furthermore, using teachers\' bodies as reference material would hardly be appropriate in a theoretical class setting.',
                'veto': 'As a parent, I strongly object to my child being exposed to their teacher\'s bodies during sexual education classes. Therefore I veto this decision.',
            },
        }
    })

    #! locked, currently not implemented
    $ load_rule("theoretical_student_material", "Use Students for learning in TSE", {
        '_description': [
            "The students learn about the human body, and the differences each individual has, by presenting them with their own bodies.",
            "While it may be a bit shameful for the students, it also is a great way to build some confidence over their own bodies and to accept that every body is beautiful and should be displayed as such.",
        ],
        '_unlock_conditions': ConditionStorage(
            RuleCondition("theoretical_teacher_material", True),
            StatCondition(inhibition = '80-'),
            LockCondition(),
        ),
        '_image_path': 'images/journal/rules/theoretical_student_sex_ed_<level>.webp',
        '_image_path_alt': 'images/journal/rules/theoretical_student_sex_ed_3.webp',
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

    #! locked, currently not implemented
    $ load_rule("practical_sex_ed", "Practical Sex Education (PSE)", {
        '_description': [
            "Everyone who wanted some hands-on experience during Sex Ed now has the chance!",
            "In the Practical Sex Ed-Classes students now get the chance to experiment actively by exploring ways of masturbation. Even though it's still limited to self-pleasuring out of safety concerns.",
        ],
        '_unlock_conditions': ConditionStorage(
            LevelCondition("4+"),
            RuleCondition("theoretical_sex_ed", True),
            LockCondition(),
        ),
        '_image_path': 'images/journal/rules/practical_sex_ed_high_school_<level>.webp',
        '_image_path_alt': 'images/journal/rules/practical_sex_ed_high_school_6.webp',
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

    #! locked, currently not implemented
    $ load_rule("practical_teacher_material", "Use Teacher for learning in PSE", {
        '_description': [
            "The teachers once again volunteer to help give the students the best learning experience as possible.",
            "Now the students get the opportunity to sexually experiment with their teacher. Nobody can teach sex better than someone in bed with years of hands-on experience.",
        ],
        '_unlock_conditions': ConditionStorage(
            LevelCondition("5+"),
            RuleCondition("practical_sex_ed", True),
            RuleCondition("theoretical_teacher_material", True),
            LockCondition(),
        ),
        '_image_path': 'images/journal/rules/practical_sex_ed_teacher_<level>.webp',
        '_image_path_alt': 'images/journal/rules/practical_sex_ed_teacher_5.webp',
    })

    #! locked, currently not implemented
    $ load_rule("practical_student_material", "Use Students for learning in PSE", {
        '_description': [
            "After learning from the teachers how to have sex, the students now learn how to learn the preferences of your sex partner.\nSo the students now get to experiment on each other.",
        ],
        '_unlock_conditions': ConditionStorage(
            RuleCondition("practical_teacher_material", True),
            RuleCondition("theoretical_student_material", True),
            LockCondition(),
        ),
        '_image_path': 'images/journal/rules/practical_sex_ed_students_high_school_<level>.webp',
        '_image_path_alt': 'images/journal/rules/practical_sex_ed_students_high_school_6.webp',
    })

    # * implemented
    $ load_rule("student_student_relation", "Students Relations", {
        '_description': [
            "This rule allows for students to have a relationship between each other and to openly show it.",
        ],
        '_unlock_conditions':ConditionStorage(
            ProgressCondition("unlock_student_relationship", 1, True),
            StatCondition(inhibition = "95-", corruption = "2+"),
        ),
        
        '_image_path': 'images/journal/rules/student_student_relation <level> 0.webp',
        '_image_path_alt': 'images/journal/rules/student_student_relation <level> 1.webp',
    })

    #! locked, currently not implemented
    $ load_rule("student_teacher_relation", "Students-Teacher Relations", {
        '_description': [
            "This rule allows for teacher to engage in a relationship with students.",
        ],
        '_unlock_conditions': ConditionStorage(
            StatCondition(corruption = '10+'),
            RuleCondition("student_student_relation", blocking = True),
            LockCondition(False),
        ),
    })

    #! locked, currently not implemented
    $ load_rule("relaxed_uniform", "Relaxed Uniform", {
        '_description': [
            "The students are free to be more relaxed about how to wear the uniform.",
        ],
        '_unlock_conditions': ConditionStorage(
            LevelCondition("3+"),
            LockCondition(False),
        ),
        '_image_path': 'images/journal/rules/relaxed_uniform.webp',
        '_image_path_alt': 'images/journal/rules/relaxed_uniform.webp',
    })

    #! locked, currently not implemented
    $ load_rule("sexy_uniform", "Sexy Uniform", {
        '_description': [
            "A new uniform rule with a minimum amount of skin that has to be shown",
        ],
        '_unlock_conditions': ConditionStorage(
            LevelCondition("5+"),
            RuleCondition("relaxed_uniform", True),
        ),
        '_image_path': 'images/journal/rules/sexy_uniform.webp',
        '_image_path_alt': 'images/journal/rules/sexy_uniform.webp',
    })

    #! locked, currently not implemented
    $ load_rule("nude_uniform", "Nude Uniform", {
        '_description': [
            "The best uniform there is with covering as little as possible.",
        ],
        '_unlock_conditions': ConditionStorage(
            LevelCondition("8+"),
            RuleCondition("sexy_uniform", True),
        ),
        '_image_path': 'images/journal/rules/nude_uniform.webp',
        '_image_path_alt': 'images/journal/rules/nude_uniform.webp',
    })

    return

# endregion
#######################