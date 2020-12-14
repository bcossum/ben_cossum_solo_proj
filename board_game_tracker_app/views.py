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
      Player.objects.create(name = request.POST['player'], created_by=new_user, user=new_user)
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
  }
  context['form'] = AddGameForm()
  return render(request, 'index.html', context)

def logout(request):
  request.session.clear()
  return redirect('/')


def profile(request, user_id):
  context = {
    'user': User.objects.get(id=user_id)
  }
  return render(request, 'profile.html', context)


#Not Added Yet
def edit_profile(request, user_id):
  context = {
    'user': User.objects.get(id=user_id),
  }
  if request.method == 'POST':
    current_user = User.objects.get(id=user_id),
    current_user.about = request.POST['about']
    current_user.save()
    return redirect(f'/user/{user.id}')
  return render(request, 'edit_profile.html', context)

def edit_play(request, game_id, play_id):
  context = {
    'play': Play.objects.get(id=play_id),
    'user': User.objects.get(id=request.session['user_id'])
  }
  if request.method == 'POST':
    this_play=Play.objects.get(id=play_id)
    this_play.date=request.POST['date']
    this_play.winner=Player.objects.get(id=request.POST['winner'])
    for player in this_play.score.all():
      player.vps=request.POST[f'vps_{player.id}']
      player.save()
    this_play.save()
    return redirect(f'/game/{game_id}/view_play/{play_id}/submit')
  return render(request, 'edit_play.html', context)


def add_fav(request, game_id):
  if request.method == 'POST':
    errors = Board_Game.objects.game_validator(request.POST)
    if errors:
      for value in errors.items():
        messages.error(request, value)
      return redirect(f'/game/{game_id}')
      
    else:
      user = User.objects.get(id=request.session['user_id'])
      for game in Board_Game.objects.all():
        if game.bg_id == game_id:
          this_game=Board_Game.objects.get(bg_id=game_id)
          user.favorites.add(this_game)
          return redirect(f'/game/{game_id}')
          
      this_game = Board_Game.objects.create(
        title=request.POST['title'],
        image=request.POST['image'],
        bg_id=request.POST['bg_id'],
      )
      user.favorites.add(this_game)
  return redirect(f'/game/{game_id}')


def record_play(request, game_id):
  if request.method == "POST":
    this_user=User.objects.get(id=request.session['user_id'])
    for game in Board_Game.objects.all():
      if game.bg_id == game_id:
        this_game = Board_Game.objects.get(bg_id=game_id)
        new_play=Play.objects.create(created_by=this_user, game=this_game)
        return redirect(f'/game/{game_id}/record_play/{new_play.id}')
        
    this_game = Board_Game.objects.create(
      title=request.POST['title'],
      image=request.POST['image'],
      bg_id=request.POST['bg_id'],
    )
    new_play=Play.objects.create(
      created_by=this_user, 
      game=this_game
      )
    return redirect(f'/game/{game_id}/record_play/{new_play.id}')
  return redirect(f'/game/{game_id}')

def record_play_form(request, game_id, play_id):
  context = {
    'play': Play.objects.get(id=play_id),
    'game': Board_Game.objects.get(bg_id=game_id),
    'user': User.objects.get(id=request.session['user_id'])
  }
  return render(request, 'record_play.html', context)

def add_player(request, game_id, play_id):
  if request.method == "POST":
    this_play = Play.objects.get(id=play_id)
    this_user = User.objects.get(id=request.session['user_id'])
    for player in this_user.created_players.all():
      if player.name == request.POST['name']:
        this_play.players.add(player)
        return redirect(f"/game/{game_id}/record_play/{play_id}")
    new_player = Player.objects.create(
      name=request.POST['name'],
      created_by=this_user,
      )
    this_play.players.add(new_player)
  return redirect(f"/game/{game_id}/record_play/{play_id}")  


def submit_play(request, game_id, play_id):
  if request.method == 'POST':
    this_play=Play.objects.get(id=play_id)
    this_play.date=request.POST['date']
    this_play.comments=request.POST['comments']
    print(request.POST['winner'])
    this_play.winner=Player.objects.get(id=request.POST['winner'])
    for player in this_play.score.all():
      print(request.POST[f'vps_{player.player.id}'])
      player.vps=request.POST[f'vps_{player.player.id}']
      player.save()
    this_play.save()
    return redirect(f'/game/{game_id}/view_play/{play_id}/submit')

  context = {
    'user': User.objects.get(id=request.session['user_id']),
    'play': Play.objects.get(id=play_id),
  }  
  return render(request, 'view_play.html', context)


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
  context = {
    'user': User.objects.get(id=request.session['user_id']),
    'results': results
  }
  return render(request, 'game_search.html', context)

def game_page_api(game_id):
  response = requests.get(f'https://www.boardgamegeek.com/xmlapi/boardgame/{game_id}')
  doc = minidom.parseString(response.text)

  return {
    game.getAttribute('objectid'): {
      'name': next(
        (name for name in game.getElementsByTagName('name') if name.getAttribute('primary') == 'true'),
        game.getElementsByTagName('name')[0]
      ).firstChild.data,
      'year': game.getElementsByTagName('yearpublished')[0].firstChild.data,
      'image': game.getElementsByTagName('image')[0].firstChild.data,
      'description': game.getElementsByTagName('description')[0].firstChild.data,
      'minplayers': game.getElementsByTagName('minplayers')[0].firstChild.data,
      'maxplayers': game.getElementsByTagName('maxplayers')[0].firstChild.data,
    }
    for game in doc.getElementsByTagName('boardgame')
  }

def game_page(request, game_id):
  results = game_page_api(game_id)
  context = {
    'user': User.objects.get(id=request.session['user_id']),
    'results': results
  }
  print(results)
  return render(request, 'game.html', context)