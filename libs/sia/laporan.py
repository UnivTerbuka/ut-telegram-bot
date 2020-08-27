from .base import BaseSia


class LaporanMixin(BaseSia):
    def cetak_lkam_semester(self, nim: str = None) -> str:
        nim = nim or getattr(self, 'nim')
        if not nim:
            return
        url = 'https://sia.ut.ac.id/lkam/lkam/cetak_LKAMSemester_txt/print?nim='  # NOQA
        res = self.session.get(url + str(nim))
        if res.status_code == 302:
            return

    def cetak_lkam_perbandingan(self, nim: str = None):
        nim = nim or getattr(self, 'nim')
        if not nim:
            return
        url = 'https://sia.ut.ac.id/lkam/lkam/cetak_LKAMPerbandingan_txt/print?nim='  # NOQA
        res = self.session.get(url + str(nim))
        if res.status_code == 302:
            return
