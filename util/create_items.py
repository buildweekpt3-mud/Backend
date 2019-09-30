from commands.models import Item

i = 1
dataFromFile = {}
with open("util/item_data") as f:
    for line in f:
        x = line.split(":")
        print(x)
        item_name = x[0]
        description = x[1]
        dataFromFile[i] = (item_name, description)
        i += 1

for data in dataFromFile:
    print(dataFromFile[data][0])
    item = Item(item_name=dataFromFile[data]
                [0], description=dataFromFile[data][1])
    item.save()
