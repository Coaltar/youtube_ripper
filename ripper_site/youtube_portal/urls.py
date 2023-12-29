from django.urls import path

from . import views



app_name = 'youtube_portal'

urlpatterns = [
    path('', views.index, name="index"),
    path('channels/', views.ChannelView.as_view(), name='channels'),
    path('videos/', views.VideoView.as_view(), name="video"),
    path('ingest/', views.ingest, name="ingest")
    
    

    # path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]