from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Room, Player, Item
from rest_framework.decorators import api_view
from util.generate_world import createWorld
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))


@csrf_exempt
@api_view(["GET"])
def generate_world(request):
    print("Create world")
    createWorld()
    return JsonResponse({}, safe=True)


@csrf_exempt
@api_view(["GET"])
def get_map(request):
    world = [{
        room.id: [
            {"x": room.x, "y": room.y},
            {"n": room.n_to, "e": room.e_to, "s": room.s_to, "w": room.w_to}
        ]
        for room in Room.objects.all()}]
    return JsonResponse(*world, safe=True)


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    items = [{"id": x.id, "name": x.item_name, "description": x.description}
             for x in room.item_set.all()]
    return JsonResponse({
        'uuid': uuid,
        'name': player.user.username,
        'inventory': [{"id": x.id, "name": x.item_name, "description": x.description} for x in player.item_set.all()],
        'room': {
            'id': room.id,
            'title': room.title,
            'description': room.description,
            'directions': {
                'n': room.n_to,
                'e': room.e_to,
                's': room.s_to,
                'w': room.w_to
            },
            'items': items
        },
        'players': players}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    user = request.user
    player = user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    items = [{"id": x.id, "name": x.item_name, "description": x.description}
             for x in room.item_set.all()]
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom = nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        items = [{"id": x.id, "name": x.item_name, "description": x.description}
                 for x in nextRoom.item_set.all()]
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({
            'name': player.user.username,
            'inventory': [{"id": x.id, "name": x.item_name, "description": x.description} for x in player.item_set.all()],
            'room': {
                'id': nextRoom.id,
                'title': nextRoom.title,
                'description': nextRoom.description,
                'directions': {
                    'n': nextRoom.n_to,
                    'e': nextRoom.e_to,
                    's': nextRoom.s_to,
                    'w': nextRoom.w_to
                },
                'items': items
            },
            'players': players,
            'error_msg': ""
        }, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({
            'name': player.user.username,
            'inventory': [{"id": x.id, "name": x.item_name, "description": x.description} for x in player.item_set.all()],
            'room': {
                'id': room.id,
                'title': room.title,
                'description': room.description,
                'directions': {
                    'n': room.n_to,
                    'e': room.e_to,
                    's': room.s_to,
                    'w': room.w_to
                },
                'items': items
            },
            'players': players,
            'error_msg': "You cannot move that way."
        }, safe=True)


# @csrf_exempt
@api_view(["POST"])
def take(request):
    user = request.user
    player = user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    item_id = int(data['item'])
    room = player.room()
    inventory = room.item_set.all()
    items = [{"id": x.id, "name": x.item_name, "description": x.description}
             for x in player.item_set.all()]
    error = ""

    if inventory.count() > 0:
        if item_id is not None and item_id > 0:
            player.take(Item.objects.get(pk=item_id))
            player.save()
            items = [{"id": x.id, "name": x.item_name, "description": x.description}
                     for x in player.item_set.all()]
        else:
            error = 'That item does not exist'
    else:
        error = 'That item is not in this room'

    return JsonResponse({'items': items, 'error_msg': error}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def drop(request):
    user = request.user
    player = user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    item_id = int(data['item'])
    room = player.room()
    items = [{"id": x.id, "name": x.item_name, "description": x.description}
             for x in player.item_set.all()]
    error = ""

    if len(items) > 0:
        if item_id is not None and item_id > 0:
            player.drop(Item.objects.get(pk=item_id))
            player.save()
            items = [{"id": x.id, "name": x.item_name, "description": x.description}
                     for x in player.item_set.all()]
        else:
            error = 'That item does not exist'
    else:
        error = 'That item is not in your inventory'

    return JsonResponse({'items': items, 'error_msg': error}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error': "Not yet implemented"}, safe=True, status=500)
