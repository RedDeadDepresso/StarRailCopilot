from enum import Enum

from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_guild_gacha
from tasks.base.ui import UI
from tasks.guild.assets.assets_guild_gacha import DRAW_ALL, DRAW_POPUP, SKIP, REWARD_CLAIMED


class GachaStatus(Enum):
    DRAW_ALL = 0
    CONFIRM = 2
    SKIP = 3
    CLAIM = 4
    FINISH = 5


class Gacha(UI):
    def handle_gacha(self, status):
        match status:
            case GachaStatus.DRAW_ALL:
                if self.appear_then_click(DRAW_ALL):
                    return GachaStatus.DRAW_ALL
                if self.appear_then_click(DRAW_POPUP):
                    return GachaStatus.CONFIRM
                else:
                    return GachaStatus.FINISH
                
            case GachaStatus.CONFIRM:
                if self.appear_then_click(SKIP):
                    return GachaStatus.SKIP
                if self.appear_then_click(DRAW_POPUP):
                    return GachaStatus.CONFIRM
                
            case GachaStatus.SKIP:
                if self.appear_then_click(REWARD_CLAIMED):
                    return GachaStatus.CLAIM
                if self.appear_then_click(SKIP):
                    return GachaStatus.SKIP
                
            case GachaStatus.CLAIM:
                if self.appear_then_click(REWARD_CLAIMED):
                    return GachaStatus.CLAIM
                else:
                    return GachaStatus.FINISH
                
            case GachaStatus.FINISH:
                return status
            
            case _:
                logger.warning(f'Invalid status: {status}')

        return status

    def run(self):
        self.ui_ensure(page_guild_gacha)
        action_timer = Timer(0.5, 1)
        status = GachaStatus.DRAW_ALL

        while 1:
            self.device.screenshot()

            if self.ui_additional():
                continue

            if action_timer.reached_and_reset():
                logger.attr('Status', status)
                status = self.handle_gacha(status)

            if status == GachaStatus.FINISH:
                break

        self.config.task_delay(server_update=True)
