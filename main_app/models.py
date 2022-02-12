from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Character(models.Model):
    name = models.CharField(max_length=50)
    character_class = models.CharField(max_length=50)
    race = models.CharField(max_length=50)
    hit_points = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spell_attack_bonus = models.IntegerField()
    spell_save_dc = models.IntegerField()
    strength_saving_throw = models.IntegerField()
    dexterity_saving_throw = models.IntegerField()
    constitution_saving_throw = models.IntegerField()
    intelligence_saving_throw = models.IntegerField()
    wisdom_saving_throw = models.IntegerField()
    charisma_saving_throw = models.IntegerField()

    def __str__(self):
        return self.name


class Weapons(models.Model):
    name = models.CharField(max_length=100)
    to_hit_bonus = models.IntegerField()
    damage_dice = models.IntegerField()
    damage_bonus = models.IntegerField()
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

