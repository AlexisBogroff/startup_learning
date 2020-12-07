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
    """
    question = {}
    question['text'] = get_input("Enter the question text")
    question['format'] = get_input("Enter the question format")
    question['use_question'] = get_input("Use this question? (True/False)")
    question['nb_points'] = get_input("Enter the number of points")
    question['difficulty'] = get_input("Enter the difficulty")
    question['keywords'] = get_input("Enter keywords, subject, or categories")
    question['notif_correct_answers'] = get_input("Inform num correct answers?")
    question['randomize_answers_order'] = get_input("Randomize answers order?")
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

    TODO: implement set_questions function and everything that can link exams
    with questions and answers
    """
    def __init__(self):
        self.title = ""
        self.description = ""
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
            'id': str(uuid.uuid4()),
            'title': self.title,
            'description': self.description,
            'randomize_questions_order': self.randomize_questions_order,
            'auto_rebase_grade': self.auto_rebase_grade,
            'grade_base': self.grade_base,
        }
        return data_dump


    def load(self, id_exam):
        """
        Load a specific exam from the exam database

        It modifies the properties of the current exam to correspond to the
        exam selected.

        Returns:
            void.
        """
        raise NotImplementedError


    def save(self):
        """
        Stores the exam in a JSON file

        It inserts the new content at the end of the file,
        on a new line, and takes a single line

        Notes:
            Each exam is stored in json format, but the file is in text format.
            This enables to store new exams by appending them in the first empty
            rows, without the need to read and parse the whole file
            (which would be the case with a json file).
        """
        exam_dump = self.get_dump()
        insert_to_exams_file(exam_dump)


    def set_properties(self):
        """
        Set all the properties from user input

        Returns:
            void
        """
        self.set_title()
        self.set_description()
        self.set_randomize_order()
        self.set_auto_rebase_grade()
        self.set_grade_base()


    def set_title(self):
        """ Set title property """
        self.title = get_input("Enter the exam title")

    def set_description(self):
        """ Set description property """
        self.description = get_input("Enter the exam description")

    def set_randomize_order(self):
        """ Set randomize_order property """
        randomize_order = get_input("Randomize questions order?")
        casted_randomize_order = cast(randomize_order, bool)
        self.randomize_questions_order = casted_randomize_order

    def set_auto_rebase_grade(self):
        """ Set auto_rebase_grade property """
        auto_rebase = get_input("Activate automatic grade rebasing?")
        casted_auto_rebase = cast(auto_rebase, bool)
        self.auto_rebase_grade = casted_auto_rebase

    def set_grade_base(self):
        """ Set grade_base property """
        grade_base = get_input("Enter the grade base")
        casted_grade_base = cast(grade_base, int)
        self.grade_base = casted_grade_base


    def set_properties_from_db_load(self):
        raise NotImplementedError

    def set_questions(self):
        raise NotImplementedError



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
    exam.set_properties()
