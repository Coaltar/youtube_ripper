from django.db import models

# Create your models here.

class Channel(models.Model):
    channel_name = models.CharField(max_length=200)
    channel_url = models.CharField(max_length=200)
    date_searched = models.DateTimeField()

    class Meta:
        app_label = 'ytb'

    def __str__(self):
        return self.channel_name
    
    #channel name
    #channel url
    

class Video(models.Model):
    title =  models.CharField(max_length=200)
    url =  models.CharField(max_length=200)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    published = models.DateTimeField('date published')
    # duration = ???
    views = models.IntegerField()
    comment_count = models.IntegerField()

    class Meta:
        app_label = 'ytb'

    def __str__(self):
        return self.title
    
    #duration - time???
    #video - blob data - do later
    
