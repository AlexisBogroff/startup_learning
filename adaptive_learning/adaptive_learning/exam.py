"""
Manage exams, questions and answers
"""
import json
import uuid

from adaptive_learning import funcs
from adaptive_learning.funcs import get_input, \
                                    cast

__PATH_EXAMS__ = "/Users/Pro/git_repositories/"\
    "adaptive_learning/adaptive_learning/adaptive_learning/"\
    "data/table_exams.txt"


def create_question():
    """
    Create a question

    It is important to fill the 'keywords' argument, since it enables
    the filtering of questions on these keywords when building exams

    Returns:
        the question dictonary

    Notes:
        text: string
        type: string, can be:
        - mcq (single or mulitple correct answers)
        - exact
        - develop (developpement answer that can hardly be auto-corrected)
        use_question: bool
        nb_points: float
        difficulty: int
        keywords: string with comma separated words
        notif_correct_answers: bool:
        - False (informs that question has one or multiple correct answers)
        - True (informs wether question has multiple correct answers or not)
        notif_num_exact_answers: bool (only if notif_correct_answers is True)
        randomize_answers_order: bool
    """
    # Get informations from user input
    question = {}
    question['text'] = get_input("Enter the question text")
    question['type'] = get_input("Enter the question type")
    question['use_question'] = get_input("Use this question?")
    question['nb_points'] = get_input("Enter the number of points")
    question['difficulty'] = get_input("Enter the difficulty")
    question['keywords'] = get_input("Enter keywords, subject, or categories")
    question['notif_correct_answers'] = get_input("Inform on num of answers?")
    question['notif_num_exact_answers'] = get_input("Inform exact num?")
    question['randomize_answers_order'] = get_input("Randomize answers order?")

    # Cast variables to expected type
    question['use_question'] = cast(question['use_question'], bool)
    question['nb_points'] = cast(question['nb_points'], float)
    question['difficulty'] = cast(question['difficulty'], int)
    question['notif_correct_answers'] = cast(
        question['notif_correct_answers'], bool)
    question['notif_num_exact_answers'] = cast(
        question['notif_num_exact_answers'], bool)
    question['randomize_answers_order'] = cast(
        question['randomize_answers_order'], bool)

    return question


def create_answer():
    """
    Create an answer

    Returns:
        the answer dictionary
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

    Notes:
        The structure of exam has its main and secondary parameters at the same
        level. The structure of the dump is different and may lead to useless
        complexity and confusion, since its secondary parameters are stored in
        a list called 'parameters'.

    TODO: implement set_questions function and everything that can link exams
    with questions and answers
    """
    def __init__(self):
        self._id = ""
        self.title = ""
        self.description = ""
        self.questions = []
        # Parameters
        self.randomize_questions_order = True
        self.auto_rebase_grade = True
        self.grade_base = 20


    def get_dump(self):
        """
        Stores exam information in a dictionary

        Returns:
            the data in dic format, ready to export in json file

        TODO: add self.questions when set_questions implemented
        """
        data_dump = {
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
        return data_dump


    def load_exam(self, id_exam):
        """
        Load a specific exam from the exam database

        It modifies the properties of the current exam to correspond to the
        exam selected.

        Returns:
            void.
        """
        db = load_table_exams()
        exam_data = self.extract_exam(id_exam, db)
        questions = exam_data['questions']
        self.set_properties(exam_data)
        self.set_questions(questions)


    def extract_exam(self, id_exam, db):
        """
        Extract the specific exam and apply sanity checks
        """
        exam_data = [exam for exam in db if exam['id'] == id_exam]

        if not exam_data:
            raise ValueError("Missing: not found with id: {}".format(id_exam))
        if len(exam_data) > 1:
            raise ValueError("Duplicates found for id: {}".format(id_exam))
        if len(exam_data) == 1:
            return exam_data[0]


    def update(self, id_exam):
        """
        Update an existing exam

        Notes:
            Implement a method to find a specific id in the db file, and get the
            corresponding row number. Then delete this row. Finally, add the
            updated version of the exam.
        """
        raise NotImplementedError


    def save_new(self):
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
        exam_dump = self.get_dump()
        insert_to_exams_file(exam_dump)


    def set_questions(self, questions=None):
        """ Set questions from user input or from existing """
        if not questions:
            self.create_question()
        else:
            self.load_questions(questions)


    def load_questions(self, loaded_questions):
        """ Load questions from exam """
        self.questions = loaded_questions


    def set_properties(self, exam_data=None):
        """
        Set all the properties

        Set the properties from either an existing exam, or from user input
        if no exam is passed.

        Args:
            exam: the exam data to load if passed

        Returns:
            void
        """
        if not exam_data:
            self.set_title_from_input()
            self.set_description_from_input()
            self.set_randomize_order_from_input()
            self.set_auto_rebase_grade_from_input()
            self.set_grade_base_from_input()
        else:
            self.set_id_from_existing(exam_data)
            self.set_title_from_existing(exam_data)
            self.set_description_from_existing(exam_data)
            self.set_randomize_order_from_existing(exam_data)
            self.set_auto_rebase_grade_from_existing(exam_data)
            self.set_grade_base_from_existing(exam_data)


    def set_id_from_existing(self, exam_data):
        """ Load id from existing exam """
        self._id = exam_data['id']

    def set_title_from_existing(self, exam_data):
        """ Load title from existing exam """
        self.title = exam_data['title']

    def set_description_from_existing(self, exam_data):
        """ Load description from existing exam """
        self.description = exam_data['description']

    def set_randomize_order_from_existing(self, exam_data):
        """ Load randomize_questions_order parameter from existing exam """
        param = exam_data['parameters']['randomize_questions_order']
        self.randomize_questions_order = param

    def set_auto_rebase_grade_from_existing(self, exam_data):
        """ Load auto_rebase_grade parameter from existing exam """
        param = exam_data['parameters']['auto_rebase_grade']
        self.auto_rebase_grade = param

    def set_grade_base_from_existing(self, exam_data):
        """ Load grade_base parameter from existing exam """
        param = exam_data['parameters']['grade_base']
        self.grade_base = param


    def set_title_from_input(self):
        """ Set title property """
        self.title = get_input("Enter the exam title")

    def set_description_from_input(self):
        """ Set description property """
        self.description = get_input("Enter the exam description")

    def set_randomize_order_from_input(self):
        """ Set randomize_order property """
        randomize_order = get_input("Randomize questions order?")
        casted_randomize_order = cast(randomize_order, bool)
        self.randomize_questions_order = casted_randomize_order

    def set_auto_rebase_grade_from_input(self):
        """ Set auto_rebase_grade property """
        auto_rebase = get_input("Activate automatic grade rebasing?")
        casted_auto_rebase = cast(auto_rebase, bool)
        self.auto_rebase_grade = casted_auto_rebase

    def set_grade_base_from_input(self):
        """ Set grade_base property """
        grade_base = get_input("Enter the grade base")
        casted_grade_base = cast(grade_base, int)
        self.grade_base = casted_grade_base


    def create_question(self):
        """
        Create and add a question to the exam list of questions property
        """
        question = create_question()
        question['id'] = self.get_question_id()
        self.questions.append(question)


    def get_question_id(self):
        """
        Generate question id

        Id is defined as the number of the question. Since the question is
        added last, it is an incremented id.
        """
        num_of_questions = len(self.questions)
        question_id = num_of_questions + 1
        return question_id


def generate_uuid(type=str):
    """ Generate unique identifier """
    if type is str:
        return str(uuid.uuid4())


def insert_to_exams_file(exam_dump):
    """ Append the new exam to the existing JSON file """
    with open(__PATH_EXAMS__, 'a') as f_exams:
        json.dump(exam_dump, f_exams)
        funcs.add_end_of_line_to_file(f_exams)


def load_table_exams():
    """
    Loads exams data from a json file

    Returns:
        the whole file content in a list of dictionaries

    Notes:
        This should not be in the Exam class, only a specific exam should be
        loaded as an Exam instance. It could be hosted in a Db class

    TODO: add a method to load only part of the file
    """
    with open(__PATH_EXAMS__, 'r') as f_exams:
        table_exams = [json.loads(row) for row in f_exams]
    return table_exams


if __name__ == "__main__":
    exam = Exam()
    exam.load_exam("f67d625b-b569-487e-91fc-0ac14ca0bc81")
    print(exam.questions)
