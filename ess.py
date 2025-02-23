import os

# Path where files were extracted
extracted_path = 'D:/다운로드/mongodb-examples'

# Function to generate output for each file
def process_files_in_directory(path):
    result = ""
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            # Read the content of the file
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            # Append file name and content
            result += f"{file_name} is a file.\nContents of {file_name}:\n{content}\n"
            result += "-" * 50 + "\n"
        elif os.path.isdir(file_path):
            # If directory, mention it
            result += f"{file_name} is a directory.\n\n"
    return result

# Process the files in the extracted directory
output = process_files_in_directory(extracted_path)

# Save the result to a file for download or viewing
output_file_path = "D:/다운로드/mongodb_examples_summary.txt"
with open(output_file_path, "w", encoding="utf-8") as output_file:
    output_file.write(output)

output_file_path

print(output)