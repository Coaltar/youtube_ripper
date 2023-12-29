from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from django.views import generic
from django.utils import timezone
from django.shortcuts import render, get_object_or_404


from .models import Channel, Video
from .selenium_scripts import ingest_channel

from .tasks import celery_ingest


def index(request):
    # template_name = "youtube_portal/index.html"

    # return HttpResponse("should display some links to the sample pages")
    return render(request, "youtube_portal/index.html",{
    })


class ChannelView(generic.ListView):
    template_name = 'youtube_portal/channels.html'
    context_object_name = 'channel_list'
    
    def get_queryset(self):
        return Channel.objects.all()
        # return Channel.objects.filter(date_searched__lte=timezone.now()).order_by("-date_searched")[:10]




# class channelDetail(generic.DetailView):

class VideoView(generic.ListView):
    template_name = 'youtube_portal/videos.html'
    context_object_name = 'video_list'

    def get_queryset(self) -> QuerySet[Any]:
        return Video.objects.all()
    

def ingest(request):
    channel_name = request.POST["channel_name"]
    print(channel_name)
    celery_ingest.delay(channel_name)

    return HttpResponseRedirect(reverse('youtube_portal:index'))
    
 
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))