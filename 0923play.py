import json

addlist = []
for i in 'helloworld':
    addlist.append(i)
with open('python\\new1.json', 'w') as jsonfile:
    json.dump(addlist, jsonfile)
    result = json.load(jsonfile)
    print(result)