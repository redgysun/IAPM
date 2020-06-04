import os


def delete_file(file_path):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_ROOT=os.path.join(BASE_DIR, 'media')
    file_full_path = os.path.join(MEDIA_ROOT, file_path)
    if os.path.exists(file_full_path):
        if os.path.isfile(file_full_path):
            #return file_full_path
            os.remove(file_full_path)
