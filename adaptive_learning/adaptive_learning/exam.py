"""
Manage exams

TODO: create a class db for functions interacting with tables
and extracting data (e.g. extract_question)
"""
from adaptive_learning import funcs
from adaptive_learning.funcs import cast, get_input
from adaptive_learning.question import Question

__PATH_EXAMS__ = "/Users/Pro/git_repositories/"\
    "adaptive_learning/adaptive_learning/adaptive_learning/"\
    "data/table_exams.txt"


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
        self.title = ""
        self.description = ""
        self.randomize_questions_order = True
        self.auto_rebase_grade = True
        self.grade_base = 20
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
        self._id = funcs.generate_uuid()
        exam_dump = self.get_exportable()
        funcs.append_to_file(exam_dump, __PATH_EXAMS__)


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
        table = funcs.load_table(f_path=__PATH_EXAMS__)
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


