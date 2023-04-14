from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from base.utils import prepare_context
from django.contrib import messages
from topics.models import *

# Create your views here.
@login_required
def all_topics(request):
    context = prepare_context(request)
    context['all_topics'] = Topic.objects.all().order_by('order','-name')
    for t in context['all_topics']:
        print(t.has_subtopics)
        print(t.subtopics)
    return render(request,'topics/all_topics.html',context)

@login_required
def add_topic(request):
    context = prepare_context(request)
    if not context['is_moderator']:
        messages.info(request,"This url is restricted, please login as moderator")
        return redirect('/learners/profile')
    if request.method == 'POST':
        if 'save-topic' in request.POST:
            topic_name = request.POST.get('topic_name')
            topic_desc = request.POST.get('topic_desc')
            topic = Topic()
            topic.name = topic_name
            topic.description = topic_desc
            topic.save()
            messages.success(request,topic_name + " successfully added.")
            return redirect('/topics/')
    return render(request,'topics/add_topic.html',context)

@login_required
def edit_topic(request,topic_id):
    context = prepare_context(request)
    if not context['is_moderator']:
        messages.info(request,"This url is restricted, please login as moderator")
        return redirect('/learners/profile')
    topic = get_object_or_404(Topic,id=topic_id)
    context['topic'] = topic
    if request.method == 'POST':
        if 'save-topic' in request.POST:
            topic_name = request.POST.get('topic_name')
            topic_desc = request.POST.get('topic_desc')
            topic.name = topic_name
            topic.description = topic_desc
            topic.save()
            messages.success(request,topic_name + " successfully updated.")
            return redirect('/topics/')
    return render(request,'topics/edit_topic.html',context)

@login_required
def delete_topic(request,topic_id):
    context = prepare_context(request)
    if not context['is_moderator']:
        messages.info(request,"This url is restricted, please login as moderator")
        return redirect('/learners/profile')
    topic = get_object_or_404(Topic,id=topic_id)
    context['topic'] = topic
    topic.delete()
    return redirect('/topics/')

@login_required
def add_subtopic(request,topic_id):
    context = prepare_context(request)
    if not context['is_moderator']:
        messages.info(request,"This url is restricted, please login as moderator")
        return redirect('/learners/profile')
    topic = get_object_or_404(Topic,id=topic_id)
    if not topic:
        messages.error(request,"Topic not found!")
        return redirect('/topics/')
    if request.method == 'POST':
        if 'save-subtopic' in request.POST:
            subtopic_name = request.POST.get('subtopic_name')
            subtopic = SubTopic()
            subtopic.name = subtopic_name
            subtopic.topic = topic
            subtopic.save()
            messages.success(request,str(subtopic) + " successfully added.")
            return redirect('/topics/')
    return render(request,'topics/add_subtopic.html',context)

@login_required
def edit_subtopic(request,subtopic_id):
    context = prepare_context(request)
    if not context['is_moderator']:
        messages.info(request,"This url is restricted, please login as moderator")
        return redirect('/learners/profile')
    subtopic = get_object_or_404(SubTopic,id=subtopic_id)
    context['subtopic'] = subtopic
    if request.method == 'POST':
        if 'save-subtopic' in request.POST:
            subtopic_name = request.POST.get('subtopic_name')
            subtopic.name = subtopic_name
            subtopic.save()
            messages.success(request,str(subtopic) + " successfully updated.")
            return redirect('/topics/')
    return render(request,'topics/edit_subtopic.html',context)

@login_required
def delete_subtopic(request,subtopic_id):
    context = prepare_context(request)
    if not context['is_moderator']:
        messages.info(request,"This url is restricted, please login as moderator")
        return redirect('/learners/profile')
    subtopic = get_object_or_404(SubTopic,id=subtopic_id)
    subtopic.delete()
    return redirect('/topics/')
