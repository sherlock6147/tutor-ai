from learners.models import Learner,Moderator

def prepare_context(request):
    context = {}
    context['is_learner'] = False
    context['learner'] = None
    context['is_moderator'] = False
    context['moderator'] = None
    if request.user.is_authenticated:
        learner = Learner.objects.filter(user = request.user).first()
        if learner:
            context['is_learner'] = True
            context['learner'] = learner
        moderator = Moderator.objects.filter(user = request.user).first()
        if moderator:
            context['is_moderator'] = True
            context['moderator'] = moderator
    print("starting context\n",context)
    return context