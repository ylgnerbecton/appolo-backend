# coding: utf-8
import time
from subprocess import call
from django.core.management.base import BaseCommand
from apps.crawlers.crawler_pdf import CrawlerPDF
# from vsales.apps.exportation.models import ExportationBerkley
# from vsales.apps.utils.consts import PENDING


class Command(BaseCommand):
    help = 'Test Selenium lib'

    def handle(self, *args, **options):
        call(["pkill", "-f", "firefox"])
        time.sleep(3)

        # exportation_pending = ExportationBerkley.objects.filter(status=PENDING)
        # self.stdout.write(self.style.SUCCESS('%s: %d proposals has found' % (time.strftime('%d/%m/%Y %H:%M:%S'),
        #                                                                      exportation_pending.count())))

        # if exportation_pending:
        crawler = CrawlerPDF()
        # for exportation in exportation_pending:
        #     exportation.send(crawler)

        # crawler.driver.close()
        crawler.driver.quit()

