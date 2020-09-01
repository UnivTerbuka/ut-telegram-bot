import logging
import requests
from dacite import from_dict
from dataclasses import dataclass
from typing import List

logging.basicConfig(filename='moodle.log',
                    filemode='a',
                    format='%(name)s %(message)s',
                    level=logging.INFO)

logger = logging.getLogger('success')
logger_failed = logging.getLogger('except')


@dataclass
class Function:
    name: str
    version: str


@dataclass
class AdvancedFeature:
    name: str
    value: int


@dataclass
class User:
    sitename: str
    username: str
    # username = NIM
    firstname: str
    lastname: str
    fullname: str
    lang: str
    userid: int
    siteurl: str
    userpictureurl: str
    functions: List[Function]
    downloadfiles: int
    uploadfiles: int
    release: str
    version: str
    mobilecssurl: str
    advancedfeatures: List[AdvancedFeature]
    usercanmanageownfiles: bool
    userquota: int
    usermaxuploadfilesize: int
    userhomepage: int
    siteid: int
    sitecalendartype: str
    usercalendartype: str
    theme: str


ENDPOINT_API = 'https://elearning.ut.ac.id/webservice/rest/server.php'
# core_webservice_get_site_info

data = {
    'wstoken': '',
    'wsfunction': 'core_webservice_get_site_info',
    'moodlewsrestformat': 'json',
}

res = requests.post(ENDPOINT_API, data=data)
if res.ok:
    print('OK')

user: User = from_dict(User, res.json())
for func in user.functions:
    data['wsfunction'] = func.name
    res = requests.post(ENDPOINT_API, data=data)
    if not res.ok:
        continue
    res_data: dict = res.json()
    if type(res_data) == dict and 'exception' in res_data:
        logger_failed.info('{} ({} {})'.format(
            repr(func), res_data.get('exception'),
            res_data.get('message') or res_data.get('errorcode')))
    else:
        logger.info(repr(func))
