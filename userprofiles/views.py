from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import User
from .models import Position
from django.contrib.auth import logout as django_logout

import logging

log = logging.getLogger(__name__)

def home(request):
    users = User.objects.all()
    return render(request, 'home.html', {'users': users})

@login_required
def user_detail(request):
    try:
        current_user = request.user
        user = User.objects.get(username=current_user.username)
        positions = Position.objects.all()
        userPositions = []
        for position in positions:
            if(position.user == user):
               userPositions.append(position)
    except User.DoesNotExist:
        raise Http404('User not found')
    return render(request, 'user_detail.html', {'user': user, 'userPositions': userPositions})

def login(request):
    return render(request, 'login.html')

def logout(request):
    django_logout(request)
    return render(request, 'logged_out.html')

def reset_request(request):


    log.warning('Password change request made for {name}'.format(

        name = request.user.username

    ))

    return render(request, 'reset_request.html', {'user': request.user})
