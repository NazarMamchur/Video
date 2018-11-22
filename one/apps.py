from django.apps import AppConfig
from requests import get, exceptions
from rest_framework import status
from json import loads
from collections import namedtuple
from . import views


class OneConfig(AppConfig):
    name = 'one'


class AppConfigCustom(AppConfig):
    name = "on_startup"
    verbose_name = "On startup"

    address = "http://httpbin.org/get/"

    def ready(self):
        while True:
            frame_curr, frame_prev = views.get_frames()
            motion = views.motion_detect(frame_curr, frame_prev)
            if motion:

            try:
                r = get(self.address)
            except exceptions.ConnectionError:
                exit(-1)
            if r.status_code is status.HTTP_204_NO_CONTENT:
                continue
            elif r.status_code is status.HTTP_200_OK:
                data = loads(r.text, object_hook=lambda d: namedtuple('cam', d.keys())(*d.values()))
                time_lock = int(data.timeLock)
                if data.body.task == 'SEND PHOTO':
                    base64 = views.get_photo()
