from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.db import models
from qcm.models import Question, Reponse, Categories

def question(request):
    questions=Question.objects.get(id=2)
    reponses_true=questions.question_true_reponse.all()
    reponses_false=questions.question_false_reponse.all()
    return render(request,'test.html', {'list_questions':questions, 'list_reponses_true':reponses_true, 'list_reponses_false':reponses_false})


def new_question(request):
    liste_questions=Question.objects.all()
    for elem in liste_questions:
        elem_id=elem.id
        questions=liste_questions.get(id=elem_id)
        reponses_true=questions.question_true_reponse.all()
        reponses_false=questions.question_false_reponse.all()
    
    return render(request,'test.html', {'list_questions':liste_questions, 'list_reponses_true':reponses_true, 'list_reponses_false':reponses_false, 'elem_id':elem_id})

def test(request):
    return render(request, 'test.html')
