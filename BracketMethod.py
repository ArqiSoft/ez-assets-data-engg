import json
from time import sleep
import sys

print('This is my code to isolate the individual Json objects, and input them to into a list to eventually be printed')

def find_first_brace_pair(file_path):
    print('Processing the first Json object...')
    print('This is how the first Json object looks')

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
    # print('However, when I run the code to iterate this process over the \n whole document I am getting this ValueError')
    with open(file_path, 'r', encoding='utf-8') as f:
        opening_positions = []
        level = 0
        count = 0
        while True:
            char = f.read(1)
            if char == '{':
                opening_positions.append(f.tell() - 1)  # Record the position of the opening brace
                level += 1
            elif char == '}':
                if opening_positions:
                    start_pos = opening_positions.pop()
                    if not opening_positions:  # If no more braces at the current level
                        count += 1
                        end_pos = f.tell()
                        f.seek(start_pos)
                        json_data = f.read(end_pos - start_pos)
                        print(f"Document {count}: {json_data}")
                        try:
                            parsed_json = json.loads(json_data)
                            json_objects.append(parsed_json)  # Append parsed JSON object to list
                        except json.JSONDecodeError as e:
                            # print(f"Error parsing JSON near position {start_pos}: {e}")
                            print(f"Problematic JSON found")
                            # print(f"Problematic JSON snippet: {json_data}")
                            raise ValueError("Invalid JSON format between brace pairs.") from e
                    level -= 1
            elif not char:
                break  # End of file
    return json_objects


def main(file_path = '/Users/rickzakharov/dev/arqisoft/ez-assets-data-engg/data/aggregated-properties.json'):
    try:
        formatted_json = find_first_brace_pair(file_path)
        print(formatted_json)
    except ValueError as e:
        print(e)
    try:
        extracted_json_objects = extract_json_sections(file_path)
        for obj in extracted_json_objects:
            print(json.dumps(obj, indent=2))  # Print each JSON object in formatted JSON
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     if len(sys.argv) > 1:  # Check if a file path was provided as an argument
#         print(f"Processing file: {sys.argv[1]}")
#         main(sys.argv[1])  # Pass the first command-line argument to main
#     else:
#         print("Usage: python BracketMethod.py <file_path>")
