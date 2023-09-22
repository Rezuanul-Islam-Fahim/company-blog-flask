import os
from PIL import Image
from flask import current_app


def add_profile_pic(profile_pic, username):

    filename = profile_pic.filename
    pic_ext = filename.split('.')[-1]
    storage_filename = str(username) + '.' + pic_ext
    file_path = os.path.join(
        current_app.root_path,
        'static\profile_imgs',
        storage_filename
    )

    pic = Image.open(profile_pic)
    pic.thumbnail((200, 200))
    pic.save(file_path)

    return file_path
