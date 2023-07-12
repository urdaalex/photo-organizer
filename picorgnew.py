import argparse, os, sys
from exiftool import ExifToolHelper
from datetime import datetime, date

parser = argparse.ArgumentParser(description='Organizes photos and movies according to EXIF metadata')
parser.add_argument('dir', help='The directory to organize')
parser.add_argument('--dry-run', help='', action="store_true")

args = parser.parse_args()
dir = args.dir
is_dry_run = args.dry_run

if is_dry_run:
    print("~~~~DRY RUN~~~~")

def move_file(src_dir, src_fn, dst_dir, dst_fn):
    src = os.path.join(src_dir, src_fn)
    dst = os.path.join(dst_dir, dst_fn)
    
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    
    if is_dry_run:
        print(f'Would move file: {src} -> {dst}')
    else:
        pass
        #os.rename(src, dst)

if not os.path.exists(dir):
    print("Path does not exist")
    sys.exit(1)

with ExifToolHelper() as et:
    for f in os.listdir(dir):
        f_full = os.path.join(dir, f)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.arw','.mov','.mp4')):
            print(f'getting metadata for {f_full}')
            metadata = et.get_metadata(f_full)
            file_dt = datetime.strptime(metadata[0]["EXIF:CreateDate"], "%Y:%m:%d %H:%M:%S")
            move_file(dir,f, os.path.join(dir, file_dt.strftime('%Y-%m-%d')), f)
