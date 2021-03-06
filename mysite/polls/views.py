from polls.models import Question, Choice
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        """
        Return the last five published questions(not including
        those set to be published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """ Excludes any questions that arent published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
    
def add(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    every = p.choice_set.all()
    
    try :
        selected_choice = request.POST['choice']
    except:
        return render(request, 'polls/detail.html', {
                    'question': p,
                    'error_message': "Please enter a viable answer!",
                     })
    else:
        if every.filter(choice_text=selected_choice).exists():
            return render(request, 'polls/detail.html', {
                    'question': p,
                    'error_message': "That answer choice is already there!",
                     })
        if selected_choice == '':
            return render(request, 'polls/detail.html', {
                'question': p,
                'error_message': "You didn't fill in an answer!",
                 })
        else:
            p.choice_set.create(choice_text=request.POST['choice'], votes=1)
            p.save()
            return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def addq(request):
    p = Question.objects.all().order_by('-pub_date')
    
    try :
        selected_question = request.POST['question']
    except:
        return render(request, 'polls/index.html', {
                    'latest_question_list':p,
                    'error_message': "Please submit a question",
                     })
    else:
        if p.filter(question_text=selected_question).exists():
            return render(request, 'polls/index.html', {
                    'question':p,
                    'error_message': "That question is already there!",
                     })
        if selected_question == '':
            return render(request, 'polls/index.html', {
                'latest_question_list':p,
                'error_message': "You didn't fill in a question!",
                 })
        else:
            q= Question(question_text=request.POST['question'], pub_date=timezone.now())
            q.save()
            return render(request, 'polls/index.html', {
                    'latest_question_list':p,
                    'error_message': "Thanks for submitting a question!",
                     })
        