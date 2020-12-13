"""
Manage exams, questions and answers
"""
import json
import uuid

# TODO: create a class db for functions interacting with tables
# and extracting data (e.g. extract_question)
from adaptive_learning.funcs import append_to_file, \
                                    cast, \
                                    generate_uuid, \
                                    get_input, \
                                    load_table

from adaptive_learning import funcs


__PATH_EXAMS__ = "/Users/Pro/git_repositories/"\
    "adaptive_learning/adaptive_learning/adaptive_learning/"\
    "data/table_exams.txt"

__PATH_QUESTIONS__ = "/Users/Pro/git_repositories/"\
    "adaptive_learning/adaptive_learning/adaptive_learning/"\
    "data/table_questions.txt"


def create_answer():
    """
    Create an answer. Add to answers list.

    Returns:
        void.

    TODO: create a class Answer (with default use_answer=True)
    """
    answer = {}
    answer['text'] = get_input("Enter the answer text")
    answer['is_correct'] = get_input("Is the answer correct? (True/False)")
    answer['use_answer'] = get_input("Do use this answer? (True/False)")
    return answer



class Exam:
    """
    Class to manage exams (creation, modification, deletion) and compose their
    questions and corresponding answers.

    grade_rebase: enables to obtain a grade on e.g. /20, although there
    are only e.g. 10 questions graded /1 point.

    Args:
        title: of the exam

    Returns:
        exam instance with its basic properties set, and ready to be composed.

    Methods:
        create_question
        extract_exam
        get_exportable
        get_question_position_id
        load_exam
        save_new_to_db
        set_auto_rebase_grade_from_existing
        set_auto_rebase_grade_from_input
        set_description_from_existing
        set_description_from_input
        set_grade_base_from_existing
        set_grade_base_from_input
        set_id_from_existing
        set_properties_from_existing_all
        set_properties_from_input_extra
        set_properties_from_input_main
        set_randomize_order_from_existing
        set_randomize_questions_order_from_input
        set_title_from_existing
        set_title_from_input
        update


    Notes:
        The structure of exam has its main and secondary parameters at the same
        level. The structure of the dump is different and may lead to useless
        complexity and confusion, since its secondary parameters are stored in
        a list called 'parameters'.
    """
    def __init__(self):
        self._id = ''
        # Main parameters
        self.title = ""
        self.description = ""
        # Extra parameters
        self.randomize_questions_order = True
        self.auto_rebase_grade = True
        self.grade_base = 20
        # Questions
        self.questions = []


    def create_question(self):
        """
        Create and add a question to the exam list of questions property
        """
        question = Question()
        question.set_parameters_from_input_main()
        question_export = question.get_exportable()
        question_export['position_id'] = self.generate_position_id()
        self.questions.append(question_export)


    def get_exportable(self):
        """
        Stores exam properties in a dictionary

        Returns:
            the data in dic format, ready to export in json file
        """
        data_export = {
            'id': self._id,
            'title': self.title,
            'description': self.description,
            'parameters': {
                'randomize_questions_order': self.randomize_questions_order,
                'auto_rebase_grade': self.auto_rebase_grade,
                'grade_base': self.grade_base,
            },
            'questions': self.questions,
        }
        return data_export


    def generate_position_id(self):
        """
        Generate question id based on its relative position

        Id is defined as the number of the question. Since the question is
        added last, it is an incremented id.
        """
        num_of_questions = len(self.questions)
        question_id = num_of_questions + 1
        return question_id


    def load_exam(self, id_exam):
        """
        Load a specific exam from the exam table

        Modifies the properties of the current exam to correspond to the
        selected exam.

        Returns:
            void.
        """
        exam_data = funcs.retrieve_sample_from_table(id_exam, __PATH_EXAMS__)
        self.set_exam_from_existing(exam_data)


    def set_exam_from_existing(self, exam_data):
        """
        Set exam properties and questions (wt answers)

        Returns:
            Void
        """
        self.set_properties_from_existing_all(exam_data)
        self.questions = exam_data['questions']


    def save_new_to_db(self):
        """
        Stores the exam in database

        It inserts the new content at the end of the file,
        on a new line, and takes a single line (each in json like format)

        Method should be executed one time only, when finished with the creation
        of the exam. Otherwise, the exam would be stored (with a new id) each
        time save method would be called.

        Notes:
            To increase performances, each exam is stored in json format,
            even though the file is in text format.
            This enables to store new exams by appending them in the first empty
            rows, without the need to read and parse the whole file
            (which would be the case with a json file).
        """
        self._id = generate_uuid()
        exam_dump = self.get_exportable()
        append_to_file(exam_dump, __PATH_EXAMS__)


    def set_auto_rebase_grade_from_existing(self, exam_data):
        """ Load auto_rebase_grade parameter from existing exam """
        param = exam_data['parameters']['auto_rebase_grade']
        self.auto_rebase_grade = param

    def set_auto_rebase_grade_from_input(self):
        """ Set auto_rebase_grade property """
        auto_rebase = get_input("Activate automatic grade rebasing?")
        casted_auto_rebase = cast(auto_rebase, bool)
        self.auto_rebase_grade = casted_auto_rebase


    def set_description_from_existing(self, exam_data):
        """ Load description from existing exam """
        self.description = exam_data['description']

    def set_description_from_input(self):
        """ Set description property """
        self.description = get_input("Enter the exam description")


    def set_grade_base_from_existing(self, exam_data):
        """ Load grade_base parameter from existing exam """
        param = exam_data['parameters']['grade_base']
        self.grade_base = param


    def set_grade_base_from_input(self):
        """ Set grade_base property """
        grade_base = get_input("Enter the grade base")
        casted_grade_base = cast(grade_base, int)
        self.grade_base = casted_grade_base


    def set_id_from_existing(self, exam_data):
        """ Load id from existing exam """
        self._id = exam_data['id']


    def set_properties_from_existing_all(self, exam_data):
        """ Set the properties from an existing exam """
        self.set_id_from_existing(exam_data)
        self.set_title_from_existing(exam_data)
        self.set_description_from_existing(exam_data)
        self.set_randomize_questions_order_from_existing(exam_data)
        self.set_auto_rebase_grade_from_existing(exam_data)
        self.set_grade_base_from_existing(exam_data)

    def set_properties_from_input_extra(self):
        """
        Set the extra properties from user input
        """
        self.set_randomize_questions_order_from_input()
        self.set_auto_rebase_grade_from_input()
        self.set_grade_base_from_input()

    def set_properties_from_input_main(self):
        """
        Set the main properties from user input
        """
        self.set_title_from_input()
        self.set_description_from_input()


    def set_randomize_questions_order_from_existing(self, exam_data):
        """ Load randomize_questions_order parameter from existing exam """
        param = exam_data['parameters']['randomize_questions_order']
        self.randomize_questions_order = param

    def set_randomize_questions_order_from_input(self):
        """ Set randomize_order property """
        randomize_order = get_input("Randomize questions order?")
        casted_randomize_order = cast(randomize_order, bool)
        self.randomize_questions_order = casted_randomize_order


    def set_title_from_existing(self, exam_data):
        """ Load title from existing exam """
        self.title = exam_data['title']

    def set_title_from_input(self):
        """ Set title property """
        self.title = get_input("Enter the exam title")


    def update(self, id_exam):
        """
        Update an existing exam

        Notes:
            Implement a method to find a specific id in the db file, and get the
            corresponding row number. Then delete this row. Finally, add the
            updated version of the exam.
        """
        raise NotImplementedError



class Question:
    """
    Class for the questions.

    They can be dealt independantly (of exams) or be called in the creation
    of an exam. The answers are called in the creation of a question.

    Methods:
        create_answer
        get_exportable
        save_new_to_db
        set_parameters_from_input_extra
        set_parameters_from_input_main
        load_question
        extract_question
        set_properties_from_existing
    """
    def __init__(self):
        self._id = ''
        # Main parameters
        self.text = ''
        self.type = ''
        self.keywords = ''  # TODO: transform into a list rather than a string
        # Extra parameters (with default value)
        self.use_question = True
        self.nb_points = 1.
        self.difficulty = 1
        self.notif_correct_answers = True
        self.notif_num_exact_answers = False
        self.randomize_answers_order = True
        # Answers
        self.answers = []


    def get_exportable(self):
        """
        Stores the question properties in a dictionary

        Returns:
            the data in dic format, ready to export in json file
        """
        data_export = {
            'id': self._id,
            'text': self.text,
            'type': self.type,
            'keywords': self.keywords,
            'parameters': {
                'use_question': self.use_question,
                'nb_points': self.nb_points,
                'difficulty': self.difficulty,
                'notif_correct_answers': self.notif_correct_answers,
                'notif_num_exact_answers': self.notif_num_exact_answers,
                'randomize_answers_order': self.randomize_answers_order,
            },
            'answers': self.answers,
        }
        return data_export


    def save_new_to_db(self):
        """
        Stores the question in database

        It inserts the new content at the end of the file,
        on a new line, and takes a single line (each in json like format)

        Method should be executed one time only, when finished with the creation
        of the question. Otherwise, the question would be stored (with a new id)
        each time save method would be called.

        Notes:
            To increase performances, each question is stored in json format,
            even though the file is in text format.
            This enables to store new questions by appending them in the first
            empty rows, without the need to read and parse the whole file
            (which would be the case with a json file).
        """
        self._id = generate_uuid()
        question_dump = self.get_exportable()
        append_to_file(question_dump, __PATH_QUESTIONS__)


    def set_parameters_from_input_extra(self):
        """
        Set question parameters

        These parameters all have a default value, and their manual setting
        is not necessary.

        It is important to fill the 'keywords' argument, since it enables
        the filtering of questions on these keywords when building exams. It
        is a rich data for algorithms.

        Notes:
            use_question: bool
            nb_points: float
            difficulty: int
            notif_correct_answers: bool:
            - False (informs that question has one or multiple correct answers)
            - True (informs wether question has multiple correct answers or not)
            notif_num_exact_answers: bool (only if notif_correct_answers is True)
            randomize_answers_order: bool
        """
        # Get informations from user input
        self.use_question = get_input("Use this question?")
        self.nb_points = get_input("Enter the number of points")
        self.difficulty = get_input("Enter the difficulty")
        self.notif_correct_answers = get_input("Inform on num of answers?")
        self.notif_num_exact_answers = get_input("Inform exact num?")
        self.randomize_answers_order = get_input("Randomize answers order?")

        # Cast variables to expected type
        self.use_question = cast(self.use_question, bool)
        self.nb_points = cast(self.nb_points, float)
        self.difficulty = cast(self.difficulty, int)
        self.notif_correct_answers = cast(self.notif_correct_answers, bool)
        self.notif_num_exact_answers = cast(self.notif_num_exact_answers, bool)
        self.randomize_answers_order = cast(self.randomize_answers_order, bool)


    def set_parameters_from_input_main(self):
        """
        Set the question necessary informations

        These parameters can not have a default value

        Notes:
            text: string
            type: string, can be:
            - mcq (single or mulitple correct answers)
            - exact
            - develop (developpement answer that can hardly be auto-corrected)
            keywords: string with comma separated words
        """
        self.text = get_input("Enter the question text")
        self.type = get_input("Enter the question type")
        self.keywords = get_input("Enter keywords, subject, or categories")


    def load_question(self, id_question):
        """
        Load a specific question from the questions library

        Modifies the properties of the current question to correspond to the
        selected question.

        Returns:
            void.
        """
        question_data = funcs.retrieve_sample_from_table(id_question,
                                                         __PATH_QUESTIONS__)
        self.set_question_from_existing(question_data)


    def set_question_from_existing(self, question_data):
        """ Set properties from an existing question """
        self._id = question_data['id']
        self.text = question_data['text']
        self.type = question_data['type']
        self.keywords = question_data['keywords']
        self.use_question = \
            question_data['parameters']['use_question']
        self.nb_points = \
            question_data['parameters']['nb_points']
        self.difficulty = \
            question_data['parameters']['difficulty']
        self.notif_correct_answers = \
            question_data['parameters']['notif_correct_answers']
        self.notif_num_exact_answers = \
            question_data['parameters']['notif_num_exact_answers']
        self.randomize_answers_order = \
            question_data['parameters']['randomize_answers_order']
        self.answers = question_data['answers']



if __name__ == "__main__":
    # Test exam
    # exam = Exam()
    # exam.load_exam("f67d625b-b569-487e-91fc-0ac14ca0bc81")
    # print('end')
    # question1 = Question()
    # question1.set_parameters_from_input_main()
    # question1.save_new_to_db()
    question2 = Question()
    question2.load_question('9b693fe2-6732-4daf-83a8-00ad25ceaadb')
    print('end')