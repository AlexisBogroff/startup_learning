"""
Main test file for adaptive learning engine

Tested functions:

    # Manage users
    test_register_admin  # I/O ?
    test_register_teacher
    test_register_student
    registering_user_can_be_admin
    registering_user_can_be_teacher
    registering_user_can_be_student
    test_create_group
    test_delete_group
    test_add_group_permission
    test_delete_group_permission
    test_set_user_group
    test_student_can_integrate_this_group
    test_student_is_from_this_school
    test_delete_user_group
    test_login
    test_logout
    test_student_is_recognized
    test_get_school_mail_domain
    test_extract_mail_domain
    test_set_user_rights
    test_get_user_rights


    # Manage Exams
    # ------------

    ## Build exams
    test_create_exam
    test_delete_exam
    test_modify_exam
    test_randomize_sections_order
    test_randomize_questions_order
    test_create_question
    test_create_answer
    test_delete_question
    test_delete_answer
    test_add_question_to_test
    test_remove_question_from_test
    test_get_answer_text
    test_set_answer_text
    test_set_answer_grade
    test_get_answer_grade
    test_update_answer_text
    test_update_answer_grade
    test_update_question_text
    test_set_question_creation_datetime
    test_set_bool_answer_is_correct
    test_get_bool_answer_is_correct
    test_set_question_difficulty
    test_get_question_difficulty
    test_set_question_category
    test_get_question_category
    test_delete_question_difficulty
    test_set_exam_keyword
    test_delete_exam_keyword
    test_create_category
    test_delete_category
    test_set_category_parent
    test_delete_category_parent
    test_get_category_children
    test_create_section
    test_delete_section
    test_add_question_to_section
    test_delete_question_of_section
    test_get_section_questions
    test_set_section_description
    test_get_section_description
    test_set_exam_description
    test_get_exam_description
    test_compute_exam_max_grade
    test_get_exam_max_grade
    test_set_exam_max_grade
    test_set_question_grade
    test_get_question_grade
    test_set_bool_use_this_question
    test_get_bool_use_this_question
    test_set_question_text
    test_get_question_text

    ## Timer
    test_teacher_start_timer
    test_teacher_stop_timer
    test_teacher_modify_timer
    test_timer_ended
    test_get_timer_initial_time
    test_get_timer_remaining_time
    test_get_timer_end_time
    test_get_timer_time_limit

    ## Exam conditions
    test_set_datetime_exam_beginning
    test_set_datetime_exam_end
    test_get_datetime_exam_beginning
    test_get_datetime_exam_end
    test_delete_datetime_exam_beginning
    test_delete_datetime_exam_end

    ## During the exam
    test_exam_started
    test_exam_ended
    test_compare_now_with_datetime_beginning
    test_compare_now_with_datetime_end
    test_get_answer
    test_get_question
    test_get_time_student_submitted_question
    test_compute_time_student_spent_on_question
    test_get_time_student_started
    test_get_time_student_ended

    ## After the exam
    test_check_student_answer_is_correct
    test_compute_student_grade

    ## Exam statistics
    test_compute_exam_min_grade
    test_compute_exam_max_grade
    test_compute_exam_average_grade
    test_compute_exam_median_grade
    test_compute_exam_frequencies
    test_compute_question_min_grade
    test_compute_question_max_grade
    test_compute_question_average_grade
    test_compute_question_frequencies
    test_get_answer_frequencies

    ## Exam plots
    test_plot_student_grade_by_question_on_the_exam
    test_plot_grades_of_student_on_all_exams
    test_plot_barplot_grades_exam_by_group
    test_plot_radar_of_student_grades_by_sections_on_the_exam


    # Student
    # -------

    ## Profile / Progression
    test_plot_radar_of_student_strenghts_by_subject
    test_should_revise_question
    test_should_revise_subject


    # Algorithms
    # ----------

    # Create test
    test_algo_create_exam
    test_algo_predict_student_exam_grade
    test_algo_predict_student_answer_is_correct
    test_algo_predict_student_subject_grade
    test_algo_predict_student_progression
    test_algo_predict_student_similarity

    test_compute_students_similarity

TODO: test_add_answer (QuestionTestCase)
TODO: test_add_question (ExamTestCase)
"""
import unittest
from unittest.mock import patch
from adaptive_learning import exam, user, funcs
from adaptive_learning.exam import Exam
from adaptive_learning.question import Question
from adaptive_learning.answer import Answer


class AnswerTestCase(unittest.TestCase):
    """
    Test the creation of an answer
    """
    def setUp(self):
        self.answer = Answer()
        self.DEFAULT_PROPERTIES = {
            'text': '',
            'is_correct': False,
            'use_answer': True,
        }


    def test_get_exportable(self):
        obtained = self.answer.get_exportable()
        self.assertEqual(obtained, self.DEFAULT_PROPERTIES)


    INPUTS_ANSWER = ('Debug answer', 'True', 'False')

    @patch('builtins.input', side_effect=INPUTS_ANSWER)
    def test_set_properties(self, mock_inputs):
        self.answer.set_properties_from_input()
        self.assertEqual(self.answer.text, 'Debug answer')
        self.assertEqual(self.answer.is_correct, True)
        self.assertEqual(self.answer.use_answer, False)
        # Restore default parameters
        self.setUp()


    @patch('builtins.input', return_value='Debug answer')
    def test_set_text_from_input(self, mock_input):
        self.answer.set_text_from_input()
        self.assertEqual(self.answer.text, 'Debug answer')
        # Restore default parameters
        self.setUp()


    @patch('builtins.input', return_value='True')
    def test_set_is_correct_from_input(self, mock_input):
        self.answer.set_is_correct_from_input()
        self.assertEqual(self.answer.is_correct, True)
        # Restore default parameters
        self.setUp()


    @patch('builtins.input', return_value='False')
    def test_set_use_answer_from_input(self, mock_input):
        self.answer.set_use_answer_from_input()
        self.assertEqual(self.answer.use_answer, False)
        # Restore default parameters
        self.setUp()



class ExamTestCase(unittest.TestCase):
    """
    Test the creation of an exam

    TODO: add tests for functions related to the .save method
    """
    def setUp(self):
        self.exam = Exam()
        self.DEFAULT_PROPERTIES = {
            'id': '',
            'title': '',
            'description': '',
            'randomize_questions_order': True,
            'auto_rebase_grade': True,
            'grade_base': 20,
            'questions': [],
        }
        self.LOADED_EXAM = {
            'id': 'id_foo',
            'title': 'title_foo',
            'description': 'desc foo',
            'auto_rebase_grade': False,
            'grade_base': 100,
            'randomize_questions_order': False,
            'questions': [
                {'foo'},
                {'bar'},
            ],
        }


    def test__init(self):
        # Controls that:
        # - object is properly instanciated
        # - properties have the expected default values
        self.assertEqual(self.exam._id, self.DEFAULT_PROPERTIES['id'])
        self.assertEqual(self.exam.title, self.DEFAULT_PROPERTIES['title'])
        self.assertEqual(self.exam.description,
                         self.DEFAULT_PROPERTIES['description'])
        self.assertEqual(self.exam.randomize_questions_order,
                         self.DEFAULT_PROPERTIES['randomize_questions_order'])
        self.assertEqual(self.exam.auto_rebase_grade,
                         self.DEFAULT_PROPERTIES['auto_rebase_grade'])
        self.assertEqual(self.exam.grade_base,
                         self.DEFAULT_PROPERTIES['grade_base'])
        self.assertEqual(self.exam.questions,
                         self.DEFAULT_PROPERTIES['questions'])


    INPUTS_NEW_QUESTION = ('New question',
                           'mcq',
                           'Programming, VBA, Introduction',
                           )

    @patch('builtins.input', side_effect=INPUTS_NEW_QUESTION)
    def test_create_question(self, mock_inputs):
        expected_questions_data = [
            {
                'id': '',  # it has an ussid only once dumped
                'text': 'New question',
                'type': 'mcq',
                'keywords': 'Programming, VBA, Introduction',
                'use_question': True,
                'nb_points': 1.,
                'difficulty': 1,
                'notif_correct_answers': True,
                'notif_num_exact_answers': False,
                'randomize_answers_order': True,
                'answers': [],
                'position_id': 1,
            }
        ]
        self.exam._create_question()
        self.assertEqual(self.exam.questions, expected_questions_data)
        # Restore default parameters
        self.setUp()


    def test_default_properties(self):
        self.assertEqual(self.exam.grade_base,
                         self.DEFAULT_PROPERTIES['grade_base'])
        self.assertEqual(self.exam.auto_rebase_grade,
                         self.DEFAULT_PROPERTIES['auto_rebase_grade'])
        self.assertEqual(self.exam.randomize_questions_order,
                         self.DEFAULT_PROPERTIES['randomize_questions_order'])


    def test_generate_position_id_when_no_questions(self):
        obtained = funcs.generate_position_id(self.exam.questions)
        expected = 1
        self.assertEqual(obtained, expected)


    def test_generate_position_id_when_two_questions(self):
        self.exam.questions.append({'dummy question 1'})
        self.exam.questions.append({'dummy question 2'})

        obtained = funcs.generate_position_id(self.exam.questions)
        expected = 3
        self.assertEqual(obtained, expected)


    def test_get_exportable(self):
        # Controls that:
        # - it returns a dictionary with the expected structure
        # - the following keys are included in the exportable (sort of dump)
        # - the corresponding values are correctly matching
        expected = self.DEFAULT_PROPERTIES
        obtained = self.exam.get_exportable()
        self.assertEqual(obtained['id'], expected['id'])
        self.assertEqual(obtained['title'], expected['title'])
        self.assertEqual(obtained['description'], expected['description'])
        self.assertEqual(obtained['randomize_questions_order'],
                expected['randomize_questions_order'])
        self.assertEqual(obtained['auto_rebase_grade'],
                expected['auto_rebase_grade'])
        self.assertEqual(obtained['grade_base'],
                expected['grade_base'])


    TABLE_EXAMS_LONG = [
        {
            'description': 'foo',
            'id': 'c85779fd',
            'auto_rebase_grade': False,
            'grade_base': 5,
            'randomize_questions_order': False,
            'questions': ['foo'],
            'title': ''
        },
        {
            'description': '',
            'id': 'f67d625b',
            'auto_rebase_grade': True,
            'grade_base': 20,
            'randomize_questions_order': True,
            'questions': ['bar'],
            'title': ''
        },
    ]
    @patch('adaptive_learning.funcs.load_table', return_value=TABLE_EXAMS_LONG)
    def test_load_exam(self, mock_table):
        # Almost duplicate of test_retrieve_exam_from_table
        self.exam.load_exam(id_exam='c85779fd')
        self.assertEqual(self.exam.questions, ['foo'])
        self.assertEqual(self.exam.description, 'foo')
        self.assertFalse(self.exam.auto_rebase_grade)
        self.assertEqual(self.exam.grade_base, 5)
        self.assertFalse(self.exam.randomize_questions_order)

        # Restore default parameters
        self.setUp()


    def test_set_auto_rebase_grade_from_existing(self):
        self.exam.set_auto_rebase_grade_from_existing(self.LOADED_EXAM)
        obtained = self.exam.auto_rebase_grade
        expected = self.LOADED_EXAM['auto_rebase_grade']
        self.assertEqual(obtained, expected)
        # Restore default parameters
        self.setUp()


    def test_set_description_from_existing(self):
        self.exam.set_description_from_existing(self.LOADED_EXAM)
        obtained = self.exam.description
        expected = self.LOADED_EXAM['description']
        self.assertEqual(obtained, expected)
        # Restore default parameters
        self.setUp()


    def test_set_grade_base_from_existing(self):
        self.exam.set_grade_base_from_existing(self.LOADED_EXAM)
        obtained = self.exam.grade_base
        expected = self.LOADED_EXAM['grade_base']
        self.assertEqual(obtained, expected)
        # Restore default parameters
        self.setUp()


    def test_set_id_from_existing(self):
        self.exam.set_id_from_existing(self.LOADED_EXAM)
        obtained = self.exam._id
        expected = self.LOADED_EXAM['id']
        self.assertEqual(obtained, expected)
        # Restore default parameters
        self.setUp()


    def test_set_properties_from_existing_all(self):
        self.exam.set_properties_from_existing_all(self.LOADED_EXAM)
        self.assertEqual(self.exam._id, 'id_foo')
        self.assertEqual(self.exam.title, 'title_foo')
        self.assertEqual(self.exam.description, "desc foo")
        self.assertEqual(self.exam.randomize_questions_order, False)
        self.assertEqual(self.exam.auto_rebase_grade, False)
        self.assertEqual(self.exam.grade_base, 100)
        # Restore default parameters
        self.setUp()


    INPUTS_PROPERTIES_MAIN = (
        'new exam title',
        'new exam description',
        )
    @patch('builtins.input', side_effect=INPUTS_PROPERTIES_MAIN)
    def test_set_properties_from_input_main(self, mock_inputs):
        self.exam.set_properties_from_input_main()
        self.assertEqual(self.exam.title, 'new exam title')
        self.assertEqual(self.exam.description, 'new exam description')
        # Restore default parameters
        self.setUp()


    INPUTS_PROPERTIES_EXTRA = (
        'False',
        'False',
        '10',
        )
    @patch('builtins.input', side_effect=INPUTS_PROPERTIES_EXTRA)
    def test_set_properties_from_input_extra(self, mock_inputs):
        self.exam.set_properties_from_input_extra()
        self.assertEqual(self.exam.randomize_questions_order, False)
        self.assertEqual(self.exam.auto_rebase_grade, False)
        self.assertEqual(self.exam.grade_base, 10)
        # Restore default parameters
        self.setUp()


    def test_set_randomize_questions_order_from_existing(self):
        self.exam.set_randomize_questions_order_from_existing(self.LOADED_EXAM)
        obtained = self.exam.randomize_questions_order
        expected = self.LOADED_EXAM['randomize_questions_order']
        self.assertEqual(obtained, expected)
        # Restore default parameters
        self.setUp()


    def test_set_title_from_existing(self):
        self.exam.set_title_from_existing(self.LOADED_EXAM)
        obtained = self.exam.title
        expected = self.LOADED_EXAM['title']
        self.assertEqual(obtained, expected)
        # Restore default parameters
        self.setUp()



class FuncsTestCase(unittest.TestCase):
    """
    Test the functions of general order
    """
    def test_cast_when_bool(self):
        obtained = funcs.cast('True', bool)
        expected = True
        self.assertEqual(obtained, expected)


    def test_cast_when_int(self):
        obtained = funcs.cast('12', int)
        expected = 12
        self.assertEqual(obtained, expected)


    def test_cast_when_float(self):
        obtained = funcs.cast('12', float)
        expected = 12.
        self.assertEqual(obtained, expected)


    def test_cast_when_not_possible(self):
        with self.assertRaises(TypeError) as context:
            funcs.cast('12', bool)

        expected = "The value: 12, of type <class 'str'>, " \
                   "cannot be casted into type: <class 'bool'>"
        self.assertTrue(expected in str(context.exception))


    def test_extract_data(self):
        data = [
            {'id': 123, 'foo1': 'bar1'},
            {'id': 433, 'foo2': 'bar2'},
        ]
        obtained = funcs.extract_data(id=433, data=data)
        expected = [{'id': 433, 'foo2': 'bar2'}]
        self.assertEqual(obtained, expected)


    def test_get_single_elem(self):
        obtained = funcs.get_single_elem([4])
        expected = 4
        self.assertEqual(obtained, expected)


    def test_is_single_when_duplicate_found(self):
        table = [
            {'id':12, 'title': 'foo'},
            {'id':12, 'title': 'foobar'},
        ]
        obtained = funcs.is_single(table)
        self.assertFalse(obtained)


    def test_is_single_when_single_found(self):
        table = [
            {'id':12, 'title': 'foobar'},
        ]
        obtained = funcs.is_single(table)
        self.assertTrue(obtained)


    def test_is_empty_when_not_found(self):
        table = []
        obtained = funcs.is_empty(table)
        self.assertTrue(obtained)


    def test_is_empty_when_found(self):
        table = [
            {'id':12, 'title': 'foobar'},
        ]
        obtained = funcs.is_empty(table)
        self.assertFalse(obtained)


    TABLE_EXAMS_SHORT = [
        {'title': '', 'id': 'c85779fd', 'questions': [...]},
        {'title': '', 'id': '327e93a3', 'questions': [...]},
    ]
    @patch('adaptive_learning.funcs.load_table', return_value=TABLE_EXAMS_SHORT)
    def test_retrieve_sample_from_table(self, mock_table):
        obtained = funcs.retrieve_sample_from_table(id_sample='c85779fd',
                                                    path_table='')
        expected = {'title': '', 'id': 'c85779fd', 'questions': [...]}
        self.assertEqual(obtained, expected)


    TABLE_EMPTY = []
    @patch('adaptive_learning.funcs.load_table', return_value=TABLE_EMPTY)
    def test_retrieve_sample_from_table_when_is_empty(self, mock_table):
        with self.assertRaises(ValueError) as context:
            funcs.retrieve_sample_from_table(id_sample='c85779fd',
                                                    path_table='')
        self.assertTrue('Missing sample id c85779fd' in str(context.exception))


    TABLE_DUPLICATES = [
        {'title': '', 'id': 'c85779fd', 'questions': [...]},
        {'title': '', 'id': 'c85779fd', 'questions': [...]},
    ]
    @patch('adaptive_learning.funcs.load_table', return_value=TABLE_DUPLICATES)
    def test_retrieve_sample_from_table_when_duplicates(self, mock_table):
        with self.assertRaises(ValueError) as context:
            funcs.retrieve_sample_from_table(id_sample='c85779fd',
                                                    path_table='')
        self.assertTrue('Duplicate sample ids c85779fd' in str(context.exception))



class QuestionTestCase(unittest.TestCase):
    """
    Test the manipulations on questions and answers
    (create, amend, delete, launch, etc.)
    """
    def setUp(self):
        self.question = Question()
        self.DEFAULT_PROPERTIES = {
            'id': '',
            'text': '',
            'type': '',
            'keywords': '',
            'use_question': True,
            'nb_points': 1.,
            'difficulty': 1,
            'notif_correct_answers': True,
            'notif_num_exact_answers': False,
            'randomize_answers_order': True,
            'answers': [],
        }
        self.QUESTION_LOADED = {
            'id': 'id_foo',
            'text': 'clever question',
            'type': 'mcq',
            'keywords': 'programming, python, structures',
            # TODO: transform into list
            'use_question': False,
            'nb_points': 0.5,
            'difficulty': 3,
            'notif_correct_answers': False,
            'notif_num_exact_answers': False,
            'randomize_answers_order': False,
            'answers': [],
        }


    def test__init(self):
        self.assertEqual(
            self.question._id,
            self.DEFAULT_PROPERTIES['id'],
        )
        self.assertEqual(
            self.question.text,
            self.DEFAULT_PROPERTIES['text'],
        )
        self.assertEqual(
            self.question.type,
            self.DEFAULT_PROPERTIES['type'],
        )
        self.assertEqual(
            self.question.keywords,
            self.DEFAULT_PROPERTIES['keywords'],
        )
        self.assertEqual(
            self.question.use_question,
            self.DEFAULT_PROPERTIES['use_question'],
        )
        self.assertEqual(
            self.question.nb_points,
            self.DEFAULT_PROPERTIES['nb_points'],
        )
        self.assertEqual(
            self.question.difficulty,
            self.DEFAULT_PROPERTIES['difficulty'],
        )
        self.assertEqual(
            self.question.notif_correct_answers,
            self.DEFAULT_PROPERTIES['notif_correct_answers'],
        )
        self.assertEqual(
            self.question.notif_num_exact_answers,
            self.DEFAULT_PROPERTIES['notif_num_exact_answers'],
        )
        self.assertEqual(
            self.question.randomize_answers_order,
            self.DEFAULT_PROPERTIES['randomize_answers_order'],
        )
        self.assertEqual(
            self.question.answers,
            self.DEFAULT_PROPERTIES['answers'],
        )


    ANSWER_PROPERTIES = ['Debug answer', 'True', 'False']

    @patch('builtins.input', side_effect=ANSWER_PROPERTIES)
    def test_add_answer(self, mock_inputs):
        self.question.add_answer()
        obtained = self.question.answers
        expected = [
            {
                'text': 'Debug answer',
                'is_correct': True,
                'use_answer': False,
                'position_id': 1,
            }
        ]
        self.assertEqual(obtained, expected)
        # Restore default parameters
        self.setUp()


    def test_get_exportable(self):
        # Controls that:
        # - it returns a dictionary with the expected structure
        # - the following keys are included in the exportable (sort of dump)
        # - the corresponding values are correctly matching
        expected = self.DEFAULT_PROPERTIES
        obtained = self.question.get_exportable()
        self.assertEqual(obtained, expected)


    def test_set_question_from_existing(self):
        self.question.set_question_from_existing(self.QUESTION_LOADED)
        self.assertEqual(
            self.question._id,
            self.QUESTION_LOADED['id'],
        )
        self.assertEqual(
            self.question.text,
            self.QUESTION_LOADED['text'],
        )
        self.assertEqual(
            self.question.type,
            self.QUESTION_LOADED['type'],
        )
        self.assertEqual(
            self.question.keywords,
            self.QUESTION_LOADED['keywords'],
        )
        self.assertEqual(
            self.question.use_question,
            self.QUESTION_LOADED['use_question'],
        )
        self.assertEqual(
            self.question.nb_points,
            self.QUESTION_LOADED['nb_points'],
        )
        self.assertEqual(
            self.question.difficulty,
            self.QUESTION_LOADED['difficulty'],
        )
        self.assertEqual(
            self.question.notif_correct_answers,
            self.QUESTION_LOADED['notif_correct_answers'],
        )
        self.assertEqual(
            self.question.notif_num_exact_answers,
            self.QUESTION_LOADED['notif_num_exact_answers'],
        )
        self.assertEqual(
            self.question.randomize_answers_order,
            self.QUESTION_LOADED['randomize_answers_order'],
        )
        self.assertEqual(
            self.question.answers,
            self.QUESTION_LOADED['answers'],
        )
        # Restore default parameters
        self.setUp()



class UserMethodsTestCase(unittest.TestCase):
    """
    Test the user methods
    TODO: test user rights
    """
    def test_extract_mail_domain(self):
        expected_domain = 'univ-paris1.fr'
        mail_address = 'test_mail-pi@univ-paris1.fr'
        obtained_domain = user.extract_mail_domain(mail_address)
        self.assertEqual(expected_domain, obtained_domain)


    def test_get_school_mail_domain(self):
        school_mail_domain_1 = user.get_school_mail_domain('paris1')
        school_mail_domain_2 = user.get_school_mail_domain('esilv')
        self.assertEqual(school_mail_domain_1, 'univ-paris1.fr')
        self.assertEqual(school_mail_domain_2, 'edu.devinci.fr')


    def test_student_is_from_this_school(self):
        school_name = 'paris1'
        student_mail = 'stu_1@univ-paris1.fr'
        is_from_this_school = user.student_is_from_this_school(
            student_mail,
            school_name)
        self.assertTrue(is_from_this_school)



if __name__ == '__main__':
    unittest.main()
