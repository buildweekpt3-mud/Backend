from django.contrib.auth.models import User
from commands.models import Player, Room, Item

from django.db.models import Max
import random


def get_random_item():
    max_id = Item.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        item = Item.objects.filter(pk=pk).first()
        if item:
            return item


def createWorld():

    print("create_world called")
    Room.objects.all().delete()

    i = 1
    dataFromFile = {}
    with open("util/data") as f:
        for line in f:
            x = line.split(":")
            print(x)
            title = x[0]
            description = x[1]
            dataFromFile[i] = (title, description)
            i += 1

    dRooms = {}

    # Counters to track how many links were skipped
    totalNorthSkipped = 0
    totalWestSkipped = 0

    startx, starty, distance = 1, 1, 1

    # Index to read data from dataFromFile
    dataFileMaxIndex = len(dataFromFile)
    for i in range(0, 10):  # For each row
        # We are in row number i. So, y cordinate is fixed at 100 + i*distance
        # now we will go through each column of this ith row, and set x co-ordinates and create room
        y = starty + i * distance
        for j in range(0, 10):
            # X, y co-ordinates of room
            x = startx + j * distance

            # We have x,y co-oridinate to create a room
            rand_room_id = random.randint(1, dataFileMaxIndex)
            print("Date from file", (dataFromFile[rand_room_id]))

            # Create room based on title, description, x and y co-ordinates
            room = Room(title=dataFromFile[rand_room_id][0],
                        description=dataFromFile[rand_room_id][1], x=x, y=y)
            room.save()
            if random.randint(1, 10) in (1, 2, 3, 4, 5, 6):  # Skip 40% of items
                item = get_random_item()
                room.addItem(item)
                room.save()
            dRooms[(x, y)] = room

            # Connect rooms

            # First look south room, which is x, y + distance, but it should exist
            if (x, y + distance) in dRooms:
                southRoom = dRooms[(x, y + distance)]
                room.connectRooms(southRoom, "s")
                southRoom.connectRooms(room, "n")

            # Look north which is 100,100, north is x, y - distance
            if y - distance >= starty:
                if random.randint(1, 10) in (1, 2, 3, 4, 5, 6, 7, 8):  # Skip 20% of norths
                    northRoom = dRooms[(x, y - distance)]
                    room.connectRooms(northRoom, "n")
                    northRoom.connectRooms(room, "s")
                else:
                    print("Skip adding south")
                    totalNorthSkipped += 1

            # Look east which is x + distance,y and should exist
            if (x + distance, y) in dRooms:
                eastRoom = dRooms[(x + distance, y)]
                room.connectRooms(eastRoom, "e")
                eastRoom.connectRooms(room, "w")

            # Look west which is x + distance,y and should exist
            if x - distance >= startx:
                if random.randint(1, 10) in (1, 2, 3, 4, 5, 6, 7, 8):  # Skip 20% of west
                    westRoom = dRooms[(x - distance, y)]
                    room.connectRooms(westRoom, "w")
                    westRoom.connectRooms(room, "e")
                else:
                    print("Skip adding west")
                    totalWestSkipped += 1

    print("Rooms : ", dRooms)
    for cord, room in dRooms.items():
        print(cord, ":", room)

    print("Total Skipped ", totalNorthSkipped, totalWestSkipped)

    players = Player.objects.all()
    for p in players:
        p.currentRoom = dRooms[(1, 1)].id
        p.save()
