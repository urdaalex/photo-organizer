import argparse
from exiftool import ExifToolHelper


parser = argparse.ArgumentParser(description='Syncs the EXIF dates of files in a source directory to the destination directory.')
parser.add_argument('src', help='Source directory')
parser.add_argument('dst', help='Destination directory')
parser.add_argument('--dst-format', help='Destination file extension override. Otherwise, will default to matching source file extension.')

args = parser.parse_args()
src = args.src
dst = args.dst
dst_format = args.dst_format

print(f'Source: {src}, Destination: {dst}, Destination Format: {dst_format}')

exit()

with ExifToolHelper(executable=".\\exiftool.exe") as et:
    metadata = et.get_metadata("D:\\Media\\staging\\videos\\C0001.MP4")
    print(metadata)

#.\exiftool.exe -tagsFromFile "D:\Media\staging\videos\C0001.MP4" -All:All  "D:\Media\staging\videos_processed\C0001.m4v" -overwrite_original