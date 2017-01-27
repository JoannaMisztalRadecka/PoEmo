from unidecode import unidecode
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect

from .forms import InspirationForm
from models import Poem, Inspiration
from architecture.control_component import ControlComponent

def make_poem(request):
     if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InspirationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            inspiration = form.save(commit=False)
            inspiration.save()
            cc = ControlComponent(inspiration.input_text)
            poem_text = cc.make_poem()
            poem = Poem(poem_text=unidecode(poem_text), inspiration=inspiration)
            poem.save()

            return redirect('poetry_generator:poem', poem_id=poem.pk)

     else:
        form = InspirationForm()

     return render(request, 'poetry_generator/inspiration.html', {'form': form})


def poem(request, poem_id):
    poem = get_object_or_404(Poem, pk=poem_id)
    inspiration = poem.inspiration
    poem_lines = poem.poem_text.split('\n')

    context = {
        'inspiration': inspiration,
        'poem_lines': poem_lines
    }
    return render(request, 'poetry_generator/poem.html', context)


def index(request):

    # cc = ControlComponent()
    # poem_text = cc.make_poem()
    # poem = Poem(poem_text=poem_text)
    # poem.save()
    inspiration_list = Inspiration.objects.all()
    context = {
        'inspiration_list': inspiration_list,
    }
    return render(request, 'poetry_generator/index.html', context)


def detail(request, text_id):
   text = get_object_or_404(Inspiration, pk=text_id)
   return render(request, 'poetry_generator/detail.html', {'inspiration': text})


def results(request, inspiration_id):
    response = "You're looking at the results of inspiration %s."
    return HttpResponse(response % inspiration_id)


def vote(request, inspiration_id):

    inspiration = get_object_or_404(Inspiration, pk=inspiration_id)
    try:
        selected_poem = inspiration.poem_set.get(pk=request.POST['poem'])
    except (KeyError, Poem.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'poetry_generator/detail.html', {
            'question': inspiration,
            'error_message': "You didn't select a choice.",
        })
    else:

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('poetry_generator:results', args=(inspiration.id,)))

    # return HttpResponse("You're voting on inspiration %s." % inspiration_id)

#
# def select(request, inspiration_id):
#     inspiration = get_object_or_404(Inspiration, pk=inspiration_id)
#     try:
#         selected_inspiration = inspiration.poem_set.get(pk=request.POST['poem'])
#     except (KeyError, Poem.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'poetry_generator/detail.html', {
#             'inspiration': inspiration,
#             'error_message': "You didn't select an inspiration.",
#         })
#     else:
#         cc = ControlComponent()
#         poem_text = cc.make_poem()
#         poem = Poem(poem_text=poem_text, inspiration=selected_inspiration)
#         poem.save()
#
    # return render(request, 'poetry_generator/detail.html', {'inspiration': selected_inspiration}, RequestContext(request))