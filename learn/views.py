from django.shortcuts import render,redirect,get_object_or_404
from base.utils import prepare_context
from topics.models import *
from learn.models import *
from django.views.decorators.http import require_http_methods
from learn.prompts import *
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

PASS_PERCENTAGE = 75

# Create your views here.
@login_required
def learn_subtopic(request,subtopic_id):
    context = prepare_context(request)
    subtopic = get_object_or_404(SubTopic,id=subtopic_id)
    # context['todos'] = Todo.objects.all()
    start_history = Chat.objects.filter(subtopic=subtopic,learner=context['learner']).order_by('created_on')
    print("Length: ",len(start_history))
    if len(start_history) == 0:
        # The learner has started learning the topic for the first time!
        # create intro_to_topic_chat message
        createStartingInformationPrompt(subtopic,context)
    context['history'] = Chat.objects.filter(subtopic=subtopic,learner=context['learner']).order_by('created_on')
    context['subtopic'] = subtopic
    print(context)
    return render(request,'learn/learn.html',context)

@require_http_methods(['POST'])
def chat_with_ai(request,subtopic_id):
    context = prepare_context(request)
    subtopic = get_object_or_404(SubTopic,id=subtopic_id)
    context['subtopic'] = subtopic
    chat = None
    prompt_input = str(request.POST.get('prompt'))
    if prompt_input.startswith('/start'):
        current_information = LearningInformation.objects.filter(chat__learner=context['learner'],chat__subtopic=subtopic).order_by('-created_on').first()
        print(current_information)
        createLearnerPrompt(subtopic,context,input=prompt_input)
        available_questions = Question.objects.filter(information = current_information,is_available=True)
        print("available questions:\n",available_questions)
        if len(available_questions) == 0:
            # generate 5 more questions and choose one
            createQuestions(subtopic,context,info=current_information)
            current_question = Question.objects.filter(information = current_information).first()
        else:
            current_question = available_questions.first()
        current_question.is_available = False
        current_question.used_on = timezone.now()
        current_question.save()
        createQuestionPrompt(subtopic,context,question=current_question.content)

    elif prompt_input.startswith('/answer'):
        prompt_reponse = prompt_input[len(str("/answer")):]
        current_information = LearningInformation.objects.filter(chat__learner=context['learner'],chat__subtopic=subtopic).order_by('-created_on').first()
        print(current_information)
        createLearnerPrompt(subtopic,context,input=prompt_input)
        available_questions = Question.objects.filter(information = current_information).order_by('-used_on')
        # print("available questions:\n",available_questions)
        current_question = available_questions.first()
        current_question.is_answered = True
        current_question.answer_response = prompt_reponse
        if is_answer_correct_ques(subtopic,context,current_question):
            current_question.is_answer_correct = True
        else:
            current_question.is_answer_correct = False
        current_question.save()
    elif prompt_input.startswith('/evaluate'):
        # prompt_reponse = prompt_input[len(str("/evaluate")):]
        total_questions_answered = 0
        total_questions_answered_correctly = 0
        informations = LearningInformation.objects.filter(chat__learner=context['learner'],chat__subtopic=subtopic).order_by('-created_on')
        createLearnerPrompt(subtopic,context,input=prompt_input)
        for info in informations:
            answered_questions = Question.objects.filter(information = info,is_answered = True).order_by('-used_on')
            total_questions_answered += len(answered_questions)
            correct_questions = Question.objects.filter(information = info,is_answered = True,is_answer_correct=True).order_by('-used_on')
            total_questions_answered_correctly += len(correct_questions)
        percentage = (total_questions_answered_correctly/total_questions_answered)*100
        if percentage >= PASS_PERCENTAGE:
            # Your have passed
            createHelpPrompt(subtopic,context,message="You have passed this subtopic, with a percentage of "+str(percentage)+". You can continue learning or choose to move to next subtopic")
            all_topics = Topic.objects.all().order_by('order','-name')
            next_subtopic = None
            flag = False
            for topic in all_topics:
                for st in topic.subtopics:
                    if flag:
                        next_subtopic = st
                    flag = st == subtopic
            messages.success(request,"You have passed this subtopic, with a percentage of "+str(percentage)+". You can continue learning or choose to move to next subtopic")
            if next_subtopic == None:
                context['redirect_to'] = '/topics/'
            else:
                context['redirect_to'] = '/learn/'+str(next_subtopic.id)+'/'
        else:
            createHelpPrompt(subtopic,context,message="You have not passed this subtopic, with a percentage of "+str(percentage)+". You need "+str(PASS_PERCENTAGE) + " to pass to next subtopic.")
    context['history'] = Chat.objects.filter(subtopic=subtopic,learner=context['learner']).order_by('created_on')
    print(render(request,'learn/chat.html',context))
    return render(request,'learn/chat.html',context)

def show_help(request):
    context = prepare_context(request)
    return render(request,"learn/help.html",context)