from module.logger import logger
from module.base.base import ModuleBase
from tasks.freebies.mailbox import Mailbox
from tasks.freebies.shop_gift import ShopGift
from tasks.freebies.gacha_gift import GachaGift


class Freebies(ModuleBase):
    def run(self):
        """
        Run all freebie tasks
        """
        if self.config.Mailbox_Enable:
            logger.hr('Mailbox')
            Mailbox(config=self.config, device=self.device).run()

        if self.config.ShopGift_Enable:
            logger.hr('Shop Gift')
            ShopGift(config=self.config, device=self.device).run()

        if self.config.GachaGift_Enable:
            logger.hr('Gacha Gift')
            GachaGift(config=self.config, device=self.device).run()
            
        self.config.task_delay(server_update=True)