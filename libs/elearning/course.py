from dataclasses import dataclass


@dataclass
class Course:
    id: int
    fullname: str
    shortname: str
    idnumber: str
    summary: str
    summaryformat: int
    startdate: int
    # TODO startdate adalah Epoch time
    # datetime.datetime.fromtimestamp(1347517370)
    enddate: int
    visible: bool
    fullnamedisplay: str
    viewurl: str
    courseimage: str
    progress: int
    hasprogress: bool
    isfavourite: bool
    hidden: bool
    timeaccess: int
    # TODO timeaccess adalah Epoch time
    showshortname: bool
    coursecategory: str
