import json
import os
from time import sleep
import sys

print('This code will isolate the individual Json objects, and input them to into a list to eventually be saved as as smaller files, and seporate the json objects that are still unformatted correctly')



def extract_json_sections(file_path):
    """
    Extract individual JSON objects from a file and separate problematic JSONs.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        tuple: List of valid JSON objects and list of problematic JSON strings.
    """
    json_objects = []
    problematic_jsons = []

    # Open the file and read character by character
    with open(file_path, 'r', encoding='utf-8') as f:
        opening_positions = []  # Stack to keep track of opening braces
        level = 0  # Tracks the depth of nested braces
        count = 0  # Counts the number of JSON objects found
        while True:
            char = f.read(1)
            if char == '{':
                opening_positions.append(f.tell() - 1)
                level += 1
            elif char == '}':
                if opening_positions:
                    start_pos = opening_positions.pop()
                    if not opening_positions:  # We found a complete JSON object
                        count += 1
                        end_pos = f.tell()
                        f.seek(start_pos)
                        json_data = f.read(end_pos - start_pos)
                        ##print(f"Document {count}: {json_data}")
                        try:
                            parsed_json = json.loads(json_data)
                            json_objects.append(parsed_json)
                        except json.JSONDecodeError:
                            print(f"Problematic JSON found at document {count}")
                            problematic_jsons.append(json_data)
                    level -= 1
            elif not char:  # End of file
                break

    return json_objects, problematic_jsons



def save_json_objects(json_objects, output_dir, file_prefix, max_file_size_mb=20):
    """
    Save JSON objects into files, each file's size limited to a specified maximum.

    Args:
        json_objects (list): List of JSON objects to save.
        output_dir (str): Directory to save JSON files.
        file_prefix (str): Prefix for output file names.
        max_file_size_mb (int): Maximum file size in megabytes.
    """
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_index = 1
        current_file_size = 0
        current_objects = []
        file_size_limit = max_file_size_mb * 1024 * 1024  # Convert MB to bytes

        def save_current_objects():
            nonlocal file_index, current_file_size, current_objects
            if current_objects:
                file_name = os.path.join(output_dir, f'{file_prefix}_{file_index}.json')
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(current_objects, f, ensure_ascii=False, indent=4)
                print(f"Saved {len(current_objects)} JSON objects into {file_name} ({os.path.getsize(file_name) / (1024 * 1024):.2f} MB)")
                file_index += 1
                current_file_size = 0
                current_objects = []

        # Iterate over JSON objects and save them into files
        for obj in json_objects:
            obj_str = json.dumps(obj, ensure_ascii=False, indent=4)
            obj_size = len(obj_str.encode('utf-8'))

            if current_file_size + obj_size > file_size_limit:
                save_current_objects()
            
            current_objects.append(obj)
            current_file_size += obj_size

        # Save any remaining objects
        save_current_objects()

    except Exception as e:
        print(f"An error occurred while saving {file_prefix} objects: {e}")


def clean_problematic_jsons(problematic_jsons):
    """
    Clean problematic JSON strings by removing zero-width non-joiners and other extraneous characters.

    Args:
        problematic_jsons (list): List of problematic JSON strings.

    Returns:
        tuple: List of cleaned JSON objects and list of remaining problematic JSON strings.
    """
    cleaned_json_objects = []
    remaining_problematic_jsons = []

    for json_str in problematic_jsons:
        # Remove zero-width non-joiners and other extraneous characters
        cleaned_str = json_str.replace('​​​&zwnj;', '').replace('\n  {\n    \"_index\": \"aggregated-properti\",\"', '')
        try:
            parsed_json = json.loads(cleaned_str)
            cleaned_json_objects.append(parsed_json)
        except json.JSONDecodeError:
            remaining_problematic_jsons.append(cleaned_str)

    return cleaned_json_objects, remaining_problematic_jsons


def save_problematic_jsons(problematic_jsons, output_dir, objects_per_file=2000):
    """
    Save problematic JSON strings into files with a specified number of objects per file.

    Args:
        problematic_jsons (list): List of problematic JSON strings.
        output_dir (str): Directory to save problematic JSON files.
        objects_per_file (int): Number of objects per output file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    total_objects = len(problematic_jsons)
    num_files = (total_objects + objects_per_file - 1) // objects_per_file

    print(f"Size of problematic_jsons array: {total_objects}")

    for i in range(num_files):
        start_index = i * objects_per_file
        end_index = min(start_index + objects_per_file, total_objects)
        chunk = problematic_jsons[start_index:end_index]
        
        file_name = os.path.join(output_dir, f'problematic_jsons_{i + 1}.json')
        
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, ensure_ascii=False, indent=4)

    print(f"Saved {total_objects} problematic JSON objects into {num_files} files.")



def main():
    # Ask the user for the JSON file path
    file_path = input("Enter the path of the JSON file you want to process: ")
    
    # Extract JSON objects and problematic JSONs from the file
    json_objects, problematic_jsons = extract_json_sections(file_path)

    # Save valid JSON objects
    output_dir = 'Parsed_Json'
    save_json_objects(json_objects, output_dir, 'json_objects')

    # Save problematic JSONs
    problematic_output_directory = 'Problematic_Json'
    save_problematic_jsons(problematic_jsons, problematic_output_directory)

    # Clean problematic JSONs
    cleaned_json_objects, remaining_problematic_json_objects = clean_problematic_jsons(problematic_jsons)
    
    # Save cleaned JSON objects
    save_json_objects(cleaned_json_objects, 'cleaned_json_objects', 'cleaned_jsons')
    
    # Save remaining problematic JSONs
    save_json_objects(remaining_problematic_json_objects, 'remaining_problematic_jsons', 'still_problematic_jsons')

if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     if len(sys.argv) > 1:  # Check if a file path was provided as an argument
#         print(f"Processing file: {sys.argv[1]}")
#         main(sys.argv[1])  # Pass the first command-line argument to main
#     else:
#         print("Usage: python BracketMethod.py <file_path>")
