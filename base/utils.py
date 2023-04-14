from learners.models import Learner,Moderator
# ACCESS_LEVELS = ADMIN-5, MODERATOR-4, LEARNER-3, NEW_USER-2, ANONYMOUS-0

def get_access_level(request):
    if request.user.is_authenticated:
        pass
    else:
        return 0

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

def allow_access(reuest, **kwargs):
    access_levels = kwargs.get('levels',['NEW_USER'])
    context = {}

    return context