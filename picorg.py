import os, exifread, sys
from datetime import datetime
import struct

def get_exif(fn):
    fd = open(fn, 'rb')
    tags = exifread.process_file(fd)
    fd.close()
    return tags

def parse_exif_date(date):
    return datetime.strptime(date.values, '%Y:%m:%d %H:%M:%S')

def get_date(fn):
    exif_tags = get_exif(fn)

    possible_dates = [exif_tags.get('EXIF DateTimeOriginal'), exif_tags.get('Image DateTime'), exif_tags.get('EXIF DateTimeDigitized')]

    #remove None values
    possible_dates = [x for x in possible_dates if x is not None]

    #parse dates
    possible_dates = [parse_exif_date(x) for x in possible_dates]

    if len(possible_dates) > 0:
        return min(possible_dates)
    else:
        return None


def move_file(src_dir, src_fn, dst_dir, dst_fn):
    src = os.path.join(src_dir, src_fn)
    dst = os.path.join(dst_dir, dst_fn)
    
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    
    #print(f'Moving file: {src} -> {dst}')
    os.rename(src, dst)

def get_mov_timestamps(filename):
    ''' Returns the (creation, modification) date-time from .mov metadata.

        Returns None if a value is not available.
    '''
    ATOM_HEADER_SIZE = 8
    # difference between Unix epoch and QuickTime epoch, in seconds
    EPOCH_ADJUSTER = 2082844800

    creation_time = modification_time = None

    # search for moov item
    with open(filename, "rb") as f:
        while True:
            atom_header = f.read(ATOM_HEADER_SIZE)
            #~ print('atom header:', atom_header)  # debug purposes
            if atom_header[4:8] == b'moov':
                break  # found
            else:
                atom_size = struct.unpack('>I', atom_header[0:4])[0]
                f.seek(atom_size - 8, 1)

        # found 'moov', look for 'mvhd' and timestamps
        atom_header = f.read(ATOM_HEADER_SIZE)
        if atom_header[4:8] == b'cmov':
            raise RuntimeError('moov atom is compressed')
        elif atom_header[4:8] != b'mvhd':
            raise RuntimeError('expected to find "mvhd" header.')
        else:
            f.seek(4, 1)
            creation_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
            creation_time = datetime.fromtimestamp(creation_time)
            if creation_time.year < 1990:  # invalid or censored data
                creation_time = None

            modification_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
            modification_time = datetime.fromtimestamp(modification_time)
            if modification_time.year < 1990:  # invalid or censored data
                modification_time = None

    return (creation_time, modification_time)

def get_mp4_timestamps(fn):
    date = os.path.getmtime(fn)
    dt = datetime.fromtimestamp(date)
    return dt

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python picorg.py <directory>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print("Path does not exist")
        sys.exit(1)

    for f in os.listdir(path):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.arw')):
            date = get_date(os.path.join(path, f))
            if date:
                move_file(path, f, os.path.join(path, date.strftime('%Y-%m-%d')), f)
        elif f.lower().endswith('.mov'):
            date = get_mov_timestamps(os.path.join(path, f))[0]
            if date:
                move_file(path, f, os.path.join(path, date.strftime('%Y-%m-%d')), f)
        elif f.lower().endswith('.mp4'):
            date = get_mp4_timestamps(os.path.join(path, f))
            if date:
                move_file(path, f, os.path.join(path, date.strftime('%Y-%m-%d')), f)
            