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
# TODO: see if it could also work with a txt file, since json rows
# are append, it is rather used as a txt file than a json file
# (since a json file would require that the whole file be a json)
# (which I'm preventing to avoid requiring to load the whole base at each I/O)
# (thus, it like a json, but without the parenthesis that should surround
# all the rows)
#
# Writing on the txt file is working properly.
# But reading does not work for now, for neither txt nor json


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
    def __init__(self, title):
        self.title = title
        self.description = ""
        self.randomize_questions_order = True
        self.auto_rebase_grade = True
        self.grade_base = 20


    def set_properties(self):
        self.title = get_input("Enter the exam title")

        self.description = get_input("Enter the exam description")

        randomize_order = get_input("Randomize questions order?")
        casted_randomize_order = cast(randomize_order, bool)
        self.randomize_questions_order = casted_randomize_order

        auto_rebase = get_input("Activate automatic grade rebasing?")
        casted_auto_rebase = cast(auto_rebase, bool)
        self.auto_rebase_grade = casted_auto_rebase

        grade_base = get_input("Enter the grade base")
        casted_grade_base = cast(grade_base, int)
        self.grade_base = casted_grade_base


    def set_questions(self):
        raise NotImplementedError


    def save(self):
        """
        Stores the exam in a JSON file

        It inserts the new content at the end of the file,
        on a new line, and takes a single line
        """
        self.insert_to_exams_file()


    def insert_to_exams_file(self):
        """ Append the new exam to the existing JSON file """
        with open(__PATH_EXAMS__, 'a') as f:
            exam_dump = self._prepare_export()
            json.dump(exam_dump, f)
            funcs.add_end_of_line_to_file(f)


    def _prepare_export(self):
        """
        Stores exam information in a dictionary

        Returns:
            the data in dic format, ready to export in json file

        TODO: add self.questions when set_questions implemented
        """
        data_export = {
            'id': str(uuid.uuid4()),
            'title': self.title,
            'description': self.description,
            'randomize_questions_order': self.randomize_questions_order,
            'auto_rebase_grade': self.auto_rebase_grade,
            'grade_base': self.grade_base,
        }
        return data_export


        # TODO: load data from table exams
        # when loading, try to load only what is required
        # (maybe not the whole file)
        # use readlines:
        # [json.loads(row) for row in open('table_exams.json','r').readlines()]
        #
        def load_table_exams():
            """
            Returns the content of the json file
            in a dictionary
            """
            with open(__PATH_EXAMS__, 'r') as f_exams:
                table_exams = json.load(f_exams)

            return table_exams


if __name__ == "__main__":
    exam = Exam('initial title')
    exam.set_properties()
