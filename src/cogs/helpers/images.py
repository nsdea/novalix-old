#https://github.com/nsde-archive/lhbot/blob/0acf310365eae4c72aa2b5bc8978d62e0919f4d5/src/cogs/helpers/welcome.py

try:
    from . import config
except ImportError:
    import config

import random
import requests

from discord import Member, File

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def generate(base, member, name, pic):
    if not member:
        member = None

    if not name:
        name = random.choice(['ExampleUserName', 'Héllö :)', 'ONLIX#1662', 'cat', 'RickAstley133742'])

    if not pic:
        pic = random.choice([
            'https://cdn.discordapp.com/avatars/657900196189044736/5c2b9e07693b5d67c12d6d570c047350.jpg?size=256',
            'https://cdn.discordapp.com/avatars/795743605221621782/25c91f77d540aa4dae14e938f861a05a.jpg?size=256',
            'https://cdn.discordapp.com/avatars/787789079227006976/89b32306687d67ee8fdb5c67d638eaaa.jpg?size=256'
        ])

    TEXT_X = 177
    TEXT_Y = 100
    PROFILE_PIC_X = 55
    PROFILE_PIC_Y = 70
    TEXT_COLOR = 0xFFFFFF
    PROFILE_PIC_RESIZE = 90

    base_img = Image.open(f'media/{base}.jpg')

    name = name[:26] if name else None
    name_text = name
    profile_pic = pic

    if member:
        name_text = member.nick if member.nick else member.name
        profile_pic = member.avatar_url_as(size=256)

    profile_pic_path = f'temp/profile_pic_{member.id if member else name}.jpg'
    open(profile_pic_path, 'wb').write(requests.get(profile_pic).content)
    profile_pic = Image.open(profile_pic_path)

    profile_pic = profile_pic.resize((PROFILE_PIC_RESIZE, PROFILE_PIC_RESIZE))
    base_img.paste(profile_pic, (PROFILE_PIC_X, PROFILE_PIC_Y))

    draw_img = ImageDraw.Draw(base_img)
    font = ImageFont.truetype('media/font.ttf', 24)
    draw_img.text((TEXT_X, TEXT_Y), name_text, TEXT_COLOR, font=font)

    path = f'temp/{member.id if member else name.replace(" ", "_")}.jpg'
    base_img.save(path)

    if __name__ == '__main__':
        base_img.show()

    return File(path)

def join(member=None, name=None, pic=None):
    generate(base='join', member=member, name=name, pic=pic)

def leave(member=None, name=None, pic=None):
    generate(base='leave', member=member, name=name, pic=pic)

if __name__ == '__main__':
    join()
    leave()