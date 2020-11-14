from django.shortcuts import render
from django.http import HttpResponse
from .models import Categories, Questions, Answers, Parameters, Mcqs

def home_view(request, *args, **kwargs):    
    return render(request, 'home.html')

def categories_view(request):
    """Function to display all the categories"""
    categories_all = Categories.objects.all()
    context = {
        'categories_all': categories_all,
        }
    return render(request, 'categories.html', context)

def questions_view(request):
    """Function to display all the questions"""
    questions_all = Questions.objects.all()
    context = {
        'questions_all': questions_all,
    }
    return render(request, 'questions.html', context)

def answers_view(request):
    """Function to display all the answers"""
    answers_all = Answers.objects.all()
    context = {
        'answers_all': answers_all,
    }
    return render(request, 'answers.html', context)


def parameters_view(request):
    """Function to display all the parameters"""
    parameters_all = Parameters.objects.all()
    context = {
        'parameters_all': parameters_all,
    }
    return render(request, 'parameters.html', context)

def mcqs_view(request):
    """Function to display all the mcqs"""
    mcqs_all = Mcqs.objects.all()
    context = {
        'mcqs_all': mcqs_all,
    }
    return render(request, 'mcqs.html', context)

def models_view(request):
    """Function to display all the tables"""
    tables_all = {'ok':1, 'ok2':2}
    context = {
        'tables_all': tables_all,
    }
    return render(request, 'tables.html', context)
