from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from learners.models import *
from django.contrib import messages
from base.utils import prepare_context

def getProfileImage(request):
    user = request.user


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
    return render(request,"learners/profile.html",context)