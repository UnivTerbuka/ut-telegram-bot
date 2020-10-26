from logging import getLogger
from telegram import Update

from moodle.core.course import BaseCourse
from moodle.mod.forum import BaseForum

from core import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from config import CALLBACK_SEPARATOR
from libs.elearning.forum import forum_buttons
from libs.utils.helpers import make_button

logger = getLogger(__name__)


@message_wrapper
@assert_token
def forums(update: Update, context: CoreContext):
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # FORUMS|course_id
    course_id = int(datas[1])
    course = BaseCourse(context.moodle).get_courses_by_field("id", str(course_id))[0]
    forums_ = BaseForum(context.moodle).get_forums_by_courses([course_id])
    context.query.answer()
    if not forums_:
        context.query.edit_text(
            text=f"Tidak ada forum untuk {course.shortname}.",
            reply_markup=make_button("< Kembali", f"COURSE|{course_id}"),
        )
        return -1
    context.query.edit_message_text(
        text=f"Forum untuk {course.shortname}",
        reply_markup=forum_buttons(forums_),
    )
    return -1


forums_pattern = r"^FORUMS\|\d+$"
