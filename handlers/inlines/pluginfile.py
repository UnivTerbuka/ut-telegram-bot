from telegram import (Update, InlineQuery, InlineQueryResultArticle,
                      InlineQueryResultDocument, InputTextMessageContent)
from core.context import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from libs.utils import format_html


@message_wrapper
@assert_token
def pluginfile(update: Update, context: CoreContext):
    query: InlineQuery = update.inline_query
    url: str = query.query
    # https://elearning.ut.ac.id/webservice/pluginfile.php/12345/mod_resource/content/0/File.pdf
    urls = url.split('/')
    resource_id = urls[5]
    resource_title = urls[-1].title()
    resource_url = url + '?token=' + context.moodle.token
    results = list()
    if url.endswith('.pdf'):
        result = InlineQueryResultDocument(
            id=resource_id,
            document_url=resource_url,
            title=resource_title,
            mime_type='application/pdf',
            description='File elearning.',
        )
        results.append(result)
    elif url.endswith('.zip'):
        result = InlineQueryResultDocument(
            id=resource_id,
            document_url=resource_url,
            title=resource_title,
            mime_type='application/zip',
            description='File elearning.',
        )
        results.append(result)
    else:
        result = InlineQueryResultArticle(
            id=resource_id,
            title=resource_title,
            input_message_content=InputTextMessageContent(
                resource_title + format_html.href('\u200c', resource_url),
                disable_web_page_preview=False,
            ))
        results.append(result)
    query.answer(
        results,
        cache_time=600,
        is_personal=True,
        switch_pm_text='Bantuan',
        switch_pm_parameter='inline-help',
    )
    return -1


pluginfile_pattern = r'^https:\/\/elearning\.ut\.ac\.id\/webservice\/pluginfile\.php\/\d+\/mod_resource\/content\/\d\/\S+$'  # NOQA
