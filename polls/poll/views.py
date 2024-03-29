from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'poll/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'poll/detail.html'


class ResultView(generic.DetailView):
    model = Question
    template_name = 'poll/results.html'
#
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'poll/detail.html', {'question': question})
#
#
# def result(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'poll/result.html', {'question': question})
#
#
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_data')[:5]
#     template =loader.get_template('poll/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#
#     output = ','.join([q.question_text for q in latest_question_list])
#     return render(request, 'poll/index.html', context)
#
#
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))