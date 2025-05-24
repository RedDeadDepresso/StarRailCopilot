from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_mailbox
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_mailbox import CLAIM_ALL


class Mailbox(UI):
    def run(self):
        self.ui_ensure(page_mailbox)
        action_timer = Timer(1).start()

        while 1:
            self.device.screenshot()
            if self.ui_additional():
                continue
            if action_timer.reached_and_reset():
                if self.match_color(CLAIM_ALL):
                    self.device.click(CLAIM_ALL)
                    logger.info("Receive mailbox")
                    continue
                else:
                    logger.info("Mailbox have been received")
                    break
