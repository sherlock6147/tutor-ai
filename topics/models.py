from django.db import models

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="")
    order = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name
    
    @property
    def has_subtopics(self) -> bool:
        return len(SubTopic.objects.filter(topic=self))!=0

    @property
    def subtopics(self) -> list:
        return SubTopic.objects.filter(topic=self)

class SubTopic(models.Model):
    name = models.CharField(max_length=200)
    order =  models.IntegerField(default=0)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.topic.name + "| " + self.name

