"""
Main test file for adaptive learning engine
"""
import unittest
from unittest.mock import patch
from adaptive_learning import user, funcs
from adaptive_learning.questionnaires import exam
from adaptive_learning.questionnaires.exam import Exam
from adaptive_learning.questionnaires.question import Question, \
    create_question, McqQuestion
from adaptive_learning.questionnaires.answer import Answer, McqAnswer


class AnswerTestCase(unittest.TestCase):
    """
    Test methods of parent class Answer
    """
    @patch('builtins.input', return_value='Debug answer')
    def setUp(self, mock_input):
        self.answer = Answer()


    @patch('builtins.input', return_value='Debug answer')
    def test__init__(self, mock_input):
        answer = Answer()
        self.assertEqual(answer._text, 'Debug answer')


    def test_make_exportable(self):
        obtained = self.answer.make_exportable()
        expected = {'text': 'Debug answer'}
        self.assertEqual(expected, obtained)


    def test_load(self):
        answer_dic = {'text': 'Other debug text'}
        self.answer.load(load_dic=answer_dic)
        self.assertEqual(self.answer._text, answer_dic['text'])



class McqAnswerTestCase(unittest.TestCase):
    """
    Test the creation and loading of an McqAnswer
    """
    INPUTS_ANSWER = ('Debug answer', 'True', 'True')

    @patch('builtins.input', side_effect=INPUTS_ANSWER)
    def setUp(self, mock_input):
        self.answer = McqAnswer()
        self.VALS = {'text': 'Debug answer',
                     'is_correct': True,
                     'use_answer': True}


    def test__init__when_loading(self):
        answer = McqAnswer(load_dic=self.VALS)
        self.assertEqual(answer._text,
                         self.VALS['text'])
        self.assertEqual(answer._is_correct,
                         self.VALS['is_correct'])
        self.assertEqual(answer._use_answer,
                         self.VALS['use_answer'])


    @patch('builtins.input', side_effect=INPUTS_ANSWER)
    def test__init__when_creating(self, mock_inputs):
        answer = McqAnswer()
        self.assertEqual(answer._text,
                         self.VALS['text'])
        self.assertEqual(answer._is_correct,
                         self.VALS['is_correct'])
        self.assertEqual(answer._use_answer,
                         self.VALS['use_answer'])


    def test_load(self):
        self.answer.load(load_dic=self.VALS)
        self.assertEqual(self.answer._text,
                         self.VALS['text'])
        self.assertEqual(self.answer._is_correct,
                         self.VALS['is_correct'])
        self.assertEqual(self.answer._use_answer,
                         self.VALS['use_answer'])


    def test_make_exportable(self):
        obtained = self.answer.make_exportable()
        self.assertEqual(obtained, self.VALS)



# class ExamTestCase(unittest.TestCase):
#     """
#     Test the creation of an exam

#     TODO: add tests for functions related to the .save method
#     """
#     INPUTS_INIT = (
#         'Title debug exam',
#         'Description debug exam',
#         'mcq',
#         'Text debug question',
#         'Keywords debug question',
#         'No',
#     )

#     @patch('builtins.input', side_effect=INPUTS_INIT)
#     def setUp(self, mock_inputs):
#         self.exam = Exam()

#         self.DEFAULT_PROPERTIES = {
#             'id': '',
#             'title': '',
#             'description': '',
#             'randomize_questions': True,
#             'auto_rebase_grade': True,
#             'grade_base': 20,
#             'questions': [],
#         }
#         self.LOADED_EXAM = {
#             'id': 'id_foo',
#             'title': 'title_foo',
#             'description': 'desc foo',
#             'auto_rebase_grade': False,
#             'grade_base': 100,
#             'randomize_questions': False,
#             'questions': [
#                 {'foo'},
#                 {'bar'},
#             ],
#         }


#     def test__init(self):
#         # Controls that:
#         # - object is properly instanciated
#         # - properties have the expected default values
#         # TODO
#         self.assertEqual(type(self.exam.id), type(self.DEFAULT_PROPERTIES['id']))
#         self.assertEqual(len(self.exam.id), 36)
#         self.assertEqual(self.exam.title, self.DEFAULT_PROPERTIES['title'])
#         self.assertEqual(self.exam.description,
#                          self.DEFAULT_PROPERTIES['description'])
#         self.assertEqual(self.exam.randomize_questions,
#                          self.DEFAULT_PROPERTIES['randomize_questions'])
#         self.assertEqual(self.exam.auto_rebase_grade,
#                          self.DEFAULT_PROPERTIES['auto_rebase_grade'])
#         self.assertEqual(self.exam.grade_base,
#                          self.DEFAULT_PROPERTIES['grade_base'])
#         self.assertEqual(self.exam.questions,
#                          self.DEFAULT_PROPERTIES['questions'])


#     def test_default_properties(self):
#         self.assertEqual(self.exam.grade_base,
#                          self.DEFAULT_PROPERTIES['grade_base'])
#         self.assertEqual(self.exam.auto_rebase_grade,
#                          self.DEFAULT_PROPERTIES['auto_rebase_grade'])
#         self.assertEqual(self.exam.randomize_questions,
#                          self.DEFAULT_PROPERTIES['randomize_questions'])


#     def test_make_exportable(self):
#         # Controls that:
#         # - it returns a dictionary with the expected structure
#         # - the following keys are included in the exportable (sort of dump)
#         # - the corresponding values are correctly matching
#         expected = self.DEFAULT_PROPERTIES
#         obtained = self.exam.make_exportable()
#         self.assertEqual(type(obtained['id']), type(expected['id']))
#         self.assertEqual(len(obtained['id']), 36)
#         self.assertEqual(obtained['title'], expected['title'])
#         self.assertEqual(obtained['description'], expected['description'])
#         self.assertEqual(obtained['randomize_questions'],
#                 expected['randomize_questions'])
#         self.assertEqual(obtained['auto_rebase_grade'],
#                 expected['auto_rebase_grade'])
#         self.assertEqual(obtained['grade_base'],
#                 expected['grade_base'])


#     TABLE_EXAMS_LONG = [
#         {
#             'description': 'foo',
#             'id': 'c85779fd',
#             'auto_rebase_grade': False,
#             'grade_base': 5,
#             'randomize_questions': False,
#             'questions': ['foo'],
#             'title': ''
#         },
#         {
#             'description': '',
#             'id': 'f67d625b',
#             'auto_rebase_grade': True,
#             'grade_base': 20,
#             'randomize_questions': True,
#             'questions': ['bar'],
#             'title': ''
#         },
#     ]
#     @patch('adaptive_learning.questionnaires.funcs.load_table', return_value=TABLE_EXAMS_LONG)
#     def test_load_exam(self, mock_table):
#         # Almost duplicate of test_retrieve_exam_from_table
#         self.exam.load_exam(id_exam='c85779fd')
#         self.assertEqual(self.exam.questions, ['foo'])
#         self.assertEqual(self.exam.description, 'foo')
#         self.assertFalse(self.exam.auto_rebase_grade)
#         self.assertEqual(self.exam.grade_base, 5)
#         self.assertFalse(self.exam.randomize_questions)



#     def test_set_auto_rebase_grade_from_existing(self):
#         self.exam.set_auto_rebase_grade_from_existing(self.LOADED_EXAM)
#         obtained = self.exam.auto_rebase_grade
#         expected = self.LOADED_EXAM['auto_rebase_grade']
#         self.assertEqual(obtained, expected)


#     def test_set_description_from_existing(self):
#         self.exam.set_description_from_existing(self.LOADED_EXAM)
#         obtained = self.exam.description
#         expected = self.LOADED_EXAM['description']
#         self.assertEqual(obtained, expected)


#     def test_set_grade_base_from_existing(self):
#         self.exam.set_grade_base_from_existing(self.LOADED_EXAM)
#         obtained = self.exam.grade_base
#         expected = self.LOADED_EXAM['grade_base']
#         self.assertEqual(obtained, expected)


#     def test_set_id_from_existing(self):
#         self.exam.set_id_from_existing(self.LOADED_EXAM)
#         obtained = self.exam.id
#         expected = self.LOADED_EXAM['id']
#         self.assertEqual(obtained, expected)


#     def test_set_properties_from_existing_all(self):
#         self.exam.set_properties_from_existing_all(self.LOADED_EXAM)
#         self.assertEqual(self.exam.id, 'id_foo')
#         self.assertEqual(self.exam.title, 'title_foo')
#         self.assertEqual(self.exam.description, "desc foo")
#         self.assertEqual(self.exam.randomize_questions, False)
#         self.assertEqual(self.exam.auto_rebase_grade, False)
#         self.assertEqual(self.exam.grade_base, 100)
#         # Restore default parameters
#         self.setUp()


#     @patch('builtins.input', return_value='new exam title')
#     def test_set_title_from_input(self, mock_input):
#         self.exam.set_title_from_input()
#         self.assertEqual(self.exam.title, 'new exam title')
#         # Restore default parameters
#         self.setUp()


#     @patch('builtins.input', return_value='new exam desc')
#     def test_create_description_from_input(self, mock_input):
#         self.exam.set_title_from_input()
#         self.assertEqual(self.exam.title, 'new exam desc')
#         # Restore default parameters
#         self.setUp()


#     @patch('builtins.input', return_value='False')
#     def test_set_randomize_questions_from_input(self, mock_input):
#         self.exam.set_randomize_questions_from_input()
#         self.assertEqual(self.exam.randomize_questions, False)
#         # Restore default parameters
#         self.setUp()


#     @patch('builtins.input', return_value='False')
#     def test_set_auto_rebase_grade_from_input(self, mock_input):
#         self.exam.set_auto_rebase_grade_from_input()
#         self.assertEqual(self.exam.auto_rebase_grade, False)
#         # Restore default parameters
#         self.setUp()


#     @patch('builtins.input', return_value='10')
#     def test_set_grade_base_from_input(self, mock_input):
#         self.exam.set_grade_base_from_input()
#         self.assertEqual(self.exam.grade_base, 10)
#         # Restore default parameters
#         self.setUp()


#     def test_set_randomize_questions_from_existing(self):
#         self.exam.set_randomize_questions_from_existing(self.LOADED_EXAM)
#         obtained = self.exam.randomize_questions
#         expected = self.LOADED_EXAM['randomize_questions']
#         self.assertEqual(obtained, expected)
#         # Restore default parameters
#         self.setUp()


#     def test_set_title_from_existing(self):
#         self.exam.set_title_from_existing(self.LOADED_EXAM)
#         obtained = self.exam.title
#         expected = self.LOADED_EXAM['title']
#         self.assertEqual(obtained, expected)
#         # Restore default parameters
#         self.setUp()



# class FuncsTestCase(unittest.TestCase):
#     """
#     Test the functions of general order
#     """
#     def test_cast_when_bool(self):
#         obtained = funcs.cast('True', bool)
#         expected = True
#         self.assertEqual(obtained, expected)


#     def test_cast_when_int(self):
#         obtained = funcs.cast('12', int)
#         expected = 12
#         self.assertEqual(obtained, expected)


#     def test_cast_when_float(self):
#         obtained = funcs.cast('12', float)
#         expected = 12.
#         self.assertEqual(obtained, expected)


#     def test_cast_when_not_possible(self):
#         with self.assertRaises(TypeError) as context:
#             funcs.cast('12', bool)

#         expected = "The value: 12, of type <class 'str'>, " \
#                    "cannot be casted into type: <class 'bool'>"
#         self.assertTrue(expected in str(context.exception))


#     def test__extract_sample(self):
#         data = [
#             {'id': 123, 'foo1': 'bar1'},
#             {'id': 433, 'foo2': 'bar2'},
#         ]
#         obtained = funcs._extract_sample(id=433, data=data)
#         expected = [{'id': 433, 'foo2': 'bar2'}]
#         self.assertEqual(obtained, expected)


#     def test_get_single_elem(self):
#         obtained = funcs.get_single_elem([4])
#         expected = 4
#         self.assertEqual(obtained, expected)


#     def test_is_single_when_duplicate_found(self):
#         table = [
#             {'id':12, 'title': 'foo'},
#             {'id':12, 'title': 'foobar'},
#         ]
#         obtained = funcs.is_single(table)
#         self.assertFalse(obtained)


#     def test_is_single_when_single_found(self):
#         table = [
#             {'id':12, 'title': 'foobar'},
#         ]
#         obtained = funcs.is_single(table)
#         self.assertTrue(obtained)


#     def test_is_empty_when_not_found(self):
#         table = []
#         obtained = funcs.is_empty(table)
#         self.assertTrue(obtained)


#     def test_is_empty_when_found(self):
#         table = [
#             {'id':12, 'title': 'foobar'},
#         ]
#         obtained = funcs.is_empty(table)
#         self.assertFalse(obtained)


#     TABLE_EXAMS_SHORT = [
#         {'title': '', 'id': 'c85779fd', 'questions': [...]},
#         {'title': '', 'id': '327e93a3', 'questions': [...]},
#     ]
#     @patch('adaptive_learning.questionnaires.funcs.load_table', return_value=TABLE_EXAMS_SHORT)
#     def test_retrieve_sample_from_table(self, mock_table):
#         obtained = db.retrieve_sample_from_table(id_sample='c85779fd',
#                                                     path_table='')
#         expected = {'title': '', 'id': 'c85779fd', 'questions': [...]}
#         self.assertEqual(obtained, expected)


#     TABLE_EMPTY = []
#     @patch('adaptive_learning.questionnaires.funcs.load_table', return_value=TABLE_EMPTY)
#     def test_retrieve_sample_from_table_when_is_empty(self, mock_table):
#         with self.assertRaises(ValueError) as context:
#             db.retrieve_sample_from_table(id_sample='c85779fd',
#                                                     path_table='')
#         self.assertTrue('Missing sample id c85779fd' in str(context.exception))


#     TABLE_DUPLICATES = [
#         {'title': '', 'id': 'c85779fd', 'questions': [...]},
#         {'title': '', 'id': 'c85779fd', 'questions': [...]},
#     ]
#     @patch('adaptive_learning.questionnaires.funcs.load_table', return_value=TABLE_DUPLICATES)
#     def test_retrieve_sample_from_table_when_duplicates(self, mock_table):
#         with self.assertRaises(ValueError) as context:
#             db.retrieve_sample_from_table(id_sample='c85779fd',
#                                                     path_table='')
#         self.assertTrue('Duplicate sample ids c85779fd' in str(context.exception))



class QuestionTestCase(unittest.TestCase):
    """
    Test the manipulations on questions and answers
    (create, amend, delete, launch, etc.)
    """
    # TODO: maybe replace the self.mock_inputs by a classic patch deorator,
    # which indicates more explicitly the functions that require patching.
    def setUp(self):
        self.INIT_INPUTS = ('Debug question text', 'keyword1, keyword2')
        self.VALS = {
            'id': '8148773d-773f-42a8-977a-4cbbcee752c1',
            'text': 'Debug question text',
            'keywords': 'keyword1, keyword2',
            'use_question': True,
            'nb_points': 1.,
            'difficulty': 1,
            'answers': [],
        }
        # This patcher will replace any call of 'input'
        # Its property enables to modify the behavior of the patch
        # using self.mock_inputs.side_effect = (list_of_values)
        patcher = patch('builtins.input', side_effect=self.INIT_INPUTS)
        self.mock_inputs = patcher.start()
        self.addCleanup(patcher.stop)

        self.question = Question()


    def test__init__(self):
        # Test init from the setUp
        self.assertEqual(type(self.question._id), type(self.VALS['id']))
        self.assertEqual(len(self.question._id), len(self.VALS['id']))
        self.assertEqual(self.question._text, self.VALS['text'])
        self.assertEqual(self.question._keywords, self.VALS['keywords'])
        self.assertEqual(self.question._use_question, self.VALS['use_question'])
        self.assertEqual(self.question._nb_points, self.VALS['nb_points'])
        self.assertEqual(self.question._difficulty, self.VALS['difficulty'])
        self.assertEqual(self.question._answers, self.VALS['answers'])


    def test_make_exportable(self):
        expected = self.VALS
        obtained = self.question.make_exportable()
        # No need to compare ids since different by design
        del expected['answers']
        del expected['id']
        del obtained['id']
        self.assertEqual(obtained, expected)


    def test_load(self):
        load_dic = {
            'id': '234-aze',
            'text': 'foo',
            'keywords': 'bar1, bar2',
            'use_question': False,
            'nb_points': 5,
            'difficulty': 3,
            'answers': [],
        }
        self.question.load(load_dic)
        self.assertEqual(self.question._id, load_dic['id'])
        self.assertEqual(self.question._text, load_dic['text'])
        self.assertEqual(self.question._keywords, load_dic['keywords'])
        self.assertEqual(self.question._use_question, load_dic['use_question'])
        self.assertEqual(self.question._nb_points, load_dic['nb_points'])
        self.assertEqual(self.question._difficulty, load_dic['difficulty'])
        self.assertEqual(self.question._answers, load_dic['answers'])



class McqQuestionTestCase(unittest.TestCase):
    """
    Test the manipulations with McqQuestion
    """
    ONE_ANSWER = ('Debug question text',
                    'keyword1, keyword2',
                    'Debug answer',
                    'True',
                    'Yes',
                    'No')


    @patch('builtins.input', side_effect=ONE_ANSWER)
    def setUp(self, mock_inputs):
        self.VALS = {
            'id': '8148773d-773f-42a8-977a-4cbbcee752c1',
            'type': 'mcq',
            'text': 'Debug question text',  #ONE_ANSWER[0]
            'keywords': 'keyword1, keyword2',  #ONE_ANSWER[1]
            'use_question': True,
            'nb_points': 1.,
            'difficulty': 1,
            'notif_correct_answers': True,
            'notif_num_exact_answers': False,
            'randomize_answers_order': True,
            'answers': [],
        }
        self.mcq_question = McqQuestion()


    TWO_ANSWERS = (
        'Text answer 1',  # text
        'True',           # is_correct
        'Yes',            # use_answer
        'Yes',            # compose new answer
        'Text answer 2',
        'False',
        'No',
        'No',
    )
    @patch('builtins.input', side_effect=TWO_ANSWERS)
    def test_add_answers(self, mock_inputs):
        self.mcq_question.add_answers()
        self.assertEqual(self.mcq_question._answers[0]._text, 'Debug answer')
        self.assertEqual(self.mcq_question._answers[1]._text, 'Text answer 1')
        self.assertEqual(self.mcq_question._answers[2]._text, 'Text answer 2')
        self.assertTrue(self.mcq_question._answers[0]._is_correct)
        self.assertTrue(self.mcq_question._answers[1]._is_correct)
        self.assertFalse(self.mcq_question._answers[2]._is_correct)
        self.assertTrue(self.mcq_question._answers[0]._use_answer)
        self.assertTrue(self.mcq_question._answers[1]._use_answer)
        self.assertFalse(self.mcq_question._answers[2]._use_answer)


    ONE_ANSWER_ = ('mcq',) + ONE_ANSWER

    @patch('builtins.input', side_effect=ONE_ANSWER_)
    def test_create_question(self, mock_inputs):
        mcq_q = create_question()

        self.assertEqual(mcq_q._type, self.VALS['type'])
        self.assertEqual(mcq_q._text, self.VALS['text'])
        self.assertEqual(mcq_q._keywords, self.VALS['keywords'])
        self.assertEqual(mcq_q._use_question, self.VALS['use_question'])
        self.assertEqual(mcq_q._nb_points, self.VALS['nb_points'])
        self.assertEqual(mcq_q._notif_correct_answers,
                         self.VALS['notif_correct_answers'])
        self.assertEqual(mcq_q._answers[0]._text, 'Debug answer')
        self.assertTrue(mcq_q._answers[0]._is_correct)
        self.assertTrue(mcq_q._answers[0]._use_answer)


    def test_load(self):
        load_dic = {
            'id': '234-aze',
            'type': 'mcq',
            'text': 'foo',
            'keywords': 'bar1, bar2',
            'use_question': False,
            'nb_points': 5,
            'difficulty': 3,
            'notif_correct_answers': self.VALS['notif_correct_answers'],
            'notif_num_exact_answers': self.VALS['notif_num_exact_answers'],
            'randomize_answers_order': self.VALS['randomize_answers_order'],
            'answers': [
                {'text': 'Foo', 'is_correct': False, 'use_answer': False},
                {'text': 'Bar', 'is_correct': True, 'use_answer': True},
            ],
        }
        self.mcq_question.load(load_dic)
        self.assertEqual(self.mcq_question._id, load_dic['id'])
        self.assertEqual(self.mcq_question._text, load_dic['text'])
        self.assertEqual(self.mcq_question._keywords, load_dic['keywords'])
        self.assertEqual(self.mcq_question._use_question, load_dic['use_question'])
        self.assertEqual(self.mcq_question._nb_points, load_dic['nb_points'])
        self.assertEqual(self.mcq_question._difficulty, load_dic['difficulty'])

        self.assertEqual(self.mcq_question._answers[0]._text,
                         load_dic['answers'][0]['text'])
        self.assertEqual(self.mcq_question._answers[0]._is_correct,
                         load_dic['answers'][0]['is_correct'])
        self.assertEqual(self.mcq_question._answers[0]._use_answer,
                         load_dic['answers'][0]['use_answer'])

        self.assertEqual(self.mcq_question._answers[1]._text,
                         load_dic['answers'][1]['text'])
        self.assertEqual(self.mcq_question._answers[1]._is_correct,
                         load_dic['answers'][1]['is_correct'])
        self.assertEqual(self.mcq_question._answers[1]._use_answer,
                         load_dic['answers'][1]['use_answer'])


    def test_make_exportable(self):
        expected = {
            'id': 'uuid4_string',
            'type': self.VALS['type'],
            'text': self.VALS['text'],
            'keywords': self.VALS['keywords'],
            'use_question': self.VALS['use_question'],
            'nb_points': self.VALS['nb_points'],
            'difficulty': self.VALS['difficulty'],
            'notif_correct_answers': self.VALS['notif_correct_answers'],
            'notif_num_exact_answers': self.VALS['notif_num_exact_answers'],
            'randomize_answers_order': self.VALS['randomize_answers_order'],
            'answers': [{'text': 'Debug answer',
                         'is_correct': True,
                         'use_answer': True}],
        }
        obtained = self.mcq_question.make_exportable()
        del expected['id']  # Delete id since uuid is different at each call
        del obtained['id']
        self.assertEqual(obtained, expected)



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
