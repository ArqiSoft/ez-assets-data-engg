import json
import os

def parse_large_json(file_path, output_dir, max_chunk_size):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    current_chunk = []  # List to store JSON objects for the current chunk
    current_size = 0  # Size of the current chunk in bytes
    chunk_index = 1

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Calculate the size of the current line in bytes
            line_size = len(line.encode('utf-8'))

            # If adding the line would exceed the max_chunk_size, save the current chunk
            if current_size + line_size > max_chunk_size:
                save_chunk(output_dir, chunk_index, current_chunk)
                chunk_index += 1
                current_chunk = []  # Start a new chunk
                current_size = 0

            # Add the line to the current chunk
            current_chunk.append(line.strip())
            current_size += line_size

        # Save the last chunk
        if current_chunk:
            save_chunk(output_dir, chunk_index, current_chunk)

def save_chunk(output_dir, chunk_index, chunk_data):
    chunk_file = os.path.join(output_dir, f'chunk_{chunk_index}.json')
    with open(chunk_file, 'w', encoding='utf-8') as chunk:
        chunk.write('[\n')
        chunk.write(',\n'.join(chunk_data))  # Join the JSON objects with comma
        chunk.write('\n]')
    print(f'Saved {chunk_file}')

file_path = 'aggregated-properties.json'
# Directory to save the smaller chunks
output_dir = 'path'
# Maximum file size in bytes (25 megabytes)
max_file_size = 25 * 1024 * 1024  # 25 MB

parse_large_json(file_path, output_dir, max_file_size)



