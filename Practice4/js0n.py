import json
json_string = '{"name": "Alex", "age": 21}'
data = json.loads(json_string)

json_new = json.dumps(data, indent=4)

with open("sample-data.json", "w") as file:
    json.dump(data, file, indent=4)

with open("sample-data.json", "r") as file:
    loaded = json.load(file)
print(loaded)


data_from_file = {
    "name": "Alex",
    "age": 22,
    "skills": ["Python", "Math", "Physics"]
}

print(data_from_file["name"])     
print(data_from_file["skills"])   

for skill in data_from_file["skills"]:
    print(skill)
