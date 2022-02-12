import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Character, Weapons
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        location = text_data_json['top-location']
        if text_data_json['weapon']:
            @sync_to_async
            def get_weapon(weapon):
                return Weapons.objects.get(id=weapon)
            weapon = await get_weapon(text_data_json['weapon'])
            dam_roll = text_data_json['damage']
            hit_roll = text_data_json['hit']
            total_hit = hit_roll + weapon.to_hit_bonus
            total_dam = dam_roll + weapon.damage_bonus
            message = message + str(total_hit) + ' to hit, ' + str(total_dam) + ' damage'

        if text_data_json['save']:
            @sync_to_async
            def get_save(name):
                return Character.objects.get(name = name)
            character = await get_save(message)
            if text_data_json['save'] == 'strength':
                save_bonus = character.strength_saving_throw
            elif text_data_json['save'] == 'dexterity':
                save_bonus = character.dexterity_saving_throw  
            elif text_data_json['save'] == 'constitution':
                save_bonus = character.constitution_saving_throw 
            elif text_data_json['save'] == 'wisdom':
                save_bonus = character.wisdom_saving_throw 
            elif text_data_json['save'] == 'intelligence':
                save_bonus = character.intelligence_saving_throw 
            elif text_data_json['save'] == 'charisma':
                save_bonus = character.charisma_saving_throw   
            tot_roll = text_data_json['roll'] + save_bonus
            message = message + ': ' + str(tot_roll) + ' ' + text_data_json['save'] + ' saving throw'

        if text_data_json['spell']:
            @sync_to_async
            def get_save(name):
                return Character.objects.get(name = name)
            character = await get_save(message)
            spell_bonus = character.spell_attack_bonus
            tot_roll = text_data_json['roll'] + spell_bonus
            message = message + ': ' + str(tot_roll) + ' to hit'

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': [message, location]
            }
        )

    async def chat_message(self, event):
        message = event['message'] 
        await self.send(text_data=json.dumps({
                'message': message
            }))

    async def send_from_view(self, event):
        await self.send(
            json.dumps({
                'type': 'events.alarm',
                'content': event['content']
            })
        )
