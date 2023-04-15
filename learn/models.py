from django.db import models
from learners.models import Learner
from topics.models import SubTopic
from django.utils import timezone

# Create your models here.
class Chat(models.Model):
    message = models.TextField()
    learner = models.ForeignKey(Learner,on_delete=models.CASCADE)
    msg_type = models.CharField(max_length=100,default="")
    from_ai = models.BooleanField(default=True)
    subtopic = models.ForeignKey(SubTopic,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "Learner: "+self.learner.user.first_name + " " + self.learner.user.last_name + " From AI " + str(self.from_ai) +" Message Type: "+ self.msg_type + " Message content: "+ str(self.message)[:30] + "..."

class LearningInformation(models.Model):
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE)
    information = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "Information for chat-id: "+str(self.chat.id) + " Information content: "+str(self.information)[:20]

class Question(models.Model):
    information = models.ForeignKey(LearningInformation,on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    is_answered = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default="")
    is_answer_correct = models.BooleanField(default=False)
    answer_response = models.TextField(default="",blank=True,null=True)
    used_on = models.DateTimeField(blank=True,null=True)
    def __str__(self) -> str:
        return "Question for info-id: "+str(self.information.id) +" content: " + str(self.content)[:30] + str(self.used_on)
