from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_gacha
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_gacha_gift import CLAIM, ENTER, CHECK


class GachaGift(UI):

    def run(self):
        self.ui_ensure(page_gacha)
        action_timer = Timer(1).start()
        enter_coords = []

        while 1:
            self.device.screenshot()
            if self.ui_additional():
                continue
            if action_timer.reached_and_reset():
                if not enter_coords:
                    enter_coords = ENTER.match_multi_template(self.device.image)
                    if enter_coords:
                        self.device.click(enter_coords[0])
                        continue

                if not self.appear(CHECK):
                    self.device.click(enter_coords[0])
                    continue

                if self.appear_then_click(CLAIM):
                    continue
                else:
                    break
