import os, sys
import argparse
from datetime import datetime



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Syncs the EXIF dates of files in a source directory to the destination directory.')
    parser.add_argument('src', help='Source directory')
    parser.add_argument('dst', help='Destination directory')
    parser.add_argument('--dst-format', help='Destination file extension override. Otherwise, will default to matching source file extension.')

    args = parser.parse_args()
    dst_file_format = args.dst_format

    src_path = args.src
    if not os.path.exists(src_path):
        print("Source path does not exist")
        sys.exit(1)

    dst_path = args.dst
    if not os.path.exists(dst_path):
        print("Destination path does not exist")
        sys.exit(1)

    skipped_files = []
    processed_file = []

    import os

    # Get a list of all the files in the directory
    src_files = os.listdir(src_path)

    # Create an empty dictionary to hold the filenames (without extensions) and paths eg. {filename (without extension): path)}
    src_file_dict = {}

    # Iterate over the dest files and add them to the dictionary
    for file in src_files:
        # Ignore directories and hidden files
        if os.path.isfile(os.path.join(src_path, file)) and not file.startswith('.'):
            f_no_ext = os.path.splitext(file)[0]
            f_ext = (dst_file_format or os.path.splitext(file)[1])
            f_dest = f_no_ext + f_ext
            src_file_dict[f_dest] = os.path.join(src_path, file)


    for f in os.listdir(src_path):
        src_date = os.path.getmtime(os.path.join(src_path, f))
        src_datetime = datetime.fromtimestamp(src_date)

        f_no_ext = os.path.splitext(f)[0]

        filepath_to_check = os.path.join(dst_path, f)
        if(os.path.exists(filepath_to_check)):
            os.utime(filepath_to_check, (src_date, src_date))
            processed_file.append(f)
        else:
            skipped_files.append(f)

    print(f'Processed: {len(processed_file)} files\n Skipped: {len(skipped_files)} files, [{skipped_files}]')
            