import os, sys
from datetime import datetime



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python picorg.py <source_directory> <destination_directory>")
        sys.exit(1)

    src_path = sys.argv[1]
    if not os.path.exists(src_path):
        print("Source path does not exist")
        sys.exit(1)

    dst_path = sys.argv[2]
    if not os.path.exists(dst_path):
        print("Destination path does not exist")
        sys.exit(1)

    skipped_files = []
    processed_file = []

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
            