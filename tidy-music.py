import mutagen
import mutagen.mp3
import os
import errno
import mimetypes

input_path = '.'
base_path = os.path.realpath(input_path)
output_path = os.path.join(base_path, 'art')

def rel_path(base, path):
    assert path.startswith(base)
    return path[len(base):]

mime_dict = {
    'image/jpeg': '.jpg',
    'image/png': '.png'
}

def save_art(file):
    file_path = os.path.realpath(file)
    mutagen_file = mutagen.mp3.MP3(file_path)
    
    output_folder = os.path.join(output_path + rel_path(base_path, file_path))
    make_dir(output_folder)
    
    file_ext = mime_dict[mutagen_file.tags['APIC:'].mime]
    file_name = mutagen_file.tags['TIT2'][0] + file_ext
    output_file = os.path.join(output_folder, file_name)

    art = mutagen_file.tags['APIC:'].data
    with open(output_file, 'wb') as img:
        img.write(art)

def make_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

ls = os.walk(base_path)
make_dir(output_path)
for (path, folders, files) in ls:
    for file in files:
        if file.lower().endswith('.mp3'):
            save_art(file)
