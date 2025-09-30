import json

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf8') as file:
        data = json.load(file)
    return data

def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_entry(data, new_entry):
    data.append(new_entry)

def modify_entry(data, key, value, update):
    for entry in data:
        if entry.get(key) == value:
            entry.update(update)

def exists_in_json(data, key, value):
    for entry in data:
        if entry.get(key) == value:
            return True
    return False

def exists_and_get_in_json(data, key, value):
    for entry in data:
        if entry.get(key) == value:
            return entry
    return None

if __name__ == "__main__":
    file_path = 'users/test.json'
    
    data = read_json_file(file_path)
    
    # Add a new entry
    #new_entry = {"id": 3, "name": "Charlie", "age": 28}
    #add_entry(data, new_entry)
    
    modify_entry(data, key='vat', value='111111111', update={"saek": [1]})
    
    write_json_file(file_path, data)
    
    print("JSON file updated successfully.")
