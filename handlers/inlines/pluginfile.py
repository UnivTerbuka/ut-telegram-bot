from telegram import Update, InlineQuery, InlineQueryResultDocument
from core.context import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper


@message_wrapper
@assert_token
def pluginfile(update: Update, context: CoreContext):
    query: InlineQuery = update.inline_query
    url: str = query.query
    # https://elearning.ut.ac.id/webservice/pluginfile.php/9661772/mod_resource/content/0/RAT.pdf
    urls = url.split('/')
    result = InlineQueryResultDocument(
        id=urls[5],
        document_url=url + '?token=' + context.moodle.token,
        title=urls[-1],
        mime_type='application/pdf',
        description='File elearning.',
    )
    results = [result]
    query.answer(
        results,
        cache_time=600,
        is_personal=True,
        switch_pm_text='Bantuan',
        switch_pm_parameter='inline-help',
    )
    return -1


pluginfile_pattern = r'^https:\/\/elearning\.ut\.ac\.id\/webservice\/pluginfile\.php\/\d+\/mod_resource\/content\/\d\/\S+\.pdf$'  # NOQA
