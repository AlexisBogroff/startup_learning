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


class Answer:
    """
    Class to manage answers
    """
    def __init__(self):
        self.text = ''
        self.is_correct = False
        self.use_answer = True


    def set_properties_from_input(self):
        """
        Create an answer

        Returns:
            None, it modifies the answer properties.
        """
        self.set_text_from_input()
        self.set_is_correct_from_input()
        self.set_use_answer_from_input()


    def set_text_from_input(self):
        """ Set is_correct property """
        self.text = get_input("Enter the answer text")


    def set_is_correct_from_input(self):
        """ Set is_correct property """
        is_correct = get_input("Is the answer correct? (True/False)")
        casted_is_correct = cast(is_correct, bool)
        self.is_correct = casted_is_correct


    def set_use_answer_from_input(self):
        """ Set use_answer property """
        use_answer = get_input("Use this answer? (True/False)")
        casted_use_answer = cast(use_answer, bool)
        self.use_answer = casted_use_answer


    def get_exportable(self):
        """
        Stores the answer properties in a dictionary

        Returns:
            the data in dic format, ready to be added to the list of answers
            of a question.
        """
        data_export = {
            'text': self.text,
            'is_correct': self.is_correct,
            'use_answer': self.use_answer,
        }
        return data_export



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

    TODO: add method to save questions of the exam to the library questions.json
    """
    def __init__(self):
        self._id = ''
        # Main parameters
        self.title = ""
        self.description = ""
        # Other parameters
        self.randomize_questions_order = True
        self.auto_rebase_grade = True
        self.grade_base = 20
        # Questions
        self.questions = []


    def __str__(self):
        return "title: {title}, id: {id}".format(title=self.title, id=self._id)


    def add_question(self, method='create', load_id=None):
        """
        Choose add method: create or load
        """
        if method == 'create':
            self._create_question()
        elif method == 'load':
            q = Question()
            q.load_question(load_id)
            q_export = q.get_exportable()
            self.questions.append(q_export)


    def _create_question(self):
        """
        Create and add a question to the exam list of questions property
        """
        question = Question()
        question.create_question()
        question_export = question.get_exportable()
        question_export['position_id'] = \
            funcs.generate_position_id(self.questions)
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
            'randomize_questions_order': self.randomize_questions_order,
            'auto_rebase_grade': self.auto_rebase_grade,
            'grade_base': self.grade_base,
            'questions': self.questions,
        }
        return data_export


    def load_exam(self, id_exam):
        """
        Load a specific exam from the exam table

        Modifies the properties of the current exam to correspond to the
        selected exam.

        Returns:
            void.
        """
        exam = funcs.retrieve_sample_from_table(id_exam, __PATH_EXAMS__)
        self.set_properties_from_existing_all(exam)
        self.questions = exam['questions']


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


    def set_auto_rebase_grade_from_existing(self, exam):
        """ Load auto_rebase_grade parameter from existing exam """
        param = exam['auto_rebase_grade']
        self.auto_rebase_grade = param


    def set_auto_rebase_grade_from_input(self):
        """ Set auto_rebase_grade property """
        auto_rebase = get_input("Activate automatic grade rebasing?")
        casted_auto_rebase = cast(auto_rebase, bool)
        self.auto_rebase_grade = casted_auto_rebase


    def set_description_from_existing(self, exam):
        """ Load description from existing exam """
        self.description = exam['description']


    def set_description_from_input(self):
        """ Set description property """
        self.description = get_input("Enter the exam description")


    def set_grade_base_from_existing(self, exam):
        """ Load grade_base parameter from existing exam """
        param = exam['grade_base']
        self.grade_base = param


    def set_grade_base_from_input(self):
        """ Set grade_base property """
        grade_base = get_input("Enter the grade base")
        casted_grade_base = cast(grade_base, int)
        self.grade_base = casted_grade_base


    def set_id_from_existing(self, exam):
        """ Load id from existing exam """
        self._id = exam['id']


    def set_properties_from_existing_all(self, exam):
        """ Set the properties from an existing exam """
        self.set_id_from_existing(exam)
        self.set_title_from_existing(exam)
        self.set_description_from_existing(exam)
        self.set_randomize_questions_order_from_existing(exam)
        self.set_auto_rebase_grade_from_existing(exam)
        self.set_grade_base_from_existing(exam)


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


    def set_randomize_questions_order_from_existing(self, exam):
        """ Load randomize_questions_order parameter from existing exam """
        param = exam['randomize_questions_order']
        self.randomize_questions_order = param


    def set_randomize_questions_order_from_input(self):
        """ Set randomize_order property """
        randomize_order = get_input("Randomize questions order?")
        casted_randomize_order = cast(randomize_order, bool)
        self.randomize_questions_order = casted_randomize_order


    def set_title_from_existing(self, exam):
        """ Load title from existing exam """
        self.title = exam['title']


    def set_title_from_input(self):
        """ Set title property """
        self.title = get_input("Enter the exam title")


    def show(self):
        """
        Display the exam properties

        TODO: split into multiple functions
        """
        questions = self.questions
        if questions:
            text_questions = ["({nb_points}) {type}: {text}"\
                .format(nb_points=q['nb_points'],
                        type=q['type'],
                        text=q['text']) \
                            for q in questions]

            text_questions = "\n\t".join(text_questions)
        else:
            text_questions = "No question registered"

        text = "id: {id}\n" \
               "title: {title}\n" \
               "description: {description}\n\n" \
               "randomize_questions_order: {randomize_questions_order}\n" \
               "auto_rebase_grade: {auto_rebase_grade}\n" \
               "grade_base: {grade_base}\n\n" \
               "questions\n" \
               "\t{text_questions}" \
               .format(
                    id=self._id,
                    title=self.title,
                    description=self.description,
                    randomize_questions_order=self.randomize_questions_order,
                    auto_rebase_grade=self.auto_rebase_grade,
                    grade_base=self.grade_base,
                    text_questions=text_questions,
                )
        print(text)


    @staticmethod
    def show_list_of_exams():
        """ Display the list of exams stored in db """
        table = load_table(f_path=__PATH_EXAMS__)
        funcs.show_table(table, ['title', 'id'])


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


    def __str__(self):
        return "text: {text}, id: {id}".format(text=self.text, id=self._id)


    def add_answer(self):
        """
        Create and add an answer to the current question
        """
        answer = Answer()
        answer.set_properties_from_input()
        answer_export = answer.get_exportable()
        answer_export['position_id'] = funcs.generate_position_id(self.answers)
        self.answers.append(answer_export)


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
            'use_question': self.use_question,
            'nb_points': self.nb_points,
            'difficulty': self.difficulty,
            'notif_correct_answers': self.notif_correct_answers,
            'notif_num_exact_answers': self.notif_num_exact_answers,
            'randomize_answers_order': self.randomize_answers_order,
            'answers': self.answers,
        }
        return data_export


    def load_question(self, id_question):
        """
        Load a specific question from the questions library

        Modifies the properties of the current question to correspond to the
        selected question.

        Returns:
            void.
        """
        question = funcs.retrieve_sample_from_table(id_question,
                                                         __PATH_QUESTIONS__)
        self.set_question_from_existing(question)


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


    def create_question(self):
        """
        Create question

        Some parameters are add with their default value

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


    def set_question_from_existing(self, question):
        """ Set properties from an existing question """
        self._id = question['id']
        self.text = question['text']
        self.type = question['type']
        self.keywords = question['keywords']
        self.use_question = question['use_question']
        self.nb_points = question['nb_points']
        self.difficulty = question['difficulty']
        self.notif_correct_answers = question['notif_correct_answers']
        self.notif_num_exact_answers = question['notif_num_exact_answers']
        self.randomize_answers_order = question['randomize_answers_order']
        self.answers = question['answers']


    def show(self):
        """
        Display the question properties

        TODO: split into multiple functions
        """
        answers = self.answers
        if answers:
            text_answers = ["{}".format(ans) for ans in answers]
            text_answers = "\n\t".join(text_answers)
        else:
            text_answers = "No answer registered"

        text = "id: {id}\n" \
               "text: {text}\n" \
               "type: {type}\n" \
               "keywords: {keywords}\n\n" \
               "use_question: {use_question}\n" \
               "nb_points: {nb_points}\n" \
               "difficulty: {difficulty}\n" \
               "notif_correct_answers: {notif_correct_answers}\n" \
               "notif_num_exact_answers: {notif_num_exact_answers}\n" \
               "randomize_answers_order: {randomize_answers_order}\n\n" \
               "answers\n" \
               "\t{text_answers}" \
               .format(
                    id=self._id,
                    text=self.text,
                    type=self.type,
                    keywords=self.keywords,
                    use_question=self.use_question,
                    nb_points=self.nb_points,
                    difficulty=self.difficulty,
                    notif_correct_answers=self.notif_correct_answers,
                    notif_num_exact_answers=self.notif_num_exact_answers,
                    randomize_answers_order=self.randomize_answers_order,
                    text_answers=text_answers,
                )
        print(text)


    @staticmethod
    def show_list_of_questions():
        """ Display the list of questions stored in db """
        table = load_table(f_path=__PATH_QUESTIONS__)
        funcs.show_table(table, ['text', 'id'])




if __name__ == "__main__":
    # Test answer
    # question2 = Question()
    # question2.load_question('9b693fe2-6732-4daf-83a8-00ad25ceaadb')
    # question2.add_answer()
    # question2.add_answer()

    # Test displays
    ## Display list of exams
    # exam = Exam()
    # exam.get_list_of_exams()

    ## Display list of questions
    question = Question()
    question.show_list_of_questions()


