from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render

from django.views import generic
from django.utils import timezone
from django.shortcuts import render, get_object_or_404


from .models import Channel, Video
from .selenium_scripts import ingest_channel



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