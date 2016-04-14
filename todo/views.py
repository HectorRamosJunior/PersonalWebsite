from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import UserProfile, Task
from .forms import UserForm, UserProfileForm, TaskForm
import json

# Create your views here.
def index(request):
	user_list = UserProfile.objects.all()
	context = {'user_list': user_list}
	return render(request, 'todo/index.html', context)


@login_required
def user_profile(request, username):
  if request.user.username != username:
    return HttpResponse("Not your account page. Go back to the start! <br/>" + 
                        "<a href='/todo/'>IndexPage</a>")

  user_profile = UserProfile.objects.get(user__username=username)
  error = False

  if request.method == 'POST':

    if request.POST.get("type") == "remove":
      task_list = user_profile.task_set.all()
      to_remove = request.POST.getlist("to_remove[]")
      tasks_removed = []
      response_data = {}


      for task in task_list:
        if str(task.pk) in to_remove:
          tasks_removed.append(str(task.pk))
          task.delete()

      response_data["tasks_removed"] = tasks_removed
      return HttpResponse(
          json.dumps(response_data),
          content_type="application/json"
      )

    elif request.POST.get("type") == "create":

        task_entry = request.POST.get("task_entry")

        task = Task(user=user_profile, text= task_entry)
        task.save()

        response_data = {}

        response_data["user_profile"] = user_profile.user.username
        response_data["task_pk"] = task.id 
        response_data["text"] = task.text

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

  else:
    task_form = TaskForm()
    task_list = user_profile.task_set.all() 
    context = {'user_profile': user_profile, 'task_list': task_list, 'error': error, 'task_form' : task_form}

    return render(request, 'todo/user_profile.html', context)


def register(request):
  registered = False #Placeholder, lets the page know if successful or not

  if request.method == 'POST': #They're trying to make an account

    #Pull data for both forms from the forms.py file
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileForm(data=request.POST)

    if user_form.is_valid() and profile_form.is_valid(): #Safeguard against bad input
      user = user_form.save() #save the data

      user.set_password(user.password) #hashes the password
      user.save() #save the hashed password

      profile = profile_form.save(commit=False) #Hold submitting the data for now
      profile.user = user #Set the one to one relationship up properly

      #if 'picture' in request.FILES:
        #profile.picture = request.FILES['picture']

      profile.save()

      registered = True

    else: #If the data was entered incorrectly
      print user_form.errors, profile_form.errors #Print both form errors!

  else: #If the request is a GET, post the register information forms
    user_form = UserForm()
    profile_form = UserProfileForm()

  context = {'user_form': user_form, 'profile_form': profile_form, 
            'registered': registered,}
  return render(request, 'todo/register.html', context)


def user_login(request):
  if request.method == 'POST': #Trying to login?
      username = request.POST.get('username') #Pulls the username field from the form
      password = request.POST.get('password') #POST.get returns 'none', not KeyError

      user = authenticate(username=username, password=password) #Legit login?

      if user: #if there's a account for the information provided
        if user.is_active: #Not BanHammered?
          login(request, user)
          return HttpResponseRedirect('/todo/')

      else: #Either acc or password is wrong
        error = "Account or Password provided was incorrect."
        return render(request, 'todo/login.html', {'error': error})


  else: #GET, trying to login
    return render(request, 'todo/login.html', {})


@login_required #make sure a user is logged on to use this
def user_logout(request):
  logout(request) #logs out the user

  return HttpResponseRedirect('/todo/') #Send em back to the index page


