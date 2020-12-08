from django.shortcuts import render, redirect
from .models import User, Board_Game, Player, Play
from django.contrib import messages
from .forms import AddGameForm
from xml.dom import minidom
import requests


def reg(request):
  if request.method == 'POST':
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
      for value in errors.items():
        messages.error(request, value)
      return redirect('/')
    else:
      new_user = User.objects.register(request.POST)
      request.session['user_id'] = new_user.id
      Player.objects.create(name = request.POST['player'], user=new_user)
      return redirect('/home')
  return render(request, 'login.html')


def login(request):
  if request.method == 'GET':
    return redirect('/')
  if not User.objects.authenticate(request.POST['username'], request.POST['password']):
    messages.error(request, 'Invalid Username/Password')
    return redirect('/')
  logged_user = User.objects.get(username=request.POST['username'])
  request.session['user_id'] = logged_user.id
  return redirect('/home')


def home(request):
  context = {
    'user': User.objects.get(id=request.session['user_id']),
    'all_games': Board_Game.objects.all()
  }
  context['form'] = AddGameForm()
  return render(request, 'index.html', context)

def logout(request):
  request.session.clear()
  return redirect('/')


def add_game(request):
  context = {}
  if request.method == "POST":
    form = AddGameForm(request.POST, request.FILES)
    if form.is_valid():
      title = form.cleaned_data.get('title')
      image = form.cleaned_data.get('image')
      obj = Board_Game.objects.create(
        title = title,
        image = image
      )
      obj.save()
      print(obj)
  return redirect('/home')


def profile(request, user_id):
  context = {
    'user': User.objects.get(id=user_id)
  }
  return render(request, 'profile.html', context)


def edit_profile(request, user_id):
  context = {
    'user': User.objects.get(id=user_id),
    'all_games': Board_Game.objects.all()
  }
  if request.method == 'POST':
    current_user = User.objects.get(id=user_id),
    current_user.about = request.POST['about']
    current_user.save()
    return redirect(f'/user/{user.id}')
  return render(request, 'edit_profile.html', context)


def game(request, game_title):
  context = {
    'game': Board_Game.objects.get(title=game_title)
  }
  print(context)
  return render(request, 'game.html', context)


def add_fav(request, game_title):
  game = Board_Game.objects.get(title=game_title)
  user = User.objects.get(id=request.session['user_id'])
  user.favorites.add(game)
  return redirect(f'/game/{game_title}')


def record_play(request, game_title):
  context = {
    'game': Board_Game.objects.get(title=game_title)
  }
  return render(request, 'record_play.html', context)


def game_search_api(term):
  response = requests.get(f'https://boardgamegeek.com//xmlapi/search?search={term}')
  doc = minidom.parseString(response.text)
  return {
    game.getAttribute('objectid'): {
      'name': game.getElementsByTagName('name')[0].firstChild.data,
      'year': game.getElementsByTagName('yearpublished')[0].firstChild.data
    }
    for game in doc.getElementsByTagName('boardgame')
  }


def game_search(request):
  return redirect(f"/game_search/{request.POST['q']}")


def game_search_results(request, term):
  results = game_search_api(term)
  print(results)
  return render(request, 'game_search.html', results)