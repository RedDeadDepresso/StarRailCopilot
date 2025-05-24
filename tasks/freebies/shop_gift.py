from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_shop
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_shop_gift import GIFT, GAME_SUPPLIES


class ShopGift(UI):

    def run(self):
        self.ui_ensure(page_shop)
        action_timer = Timer(1).start()
        game_supplies_coords = []

        while 1:
            self.device.screenshot()
            if self.ui_additional():
                continue
            if action_timer.reached_and_reset():
                if self.appear_then_click(GIFT):
                    logger.info("Receive gift")
                    break

                if not game_supplies_coords:
                    game_supplies_coords = GAME_SUPPLIES.match_multi_template(self.device.image)

                if game_supplies_coords:
                    self.device.click(game_supplies_coords[0])
                    continue
