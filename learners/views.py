from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from learners.models import *
from django.contrib import messages
from base.utils import prepare_context
from topics.models import *
from learn.models import *


# Create your views here.
@login_required
def register(request):
    context = {}
    context = prepare_context(request)
    if context['learner']:
        messages.info(request,"Your account has been created already.")
        return redirect('/learners/profile')
    if request.method == 'POST':
        if 'save-btn' in request.POST:
            learner = Learner()
            learner.user = request.user
            learner.phone = request.POST.get('phone')
            learner.save()
            return redirect('/learners/profile')
    return render(request,"learners/register.html",context)

# ACCESS_LEVELS = ADMIN, MODERATOR, LEARNER, NEW_USER
@login_required
def profile(request):
    context = {}
    context = prepare_context(request)
    if not context['learner']:
        messages.info(request,"Please complete registration.")
        return redirect('/learners/register')
    subtopics = SubTopic.objects.all().order_by("-name")
    progress_list = []
    total_correct = 0
    total_answered = 0
    for subtopic in subtopics:
        progress = {}
        progress['subtopic'] = subtopic
        informations = LearningInformation.objects.filter(chat__learner=context['learner'],chat__subtopic=subtopic).order_by('-created_on')
        if len(informations)==0:
            continue
        total_questions_answered = 0
        total_questions_answered_correctly = 0
        for info in informations:
            answered_questions = Question.objects.filter(information = info,is_answered = True).order_by('-used_on')
            total_questions_answered += len(answered_questions)
            correct_questions = Question.objects.filter(information = info,is_answered = True,is_answer_correct=True).order_by('-used_on')
            total_questions_answered_correctly += len(correct_questions)
            total_answered += total_questions_answered
            total_correct += total_questions_answered_correctly
        if total_questions_answered != 0:
            progress['percentage'] = (total_questions_answered_correctly/total_questions_answered)*100
        else:
            progress['percentage'] = 0
        progress_list.append(progress)
    context['progress_list'] = progress_list
    if total_answered != 0:
        context['total_percentage'] = (total_correct / total_answered)*100
    else:
        context['total_percentage'] = 0
    print(context)
    return render(request,"learners/profile.html",context)