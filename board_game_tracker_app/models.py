from django.db import models
import re
import bcrypt
from django.utils import timezone

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
  def user_validator(self, postData):
    errors = {}
    for email_check in User.objects.all():
      if email_check.email == postData['email']:
        errors["email"] = "Email already exists in database"
    
    for username_check in User.objects.all():
      if username_check.username == postData['username']:
        errors["username"] = "Username already exists in database"

    if len(postData['username']) < 2:
      errors['username'] = "Username must be at least two characters long"
    
    if not EMAIL_REGEX.match(postData['email']):      
      errors['email'] = ("Invalid email address!")

    if len(postData['password']) < 8:
      errors['password'] = "Password must be at least eight characters"

    if postData['pw_confirm'] != postData['password']:
      errors['pw_confirm'] = "Password does not match"

    return errors

  def edit_validator(self, postData, this_user):
    errors = {}

    if postData['email'] != this_user.email:
      for email_check in User.objects.all():
        if email_check.email == postData['email']:
          errors["email"] = "Email already exists in database"
    
    if postData['username'] != this_user.email:
      for username_check in User.objects.all():
        if username_check.username == postData['username']:
          errors['username'] = 'Username already exists in database'

    if len(postData['username']) < 2:
      errors['username'] = "Username must be at least two characters long"    
    
    if not EMAIL_REGEX.match(postData['email']):      
      errors['email'] = "Invalid email address!"

    return errors

  def authenticate(self, username, password):
    users = self.filter(username=username)
    if not users:
        return False

    user = users[0]
    return bcrypt.checkpw(password.encode(), user.password.encode())

  def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            username = form['username'],
            email = form['email'],
            password = pw,
        )

class BoardGameManager(models.Manager):
  def game_validator(self, postData):
    errors = {}
    for id_check in Board_Game.objects.all():
      if id_check.bg_id == postData['bg_id']:
        errors['bg_id'] = "Board Game ID already exists" 

class User(models.Model):
  username = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

class Player(models.Model):
  name = models.CharField(max_length=255)
  created_by = models.ForeignKey(User, related_name='created_players', on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='player_name')

class Board_Game(models.Model):
  title = models.CharField(max_length=255)
  image = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=None)
  bg_id = models.IntegerField()
  favorited_by = models.ManyToManyField(User, related_name="favorites")
  objects = BoardGameManager()

  def __str__(self):
    return self.title

class Play(models.Model):
  date = models.DateField(default=timezone.now, blank=True)
  comments = models.TextField(null=True, blank=True)
  game = models.ForeignKey(Board_Game, on_delete=models.SET_NULL, null=True, blank=True)
  winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='num_of_wins')
  created_by = models.ForeignKey(User, related_name='plays', on_delete=models.CASCADE, null=True, blank=True)
  players = models.ManyToManyField(Player, related_name="plays", through="Score")


class Score(models.Model):
  vps=models.IntegerField(null=True, blank=True)
  play=models.ForeignKey(Play, on_delete=models.CASCADE, related_name="score")
  player=models.ForeignKey(Player, on_delete=models.CASCADE, related_name="score")



