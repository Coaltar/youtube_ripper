from django.http import HttpResponse
from django.shortcuts import render

from django.views import generic
from django.utils import timezone


from .models import Channel, Video



def index(request):
    return HttpResponse("should display some links to the sample pages")

def search(form):
    return HttpResponse("The search form should go here")

class ChannelView(generic.ListView):
    template_name = 'youtube_portal/channels.html'
    context_object_name = 'channels_list'

    max_display = 10
    
    def get_queryset(self):
        return Channel.objects.filter(pub_date__lte=timezone.now()).order_by("-searched")[:max_display]

class VideoView(generic.DetailView):
    model = Video
    template_name = 'youtube_portal/video.html'
    




    
