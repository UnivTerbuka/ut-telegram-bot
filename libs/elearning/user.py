from dataclasses import dataclass
from typing import List


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
