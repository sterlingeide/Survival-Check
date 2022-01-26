from django.shortcuts import render, redirect
from .models import Character, Weapons
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def index(request):
    return HttpResponse("Hello, world. You're at the main index.")

def login_view(request):
    if request.method == 'POST':
        # try to log the user in
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user) # log the user in by creating a session
                    return redirect('/user/'+u)
                else:
                    print('The account has been disabled.')
                    return redirect('/login')
        else:
            print('The username and/or password is incorrect.')
            return redirect('/login')
    else: # it was a GET request so send the empty login form
        form = AuthenticationForm()
        return render(request, 'main_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/user/'+str(user))
        else:
            return HttpResponse('<h1>Try Again</h1>')
    else:
        form = UserCreationForm()
        return render(request, 'main_app/signup.html', {'form': form})

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    print(user)
    characters = (Character.objects.filter(user=user))
    print(characters)
    return render(request, 'main_app/profile.html', {'username': username, 'characters': characters})


@method_decorator(login_required, name='dispatch')
class character_creation(CreateView):
    model = Character
    fields = '__all__'
    success_url = '/characters/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print('!!!!! SELF.OBJECT:', self.object)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/characters')

class character_update(UpdateView):
    model = Character
    fields = ['name', 'character_class', 'race', 'hit_points', 'spell_attack_bonus', 'spell_save_dc', 'strength_saving_throw', 'dexterity_saving_throw', 'constitution_saving_throw', 'intelligence_saving_throw', 'wisdom_saving_throw', 'charisma_saving_throw']

    def form_valid(self, form): # this will allow us to catch the pk to redirect to the show page
        self.object = form.save(commit=False) # don't post to the db until we say so
        self.object.save()
        return HttpResponseRedirect('/character/'+str(self.object.pk))

class character_delete(DeleteView):
    model = Character
    success_url = '/characters'


def character_index(request):
    # Get all cats from the db
    characters = Character.objects.all()
    return render(request, 'character/index.html', {'characters': characters})


def character_show(request, character_id):
    character = Character.objects.get(id=character_id)
    # weapons = Weapons.objects.all()
    return render(request, 'character/show.html', {'character': character})