import json

def find_first_brace_pair(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        opening_positions = []
        level = 0
        while True:
            char = f.read(1)
            if char == '{':
                opening_positions.append(f.tell() - 1)  # Record the position of the opening brace
                level += 1
            elif char == '}':
                if opening_positions:
                    start_pos = opening_positions.pop()
                    if not opening_positions:  # If no more braces at the current level
                        end_pos = f.tell()
                        f.seek(start_pos)
                        json_data = f.read(end_pos - start_pos)
                        try:
                            parsed_json = json.loads(json_data)
                            return json.dumps(parsed_json, indent=2)  # Return formatted JSON string
                        except json.JSONDecodeError as e:
                            raise ValueError("Invalid JSON format between brace pairs.") from e
                    level -= 1
            elif not char:
                break  # End of file
    raise ValueError("No complete brace pair found in the JSON file.")

json_objects = []
def extract_json_sections(file_path):
    
    with open(file_path, 'r', encoding='utf-8') as f:
        opening_positions = []
        level = 0
        while True:
            char = f.read(1)
            if char == '{':
                opening_positions.append(f.tell() - 1)  # Record the position of the opening brace
                level += 1
            elif char == '}':
                if opening_positions:
                    start_pos = opening_positions.pop()
                    if not opening_positions:  # If no more braces at the current level
                        end_pos = f.tell()
                        f.seek(start_pos)
                        json_data = f.read(end_pos - start_pos)
                        try:
                            parsed_json = json.loads(json_data)
                            json_objects.append(parsed_json)  # Append parsed JSON object to list
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON near position {start_pos}: {e}")
                            print(f"Problematic JSON snippet: {json_data}")
                            raise ValueError("Invalid JSON format between brace pairs.") from e
                    level -= 1
            elif not char:
                break  # End of file
    return json_objects


# Example usage:
'''file_path = 'aggregated-properties.json'
try:
    formatted_json = find_first_brace_pair(file_path)
    print(formatted_json)
except ValueError as e:
    print(e)'''

# Example usage:
'''file_path = 'aggregated-properties.json'
try:
    extracted_json_objects = extract_json_sections(file_path)
    for obj in extracted_json_objects:
        print(json.dumps(obj, indent=2))  # Print each JSON object in formatted JSON
except ValueError as e:
    print(e)'''
