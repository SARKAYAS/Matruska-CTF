#!/usr/bin/python3

import sys
import getopt
import os
import zipfile
import tarfile
import magic

debug = False
max_depth = 1000  # Maksimum iç içe geçmiþ arþiv dosya derinliði
extracted_files = set()  # Çýkartýlan dosyalarý izlemek için küme

def main(argv):
    global debug
    infile = ""

    # Platform baðýmsýz root kullanýcý kontrolü
    if os.name == 'posix' and os.getuid() == 0:
        print("Hey, you just tried to run matryoshka as root.")
        print("I appreciate that you're so confident in my code. I really do.")
        print("But the fact is, this is an unfinished mess. *I* don't even run it as root.")
        print("There is a very real chance that this code will try to overwrite something incredibly important.")
        print("So try again, but not as root.")
        sys.exit(1337)

    try:
        opts, args = getopt.getopt(argv, "hi:d", ["infile=", "debug"])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit(0)
        elif opt == '-d':
            debug = True
        elif opt in ("-i", "--infile"):
            infile = arg

    if infile == "":
        help()
        sys.exit(1)

    # Baþlangýçta dosyayý çýkartma iþlemi baþlat
    extract_archive(infile, 0)

def extract_archive(archive_file, depth):
    if depth > max_depth:
        print(f"Error: Maximum depth limit ({max_depth}) exceeded for {archive_file}. Aborting.")
        return

    if archive_file in extracted_files:
        print(f"Warning: {archive_file} has already been extracted. Skipping.")
        return

    extracted_files.add(archive_file)  # Dosya çýkartýldý olarak iþaretlenir

    mime_type = magic.from_file(archive_file, mime=True)
    if debug:
        print(f"File {archive_file} found to be type {mime_type}")

    if mime_type == 'application/zip':
        extract_zip(archive_file, depth)
    elif mime_type == 'application/x-tar':
        extract_tar(archive_file, depth)
    else:
        print(f"Error: Unsupported file type for {archive_file}. Exiting.")

def extract_zip(zip_file, depth):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(zip_file))
        print(f"{zip_file} extracted successfully.")
        # Ýçinde baþka arþiv dosyalarý varsa onlarý da çýkart
        extract_nested_archives(os.path.dirname(zip_file), depth + 1)
    except zipfile.BadZipFile:
        print(f"Error: {zip_file} is not a valid zip file.")

def extract_tar(tar_file, depth):
    try:
        with tarfile.open(name=tar_file, mode='r') as tar_ref:
            tar_ref.extractall(os.path.dirname(tar_file))
        print(f"{tar_file} extracted successfully.")
        # Ýçinde baþka arþiv dosyalarý varsa onlarý da çýkart
        extract_nested_archives(os.path.dirname(tar_file), depth + 1)
    except tarfile.ReadError:
        print(f"Error: {tar_file} is not a valid tar file.")

def extract_nested_archives(directory, depth):
    # Verilen dizindeki tüm dosyalarý tara
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Dosyanýn türünü kontrol et
            mime_type = magic.from_file(file_path, mime=True)
            if mime_type == 'application/zip':
                extract_zip(file_path, depth)
            elif mime_type == 'application/x-tar':
                extract_tar(file_path, depth)

def help():
    print("Usage: matryoshka -i <Archive file in>")
    print("Options:")
    print("  -i, --infile <file>   ")

if __name__ == "__main__":
    main(sys.argv[1:])
