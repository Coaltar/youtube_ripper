from django.urls import path

from . import views



app_name = 'ytb'

urlpatterns = [
    path('', views.index, name="index").
    path('channels/<int:pk>/', views.ChannelView.as_view(), name='channels'),
    path('video/<int:pk>/', views.VideoView.as_view(), name="video")
    

    # path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]