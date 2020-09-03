from datetime import datetime, timezone, timedelta
from libs.rss.pengumuman import Pengumuman


class TestPengumuma:
    title = '<div>Test Pengumuman</div>'
    link = 'https://www.ut.ac.id  '
    description = '<div>test</div>'
    pubdate = datetime(1999,
                       9,
                       19,
                       19,
                       19,
                       19,
                       tzinfo=timezone(timedelta(hours=+7)))
    creator = 'admin'

    def test_create_pengumuman(self):
        pengumuman = Pengumuman(
            title=self.title,
            link=self.link,
            description=self.description,
            pubdate=self.pubdate.strftime('%a, %d %b %Y %H:%M:%S %z'),
            creator=self.creator)
        assert pengumuman.title == 'Test Pengumuman'
        assert pengumuman.link == self.link.strip()
        assert ' ' not in pengumuman.link
        assert pengumuman.description == 'test'
        assert pengumuman.pubdate == self.pubdate
        assert pengumuman.creator == self.creator
