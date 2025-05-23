from enum import Enum
from datetime import datetime, timedelta

from module.base.timer import Timer
from module.exception import RequestHumanTakeover
from module.logger import logger
from tasks.base.ui import UI
from tasks.base.page import page_balloon
from tasks.base.assets.assets_base_page import CLOSE
from tasks.balloon.assets.assets_balloon import START, AUTO, CANCEL, OCR_DURATION
from module.ocr.ocr import Duration


class BalloonStatus(Enum):
    ENTER = 0
    AUTO = 1
    START = 2
    CLOSE = 3
    FINISH = 4


class Balloon(UI):
    def ocr_duration(self):
        ocr = Duration(OCR_DURATION)

        timeout = Timer(2, count=6).start()
        failed_duration = timedelta(0)
        duration = failed_duration
        for _ in self.loop():
            duration = ocr.ocr_single_line(self.device.image)
            if duration != failed_duration:
                break
            logger.warning(f'Invalid duration: {duration}')
            if timeout.reached():
                logger.warning('Get duration timeout. Set to 15 minutes instead.')
                return timedelta(minutes=15)

        logger.attr(f'Duration', str(duration))
        return duration

    def handle_balloon(self, status):
        match status:
            case BalloonStatus.ENTER:
                if self.appear(CANCEL):
                    return BalloonStatus.FINISH
                return BalloonStatus.AUTO
            
            case BalloonStatus.AUTO:
                self.device.click(AUTO)
                return BalloonStatus.START
            
            case BalloonStatus.START:
                self.device.click(START)
                return BalloonStatus.ENTER
            
            case BalloonStatus.FINISH:
                return status 

            case _:
                logger.warning(f'Invalid status: {status}')

        return status

    def run(self):
        self.ui_ensure(page_balloon)
        action_timer = Timer(0.5, 1)
        status = BalloonStatus.ENTER

        while 1:
            self.device.screenshot()

            if self.ui_additional():
                continue

            if action_timer.reached_and_reset():
                logger.attr('Status', status)
                status = self.handle_balloon(status)

            if status == BalloonStatus.FINISH:
                break

        next_run = datetime.now() + self.ocr_duration()
        self.config.task_delay(target=next_run)
