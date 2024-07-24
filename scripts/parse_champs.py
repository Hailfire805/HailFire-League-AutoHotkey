import json

# Read JSON data from a file with UTF-8 encoding
with open('../src/champions_raw.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Extract "name" as the key and "key" as the value
keys = {details['name']: details['key'] for champion, details in json_data['data'].items()}

# Define the output file path
output_file_path = '../src/Champion_Ids.json'

# Write the extracted keys to a new JSON file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(keys, output_file, indent=4, ensure_ascii=False)

print(f"Extracted keys have been saved to {output_file_path}")
