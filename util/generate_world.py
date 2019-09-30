from django.contrib.auth.models import User
from commands.models import Player, Room

import random


def createWorld():

    print("create_world called")
    Room.objects.all().delete()

    # Read data from file and keep in dictonary
    # Dictionary key : running number, starting from 1
    # Dictionary value : tuple of title and description read from data fle
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

    #
    # We will create a dictionary of rooms
    # dRoooms key (x,y) cordinates of room
    # dRooms value is the Room object at coordinates (x,y)
    dRooms = {}

    # Counters to track how many links were skipped
    totalSouthSkipped = 0
    totalWestSkipped = 0

    # We are going to place rooms on co-odrinates starting from (100,100)
    # We will go right and up by distance points.
    # So, first room coordinate is (100,100). Next room in same row will be (1distance, 100), (150, 100) and so on. Last room
    # in this row will be (350,100)
    # After being done this row, we move to next row above this, which has first room at (100, 1distance). Its next room will
    # be (1distance, 1distance), (150, 1distance) and so on.
    # This will we keep going up until last row, whose first room will be (100, 350).
    #

    startx, starty, distance = 1, 1, 1

    # Index to read data from dataFromFile
    dataFileIndex = 1
    for i in range(0, 10):  # For each row
        # We are in row number i. So, y cordinate is fixed at 100 + i*distance
        # now we will go through each column of this ith row, and set x co-ordinates and create room
        y = starty + i * distance
        for j in range(0, 10):
            # X, y co-ordinates of room
            x = startx + j * distance

            # We have x,y co-oridinate to create a room

            print("Date from file", (dataFromFile[dataFileIndex]))
            # Create room based on title, description, x and y co-ordinates
            room = Room(title=dataFromFile[dataFileIndex][0],
                        description=dataFromFile[dataFileIndex][1], x=x, y=y)
            room.save()
            dRooms[(x, y)] = room

            # Connect this room to its neghbour

            # First look north room, which is x, y + distance, but it should exist
            if (x, y - distance) in dRooms:
                northRoom = dRooms[(x, y + distance)]
                room.connectRooms(northRoom, "n")
                northRoom.connectRooms(room, "s")

            # Look south which is 100,100, south is x, y - distance
            if y - distance >= starty:
                if random.randint(1, 10) in (1, 2, 3, 4, 5, 6, 7, 8):  # Skip 20% of souths
                    southRoom = dRooms[(x, y - distance)]
                    room.connectRooms(southRoom, "s")
                else:
                    print("Skip adding south")
                    totalSouthSkipped += 1

            # Look east which is x + distance,y and should exist
            if (x - distance, y) in dRooms:
                westRoom = dRooms[(x - distance, y)]
                room.connectRooms(westRoom, "w")
                westRoom.connectRooms(room, "e")

            # Look west which is x + distance,y and should exist
            if x - distance >= startx:
                if random.randint(1, 10) in (1, 2, 3, 4, 5, 6, 7, 8):  # Skip 20% of west
                    westRoom = dRooms[(x - distance, y)]
                    room.connectRooms(westRoom, "w")
                else:
                    print("Skip adding west")
                    totalWestSkipped += 1

            dataFileIndex += 1

    print("Rooms : ", dRooms)
    for cord, room in dRooms.items():
        print(cord, ":", room)

    print("Total Skipped ", totalSouthSkipped, totalWestSkipped)

    players = Player.objects.all()
    for p in players:
        p.currentRoom = dRooms[(1, 1)].id
        p.save()
