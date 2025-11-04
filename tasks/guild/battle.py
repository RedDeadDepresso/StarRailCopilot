from enum import Enum

from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_guild
from tasks.base.ui import UI
from tasks.guild.assets.assets_guild_check_in import FOUNTAIN, GREET, LEVEL_UP


class CheckInStatus(Enum):
    FOUNTAIN = 0
    GREET = 2
    LEVEL_UP = 3
    FINISH = 2


class CheckIn(UI):
    def handle_check_in(self, status):
        match status:
            case CheckInStatus.FOUNTAIN:
                if self.appear_then_click(FOUNTAIN):
                    return CheckInStatus.FOUNTAIN
                if self.appear_then_click(GREET):
                    return CheckInStatus.GREET
                if self.appear_then_click(LEVEL_UP):
                    return CheckInStatus.LEVEL_UP
                
            case CheckInStatus.GREET:
                if self.appear_then_click(GREET):
                    return CheckInStatus.GREET
                return CheckInStatus.FINISH
            
            case CheckInStatus.LEVEL_UP:
                if self.appear_then_click(LEVEL_UP):
                    return CheckInStatus.LEVEL_UP
                return CheckInStatus.FINISH
                
            case CheckInStatus.FINISH:
                return status
            
            case _:
                logger.warning(f'Invalid status: {status}')

        return status

    def run(self):
        self.ui_ensure(page_guild)
        action_timer = Timer(0.5, 1)
        status = CheckInStatus.FOUNTAIN

        while 1:
            self.device.screenshot()

            if self.ui_additional():
                continue

            if action_timer.reached_and_reset():
                logger.attr('Status', status)
                status = self.handle_check_in(status)

            if status == CheckInStatus.FINISH:
                break

        self.config.task_delay(server_update=True)
