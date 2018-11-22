import base64
import io

from requests import get, exceptions
from PIL import Image

frame_prev = None
frame_curr = None
threshold = 12

ipcam_address = ''


def get_frames():
    try:
        frame_pre = get(ipcam_address)
        frame_cur = get(ipcam_address)

    # витягнути зображення з запитів
    except exceptions.ConnectionError:
        return None, None
    return frame_cur, frame_pre


def get_photo():
    try:
        photo = get(ipcam_address)
        # витягнути зображення з запиту
    except exceptions.ConnectionError:
        return None
    return photo


def motion_detect(frame_curr, frame_prev):
    return dist(d_hash(frame_prev), d_hash(frame_curr)) > threshold


def receive_frames(request):
    if 'file' in request.POST:
        global frame_curr
        global frame_prev
        frame_prev = frame_curr

        # get photo from request

        # frame_curr = photo
        imgdata = base64.b64decode(str(base64_string))
        frame_curr = Image.open(io.BytesIO(imgdata)).convert('LA')
        motion = motion_detect(frame_curr, frame_prev)
        # + ще

def d_hash(img):
    img = img.resize((17, 17), Image.ANTIALIAS)
    row_hash = 0
    col_hash = 0
    for i in range(15):
        for j in range(15):
            row_bit = img[j][i] < img[j + 1][i]
            col_bit = img[i][j] < img[i][j + 1]
            row_hash = row_hash << 1 | row_bit
            col_hash = col_hash << 1 | col_bit
    return row_hash << 256 | col_hash


def dist(hash1, hash2):
    return bin(hash1 ^ hash2).count('1')