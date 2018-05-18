"""
Definition of views.
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http.response import HttpResponse, Http404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question,Choice,User
from django.template import loader
from django.core.urlresolvers import reverse
from app.forms import QuestionForm, ChoiceForm,UserForm
from django.shortcuts import redirect
import json


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def verPreguntas(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    template = loader.get_template('app/verPreguntas.html')    
    questions = Question.objects.all()
    temas = questions.values('tema').distinct()
    context = {
                'title':'Ver preguntas y respuestas',
                'message':'Listado de las preguntas y sus respectivas respuestas',
                'latest_question_list': latest_question_list,
                'temas':temas,
              }
    return render(request, 'app/verPreguntas.html', context)

def verPreguntasTema(request):
    selected = request.POST['dropList']
    listaObjectos = Question.objects.filter(tema=request.POST['dropList'])

    context = {
            'title':'Ver preguntas y respuestas por tema',
            'message':'Listado de las preguntas y sus respectivas respuestas con el tema "' + selected + '"',
            'listaObjectos': listaObjectos,
            }
    return render(request, 'app/verPreguntasTema.html', context)


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    template = loader.get_template('polls/index.html')
    questions = Question.objects.all()
    temas = questions.values('tema').distinct()
    context = {
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': latest_question_list,
                'temas':temas,
              }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
     question = get_object_or_404(Question, pk=question_id)
     return render(request, 'polls/detail.html', {'title':'Respuestas asociadas a la pregunta:','question': question})

def results(request, question_id, selected_choice_id):
    question = get_object_or_404(Question, pk=question_id)
    choice = get_object_or_404(Choice, pk=selected_choice_id)
    return render(request, 'polls/results.html', {'title':'Resultados de la pregunta:','question': question,'choice':choice})

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form. Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        return HttpResponseRedirect(reverse('results', args=(p.id,selected_choice.id)))

def question_new(request):
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.pub_date=datetime.now()
                question.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = QuestionForm()
        return render(request, 'polls/question_new.html', {'form': form})

def choice_add(request, question_id):
        question = Question.objects.get(id = question_id)
        cantidadChoice = Choice.objects.filter(question = question_id).count()
        message = ''
        hayTrue = 0
        if request.method == "POST":
            form = ChoiceForm(request.POST)
            if form.is_valid():
                if cantidadChoice < 4:
                    choiceTrue = form.cleaned_data['correct']
                    if choiceTrue is True:
                        choices = Choice.objects.filter(question = question_id)
                        hayTrue = choices.filter(correct = True).count()
                    if hayTrue == 0:
                        choice = form.save(commit = False)
                        choice.question = question
                        choice.vote = 0
                        choice.save()
                        message = 'Respuesta añadida con éxito.'
                    else: 
                        message = 'Ya hay una respuesta correcta.'
                else:
                    message = 'Máximo de respuestas alcanzadas.'
        else:
            form = ChoiceForm()
        return render(request, 'polls/choice_new.html', {'title':'Pregunta:'+ question.question_text,'message':message,'form': form})

def chart(request, question_id):
    q=Question.objects.get(id = question_id)
    qs = Choice.objects.filter(question=q)
    dates = [obj.choice_text for obj in qs]
    counts = [obj.votes for obj in qs]
    context = {
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
    }

    return render(request, 'polls/grafico.html', context)

def user_new(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = UserForm()
        return render(request, 'polls/user_new.html', {'form': form})

def users_detail(request):
    latest_user_list = User.objects.order_by('email')
    template = loader.get_template('polls/users.html')
    context = {
                'title':'Lista de usuarios',
                'latest_user_list': latest_user_list,
              }
    return render(request, 'polls/users.html', context)