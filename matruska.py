import zipfile
import os

def extract_deepest(archive_path, extract_dir):
    current_path = archive_path

    while True:
        with zipfile.ZipFile(current_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            print(f"Extracted: {current_path}")
            files = zip_ref.namelist()

        found_archive = False

        for file in files:
            file_path = os.path.join(extract_dir, file)
            if zipfile.is_zipfile(file_path):
                current_path = file_path
                found_archive = True
                break
            elif file.endswith('.txt'):
                print(f"Found target file: {file_path}")
                return file_path

        if not found_archive:
            print("No more nested archives found.")
            break

# Örnek kullanım:
extract_deepest("matruska.zip", "output_folder")
