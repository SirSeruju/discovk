import requests
import hashlib
import urllib
import random
import string
import re


class VkAndroidApi(object):
    session = requests.Session()
    session.headers = {"User-Agent": "VKAndroidApp/4.13.1-1206 (Android 4.4.3; SDK 19; armeabi; ; ru)",
                       "Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, */*"}

    def __init__(this, login=None, password=None, token=None, secret=None, v=5.95):
        this.v = v
        this.device_id = "".join(random.choice(
            string.ascii_lowercase+string.digits) for i in range(16))

        if token is not None and secret is not None:
            this.token = token
            this.secret = secret
            return
        # Генерируем рандомный device_id
        answer = this.session.get(
            "https://oauth.vk.com/token?grant_type=password&scope=nohttps,audio&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username={login}&password={password}".format(
                login=login,
                password=password
            ),
            headers={'User-Agent': 'Mozilla/4.0 (compatible; ICS)'}).json()
        if("error" in answer):
            raise PermissionError("invalid login|password!")
        this.secret = answer["secret"]
        this.token = answer["access_token"]
        # Методы, "Открывающие" доступ к аудио. Без них, аудио получить не получится
        this.method('execute.getUserInfo', func_v=9),
        this._send('/method/auth.refreshToken?access_token={token}&v={v}&device_id={device_id}&lang=ru'.format(
            token=this.token, v=v, device_id=this.device_id))

    def method(this, method, **params):
        url = ("/method/{method}?v={v}&access_token={token}&device_id={device_id}".format(method=method, v=this.v, token=this.token, device_id=this.device_id)
               + "".join("&%s=%s" % (i, params[i])
                         for i in params if params[i] is not None)
        )
        return this._send(url, params, method)

    def _send(this, url, params=None, method=None, headers=None):
        hash = hashlib.md5((url+this.secret).encode()).hexdigest()
        if method is not None and params is not None:
            url = ("/method/{method}?v={v}&access_token={token}&device_id={device_id}".format(method=method, token=this.token, device_id=this.device_id, v=this.v)
                   + "".join(
                "&"+i+"="+urllib.parse.quote_plus(str(params[i])) for i in params if(params[i] is not None)
            ))
        if headers is None:
            return this.session.get('https://api.vk.com'+url+"&sig="+hash).json()
        else:
            return this.session.get('https://api.vk.com'+url+"&sig="+hash, headers=headers).json()
    _pattern = re.compile(r'/[a-zA-Z\d]{6,}(/.*?[a-zA-Z\d]+?)/index.m3u8()')

    def to_mp3(self, url):
        return self._pattern.sub(r'\1\2.mp3', url)
