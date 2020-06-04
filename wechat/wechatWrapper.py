import os
import json
import requests

# <code\>
CORPID = 'wwd26b80b105de25f6'

def get_token(secret):
    '''
    获取应用的token，agent为应用名称
    '''
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    values = {'corpid': CORPID, 'corpsecret': secret}
    req = requests.post(url, params=values)
    data = json.loads(req.text)
    return data['access_token']

class UserManager(object):
    '''
    获取某个应用的用户信息
    '''

    def __init__(self, agent):
        self.name = '通讯录'
        self.corpid = CORPID
        self.secret = AgentSecrets[self.name]
        self.agent_name = agent
        self.agent_id = AgentIds[agent]
        self.token = get_token(self.name)

    def get_department_list(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/department/list'
        values = {'access_token': self.token}
        req = requests.post(url, params=values)
        res = json.loads(req.text)
        return {x['id']: x for x in res['department']}

    def get_department_member(self, department_id, fetch_child=1):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/user/simplelist'
        values = {
            'access_token': self.token,
            'department_id': department_id,
            'fetch_child': fetch_child
        }
        req = requests.post(url, params=values)
        res = json.loads(req.text)
        return res

    def get_tag_list(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/tag/list'
        values = {'access_token': self.token}
        req = requests.post(url, params=values)
        res = json.loads(req.text)
        return res

    def get_tag_member(self, tagid):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/tag/get'
        values = {
            'access_token': self.token,
            'tagid': tagid
        }
        req = requests.post(url, params=values)
        res = json.loads(req.text)
        return {x['id']: x for x in res['department']}

# <code\>
class MediaTypes(object):
    '''
    素材类型
    '''
    IMAGE = 'image'
    VOICE = 'voice'
    VIDEO = 'video'
    FILE = 'file'


def check_file(path, media_type):
    '''
    检查文件是否存在，是否符合大小限制
    '''
    if not os.path.isfile(path):
        return False
    fsize = os.path.getsize('test.jpg') / 1024.0 / 1024.0
    if media_type == MediaTypes.IMAGE:
        if fsize >= 2.0:
            return False
    elif media_type == MediaTypes.VOICE:
        if fsize >= 2.0:
            return False
    elif media_type == MediaTypes.VIDEO:
        if fsize >= 10.0:
            return False
    elif media_type == MediaTypes.FILE:
        if fsize >= 20.0:
            return False
    return True


def upload_media(path, media_type, token):
    '''
    上传本地素材
    '''
    upload_url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload'
    info = {
        'access_token': token,
        'type': media_type
    }
    data = {'media': open(path, 'rb')}
    r = requests.post(url=upload_url, params=info, files=data)
    res = r.json()
    assert 'media_id' in list(res.keys())
    return res['media_id']


def download_media(path, media_id, token):
    '''
    下载素材
    '''
    download_url = 'https://qyapi.weixin.qq.com/cgi-bin/media/get'
    info = {
        'access_token': token,
        'media_id': media_id
    }
    r = requests.post(url=download_url, params=info)
    with open(path, 'wb') as f:
        f.write(r.content)
    return r

class MsgTypes(object):
    '''
    消息类型
    '''
    TEXT = 'text'
    IMAGE = 'image'
    VOICE = 'voice'
    VIDEO = 'video'
    FILE = 'file'
    TEXTCARD = 'textcard'
    NEWS = 'news'
    MPNEWS = 'mpnews'


# 企业微信API
# https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN

class MsgCourier(object):
    '''
    生成消息，发送消息
    '''

    def __init__(self, agent, agent_id, agent_secret):
        self.agent = agent
        self.agent_id = agent_id
        self.agent_secret = agent_secret
        self.token = get_token(agent_secret)
        self.url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token

    def send_msg(self, msg):
        values = json.dumps(msg)
        requests.post(self.url, values)

    def _get_msg_with_content_(self, agent_id, msg_type, content):
        values = {'touser': '@all',
                  'agentid': agent_id,
                  "msgtype": msg_type,
                  msg_type: content}
        return values

    def get_text_msg(self, text):
        content = {'content': text}
        return self._get_msg_with_content_(self.agent_id, MsgTypes.TEXT, content)

    def get_media_msg(self, path, media_type, **more_info):
        meta_id = upload_media(path, media_type, self.agent)
        content = {"media_id": meta_id}
        content.update(more_info)
        msg_type = media_type
        return self._get_msg_with_content_(msg_type, content)

    def get_textcard_msg(self, title, description, url):
        content = {
            'title': title,
            'description': description,
            'url': url,
            'btntxt': '更多'
        }
        return self._get_msg_with_content_(MsgTypes.TEXTCARD, content)

    def get_news_msg(self, title, description, url, picture_url):
        article = {"title": title,
                   'description': description,
                   'url': url,
                   'picurl': picture_url,
                   'btntxt': '更多'
                   }
        content = {'articles': [article]}
        return self._get_msg_with_content_(MsgTypes.NEWS, content)

    def get_article(self, title, author, content, digest, url, thumb_img_path):
        media_id = upload_media(thumb_img_path,
                                MediaTypes.IMAGE,
                                self.token)

        article = {"title": title,
                   "thumb_media_id": media_id,
                   "author": author,
                   "content_source_url": url,
                   "content": content,
                   "digest": digest
                   }
        return article

    def get_mpnews_msg(self, article, *articles):
        all_articel = [article]
        all_articel.extend(articles)
        content = {
            "articles": all_articel
        }
        return self._get_msg_with_content_(MsgTypes.MPNEWS, content)

def quick_send_msg(agent, msg, agent_id='', agent_secret=''):
    '''
    快速发送文本消息
    '''
    msgCourier = MsgCourier(agent,agent_id,agent_secret)
    msg = msgCourier.get_text_msg(text=msg)
    return msgCourier.send_msg(msg)