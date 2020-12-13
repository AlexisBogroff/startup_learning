import datetime

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from django.urls import reverse
from .views import (
    Moyenne,
    Note_plus_basse,
    Note_plus_haute,
    Q1,
    Q3,
    Mediane,
    Frequences,
    Statistique_question,
    get_questions,
    check_answer,
    get_time,
    get_date,
    add_time,
    compare_date,

)

from .models import DynMCQInfo, DynMCQquestion, DynMCQanswer, PassDynMCQTest, \
    PassDynMCQTestInfo, Dynquestion


# Create your tests here.

def setup_group_permissions():
    content_type = ContentType.objects.get_for_model(DynMCQInfo)
    can_create_test = Permission.objects.create(codename='can_create_test',
                                                name='Can Create Test',
                                                content_type=content_type)
    can_create_test.save()
    can_see_test = Permission.objects.create(codename='can_see_test',
                                             name='Can See Test',
                                             content_type=content_type)
    can_see_test.save()
    can_pass_test = Permission.objects.create(codename='can_pass_test',
                                              name='Can Pass Test',
                                              content_type=content_type)
    can_pass_test.save()
    can_see_stats = Permission.objects.create(codename='can_see_stats',
                                              name='Can See Stats',
                                              content_type=content_type)
    can_see_stats.save()
    teacher = Group.objects.create(name='Teacher')
    teacher.permissions.add(can_create_test, can_see_test, can_pass_test,
                            can_see_stats)
    teacher.save()
    student = Group.objects.create(name='Student')
    student.permissions.add(can_pass_test)
    student.save()
    group1 = Group.objects.create(name='esilv_IF1')
    group1.save()
    group2 = Group.objects.create(name='esilv_IF2')
    group2.save()


def register_user(c):
    response = c.post('/tests/register/',
                      {'last_name': 'L', 'first_name': 'Client',
                       'email': 'client@live.fr', 'username': 'client1',
                       'password': '123', 'function': 'Teacher',
                       'group1': 'esilv_IF1', 'group2': 'None'})


def login_user(c):
    response = c.post('/tests/login/',
                      {'username': 'client1', 'password': '123'})


def launch_a_test(c, id):
    response = c.post('/tests/manage/launch/mcqdyn/' + id + '/',
                      {'activated_for': 'esilv_IF1', 'time': '5:30'})
    test = DynMCQInfo.objects.get(id_test=id)
    test.release_time = datetime.datetime.today()
    test.save()


def setup_marks():
    marks_list = [2, 4, 1, 6, 8, 7, 6, 6, 0, 4, 5]
    return marks_list


def setup_test():
    # Création du test
    test1 = DynMCQInfo(id_test="1", title="Test 1", questions="a[1,2,3]b")
    test2 = DynMCQInfo(id_test="2", title="Test 2", questions="a[1,2,3]b[1,2]")

    mcq1 = DynMCQquestion(q_num=1, q_text="Q1", nb_ans="2")
    r11 = DynMCQanswer(q_num=1, ans_num=1, ans_text="r11", right_ans=1)
    r12 = DynMCQanswer(q_num=1, ans_num=2, ans_text="r12", right_ans=0)

    mcq2 = DynMCQquestion(q_num=2, q_text="Q2", nb_ans="3")
    r21 = DynMCQanswer(q_num=2, ans_num=1, ans_text="r21", right_ans=0)
    r22 = DynMCQanswer(q_num=2, ans_num=2, ans_text="r22", right_ans=0)
    r23 = DynMCQanswer(q_num=2, ans_num=3, ans_text="r23", right_ans=1)

    mcq3 = DynMCQquestion(q_num=3, q_text="Q3", nb_ans="2")
    r31 = DynMCQanswer(q_num=3, ans_num=1, ans_text="r31", right_ans=0)
    r32 = DynMCQanswer(q_num=3, ans_num=2, ans_text="r32", right_ans=1)

    nq1 = Dynquestion(q_num=1, q_text="QN1", r_text="question1")
    nq2 = Dynquestion(q_num=2, q_text="QN2", r_text="question2")

    # Création des réponses
    p_test1 = PassDynMCQTestInfo(id_test="1", id_student="1", attempt=1)
    p_test11 = PassDynMCQTest(id_test="1", id_student="1", attempt=1,
                              q_num="1", r_ans="1")  # Bonne réponse
    p_test12 = PassDynMCQTest(id_test="1", id_student="1", attempt=1,
                              q_num="2", r_ans="2")  # Mauvaise réponse
    p_test13 = PassDynMCQTest(id_test="1", id_student="1", attempt=1,
                              q_num="3", r_ans="1")  # Mauvaise réponse

    p_test2 = PassDynMCQTestInfo(id_test="1", id_student="2", attempt=1)
    p_test21 = PassDynMCQTest(id_test="1", id_student="2", attempt=1,
                              q_num="1", r_ans="1")  # Bonne réponse
    p_test22 = PassDynMCQTest(id_test="1", id_student="2", attempt=1,
                              q_num="2", r_ans="3")  # Bonne réponse
    p_test23 = PassDynMCQTest(id_test="1", id_student="2", attempt=1,
                              q_num="3", r_ans="2")  # Bonne réponse

    p_test3 = PassDynMCQTestInfo(id_test="1", id_student="3", attempt=1)
    p_test31 = PassDynMCQTest(id_test="1", id_student="3", attempt=1,
                              q_num="1", r_ans="1")  # Bonne réponse
    p_test32 = PassDynMCQTest(id_test="1", id_student="3", attempt=1,
                              q_num="2", r_ans="3")  # Bonne réponse
    p_test33 = PassDynMCQTest(id_test="1", id_student="3", attempt=1,
                              q_num="3", r_ans="1")  # Mauvaise réponse

    # Saving

    test1.save()
    test2.save()
    mcq1.save()
    r11.save()
    r12.save()
    mcq2.save()
    r21.save()
    r22.save()
    r23.save()
    mcq3.save()
    r31.save()
    r32.save()
    nq1.save()
    nq2.save()
    p_test1.save()
    p_test11.save()
    p_test12.save()
    p_test13.save()
    p_test2.save()
    p_test21.save()
    p_test22.save()
    p_test23.save()
    p_test3.save()
    p_test31.save()
    p_test32.save()
    p_test33.save()


class DumbModelTests(TestCase):

    def test_register(self):
        setup_group_permissions()
        c = Client()
        register_user(c)
        user = User.objects.get(username='client1')
        self.assertEqual(user.email, 'client@live.fr')

    def test_mean(self):
        marks_list = setup_marks()
        moyenne = Moyenne(marks_list)
        self.assertEqual(moyenne, "4.45")

    def test_worst_mark(self):
        marks_list = setup_marks()
        note_plus_basse = Note_plus_basse(marks_list)
        self.assertEqual(note_plus_basse, 0)

    def test_best_mark(self):
        marks_list = setup_marks()
        note_plus_haute = Note_plus_haute(marks_list)
        self.assertEqual(note_plus_haute, 8)

    def test_Q1(self):
        marks_list = setup_marks()
        q1 = Q1(marks_list)
        self.assertEqual(q1, 2)

    def test_Q3(self):
        marks_list = setup_marks()
        q3 = Q3(marks_list)
        self.assertEqual(q3, 6)

    def test_Mediane(self):
        marks_list = setup_marks()
        median = Mediane(marks_list)
        self.assertEqual(median, 5)

    def test_Frequences(self):
        statistique_notes = [1, 1, 1, 0, 2, 1, 3, 1, 1]
        total_freq = Frequences(statistique_notes, setup_marks())

        freq = ["9.09", "9.09", "9.09", "0.00", "18.18", "9.09", "27.27",
                "9.09", "9.09"]
        cum_freq = ["9.09", "18.18", "27.27", "27.27", "45.45", "54.55",
                    "81.82", "90.91", "100.00"]
        test_freq = []
        i = 0
        while i < len(freq):
            test_freq.append((freq[i], cum_freq[i]))
            i += 1
        self.assertEqual(total_freq, test_freq)

    def test_Statistique_question(self):
        setup_test()
        the_dyn_mcq_test_info = get_object_or_404(DynMCQInfo, id_test="1")

        stats_question = Statistique_question(the_dyn_mcq_test_info)
        test_stats_question = [3, 2, 1]

        self.assertEqual(stats_question, test_stats_question)

    def test_tests_list_teacher_view(self):
        setup_group_permissions()
        setup_test()
        c = Client()
        register_user(c)
        login_user(c)
        dyn_mcq_test_info = get_object_or_404(DynMCQInfo, id_test="1")
        response = c.get(reverse('tests:List tests teacher'))
        test = response.context['testlist_dynmcqtestinfo_all']
        self.assertEqual(test[0], dyn_mcq_test_info)

    def test_pass_testslist_teacher_view(self):
        setup_group_permissions()
        c = Client()
        register_user(c)
        login_user(c)
        setup_test()
        pass_dyn_mcq_test_info = PassDynMCQTestInfo.objects.all()
        response = c.get(reverse('tests:List pass tests teacher'))
        test = response.context['pass_dynMCQtest_all']
        test_list = []
        pass_dyn_mcq_test_info_list = []
        i = 0
        while i < len(test):
            test_list.append(test[i])
            pass_dyn_mcq_test_info_list.append(pass_dyn_mcq_test_info[i])
            i += 1
        self.assertEqual(test_list, pass_dyn_mcq_test_info_list)

    def test_test_create_view(self):
        setup_group_permissions()
        setup_test()
        c = Client()
        register_user(c)
        login_user(c)
        dyn_mcq_test_info = get_object_or_404(DynMCQInfo, id_test="1")
        response = c.get(reverse('tests:Create test'))
        test = response.context['testlist_dynmcqtestinfo_all']
        self.assertEqual(test[0], dyn_mcq_test_info)

    def test_DynMCQTest_menu_view(self):
        setup_group_permissions()
        setup_test()
        c = Client()
        register_user(c)
        login_user(c)
        response = c.post('/tests/manage/create/dynmcqtestmenu/',
                          {'id_test': '3', 'title': 'Test3'})
        test = DynMCQInfo.objects.get(id_test='3')
        self.assertEqual(test.title, "Test3")

    def test_Manage_questions_view(self):
        setup_group_permissions()
        setup_test()
        c = Client()
        register_user(c)
        login_user(c)
        response = c.get(reverse('tests:Manage Questions'))
        mcq_questions = response.context['DynMCQquestions']
        dyn_questions = response.context['Dynquestions']
        dyn_mcq_questions_all = DynMCQquestion.objects.all()
        dyn_questions_all = Dynquestion.objects.all()
        mcq_questions_list = []
        dyn_questions_list = []
        dyn_mcq_questions_all_list = []
        dyn_questions_all_list = []
        i = 0
        for i in range(len(dyn_mcq_questions_all)):
            mcq_questions_list.append(mcq_questions[i])
            dyn_mcq_questions_all_list.append(dyn_mcq_questions_all[i])
        for i in range(len(dyn_questions_all)):
            dyn_questions_list.append(dyn_questions[i])
            dyn_questions_all_list.append(dyn_questions_all[i])

        self.assertEqual([mcq_questions_list, dyn_questions_list],
                         [dyn_mcq_questions_all_list, dyn_questions_all_list])

    def test_get_questions(self):
        questions = get_questions("a[1,6,5]b[4,8]")
        questions2 = get_questions("ab[4,8,78]")
        questions3 = get_questions("a[1,2,7,8]b")
        self.assertEqual([questions, questions2, questions3],
                         [[['1', '6', '5'], ['4', '8']], [[], ['4', '8', '78']],
                          [['1', '2', '7', '8'], []]])

    def test_check_answers(self):
        check_ans1 = check_answer("[1],[2]", [2, 1])
        check_ans2 = check_answer("[1]", [2, 1])
        self.assertEqual([check_ans1, check_ans2], [True, False])

    def test_get_time(self):
        time = get_time("5:30")
        self.assertEqual(time, '5.5')

    def test_get_date(self):
        time = get_date("2009-01-06 15:08:24.789150")
        self.assertEqual(time, [15, 8, 24])

    def test_add_time(self):
        time1 = add_time([15, 56, 30], "10:30")
        time2 = add_time([23, 57, 30], "5:20")
        self.assertEqual([time1, time2], [[16, 7, 0], [0, 2, 50]])

    def test_compare_date(self):
        delta_time1 = compare_date([15, 56, 30], [16, 7, 0])
        delta_time2 = compare_date([23, 59, 0], [23, 57, 30])
        self.assertEqual([delta_time1, delta_time2], [10.5, -1.5])

    def test_DynMCQquestion_select_menu_view(self):
        setup_group_permissions()
        setup_test()
        c = Client()
        register_user(c)
        login_user(c)
        test = DynMCQInfo.objects.create(id_test="3", title="Premier Test")
        response = c.post('/tests/manage/create/dynmcqtestselectqmenu/3/',
                          {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '0',
                           'form-MAX_NUM_FORMS': '',
                           'form-0-questions': [1, 2, 3],
                           'form-1-questions': [1, 2]})
        response = c.get(reverse('tests:SelectMenu DynMCQquestion',
                                 kwargs={'input_id_test': '3'}))
        mcq_questions = response.context['DynMCQquestionTestList']
        dyn_questions = response.context['DynquestionTestList']
        dyn_mcq_questions_all = DynMCQquestion.objects.all()
        dyn_questions_all = Dynquestion.objects.all()
        mcq_questions_list = []
        dyn_questions_list = []
        dyn_mcq_questions_all_list = []
        dyn_questions_all_list = []
        i = 0
        for i in range(len(dyn_mcq_questions_all)):
            mcq_questions_list.append(mcq_questions[i])
            dyn_mcq_questions_all_list.append(dyn_mcq_questions_all[i])
        for i in range(len(dyn_questions_all)):
            dyn_questions_list.append(dyn_questions[i])
            dyn_questions_all_list.append(dyn_questions_all[i])

        self.assertEqual([mcq_questions_list, dyn_questions_list],
                         [dyn_mcq_questions_all_list, dyn_questions_all_list])

    def test_Question_reallocation_view(self):
        setup_group_permissions()
        setup_test()
        c = Client()
        register_user(c)
        login_user(c)
        test = DynMCQInfo.objects.create(id_test="3", title="Premier Test",
                                         questions="a[1,2,3]b[1,2]")
        response = c.post('/tests/manage/create/question_reallocation/3/',
                          {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '0',
                           'form-MAX_NUM_FORMS': '', 'form-0-questions': [1, 2],
                           'form-1-questions': [1, 2]})
        test = DynMCQInfo.objects.get(id_test="3")
        response = c.get(reverse('tests:Question_reallocation',
                                 kwargs={'input_id_test': '3'}))
        mcq_questions = response.context['DynMCQquestionTestList']
        dyn_questions = response.context['DynquestionTestList']
        dyn_mcq_questions1 = DynMCQquestion.objects.get(q_num=1)
        dyn_mcq_questions2 = DynMCQquestion.objects.get(q_num=2)
        dyn_questions_all = Dynquestion.objects.all()
        mcq_questions_list = []
        dyn_questions_list = []
        dyn_mc_questions_all_list = [dyn_mcq_questions1, dyn_mcq_questions2]
        dyn_questions_all_list = []
        for i in range(len(mcq_questions)):
            mcq_questions_list.append(mcq_questions[i])
        for i in range(len(dyn_questions_all)):
            dyn_questions_list.append(dyn_questions[i])
            dyn_questions_all_list.append(dyn_questions_all[i])

        self.assertEqual([mcq_questions_list, dyn_questions_list],
                         [dyn_mc_questions_all_list, dyn_questions_all_list])

    def test_DynMCQquestion_create_view(self):
        setup_group_permissions()
        setup_test()
        c = Client()
        register_user(c)
        login_user(c)
        question = DynMCQquestion.objects.create(q_num="4")
        response = c.post('/tests/manage/create/dynmcqtestmcqquestion/4/',
                          {'q_text': 'Question 4', 'nb_ans': '2',
                           'activated': 1})
        question = DynMCQquestion.objects.get(q_num="4")
        self.assertEqual(question.q_text, 'Question 4')

    def test_Dynquestion_create_view(self):
        setup_group_permissions()
        setup_test()
        c = Client()
        register_user(c)
        login_user(c)
        question = Dynquestion.objects.create(q_num="3")
        response = c.post('/tests/manage/create/dynmcqtestquestion/3/',
                          {'q_text': 'Question 3', 'r_text': 'q3',
                           'activated': 1})
        question = Dynquestion.objects.get(q_num="3")
        self.assertEqual([question.q_text, question.r_text],
                         ['Question 3', 'q3'])

    def test_Add_difficulty_view(self):
        setup_group_permissions()
        setup_test()
        c = Client()
        register_user(c)
        login_user(c)

        response = c.post('/tests/manage/create/add_difficulty/1/',
                          {'form-TOTAL_FORMS': '5', 'form-INITIAL_FORMS': '0',
                           'form-MAX_NUM_FORMS': '', 'form-0-difficulty': '4',
                           'form-1-difficulty': '2', 'form-2-difficulty': '0',
                           'form-3-difficulty': '1', 'form-4-difficulty': '0'})
        question = DynMCQquestion.objects.get(q_num="1")

        self.assertEqual(question.difficulty, "['4']['2']['0']['1']['0']")

    def test_Add_difficulty_question_view(self):
        setup_group_permissions()
        setup_test()
        c = Client()
        register_user(c)
        login_user(c)

        response = c.post('/tests/manage/create/add_difficulty_question/1/',
                          {'form-TOTAL_FORMS': '5', 'form-INITIAL_FORMS': '0',
                           'form-MAX_NUM_FORMS': '', 'form-0-difficulty': '4',
                           'form-1-difficulty': '2', 'form-2-difficulty': '0',
                           'form-3-difficulty': '1', 'form-4-difficulty': '0'})
        question = Dynquestion.objects.get(q_num="1")

        self.assertEqual(question.difficulty, "['4']['2']['0']['1']['0']")

    def test_DynMCQanswer_create_view(self):
        setup_group_permissions()
        setup_test()
        c = Client()
        register_user(c)
        login_user(c)
        question = DynMCQquestion.objects.create(q_num="4", q_text='Question 4',
                                                 nb_ans='2', activated=1)
        response = c.post('/tests/manage/create/dynmcqtestanswer/4/',
                          {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '0',
                           'form-MAX_NUM_FORMS': '',
                           'form-0-ans_text': 'Answer 1', 'form-0-right_ans': 0,
                           'form-1-ans_text': 'Answer 2',
                           'form-1-right_ans': 1})
        answers = DynMCQanswer.objects.filter(q_num="4")
        self.assertEqual([answers[0].ans_text, answers[1].ans_text],
                         ['Answer 1', 'Answer 2'])

    def test_launch_specific_dynmcq_view(self):
        setup_group_permissions()
        setup_test()
        c = Client()
        register_user(c)
        login_user(c)
        launch_a_test(c, '2')
        test = DynMCQInfo.objects.get(id_test='2')
        self.assertEqual(test.time, "5:30")

    def test_DynMCQtest_pass_view(self):
        setup_group_permissions()
        setup_test()
        c = Client()
        register_user(c)
        login_user(c)
        launch_a_test(c, '2')
        pass_test = PassDynMCQTestInfo(id_test="2", id_student="client1",
                                       attempt=1, mark=0)
        pass_test.save()
        response = c.post('/tests/pass/dynmcqtest/2/client1/1',
                          {'form-TOTAL_FORMS': '3', 'form-INITIAL_FORMS': '0',
                           'form-MAX_NUM_FORMS': '', 'form-0-r_ans': '1',
                           'form-1-r_ans': '3', 'form-2-r_ans': '2',
                           'form-0-r_answer': 'question1',
                           'form-1-r_answer': 'question3'})
        pass_test = PassDynMCQTestInfo.objects.get(id_test="2",
                                                   id_student="client1",
                                                   attempt=1)
        self.assertEqual(pass_test.mark, 4)
