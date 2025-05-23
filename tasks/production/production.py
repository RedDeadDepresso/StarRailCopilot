from enum import Enum

from module.base.timer import Timer
from module.exception import RequestHumanTakeover
from module.logger import logger
from tasks.base.ui import UI
from tasks.base.page import page_dashboard
from tasks.base.page import DASHBOARD_CHECK
from tasks.production.assets.assets_production import OPEN_PRODUCE_ALL, CONFIRM_PRODUCE_ALL


class ProductionStatus(Enum):
    ENTER = 0
    OPEN = 1
    CONFIRM = 2
    FINISH = 3


class Production(UI):
    def handle_production(self, status):
        match status:
            case ProductionStatus.ENTER:
                if self.appear(OPEN_PRODUCE_ALL):
                    return ProductionStatus.OPEN
                self.device.click(DASHBOARD_CHECK)
            case ProductionStatus.OPEN:
                if self.appear(CONFIRM_PRODUCE_ALL):
                    return ProductionStatus.CONFIRM
                self.device.click(OPEN_PRODUCE_ALL)
            case ProductionStatus.CONFIRM:
                if not self.appear(CONFIRM_PRODUCE_ALL):
                    return ProductionStatus.FINISH
                self.device.click(CONFIRM_PRODUCE_ALL)
            case ProductionStatus.FINISH:
                return status
            case _:
                logger.warning(f'Invalid status: {status}')

        return status

    def run(self):
        self.ui_ensure(page_dashboard)
        action_timer = Timer(0.5, 1)
        status = ProductionStatus.ENTER

        while 1:
            self.device.screenshot()

            if self.ui_additional():
                continue

            if action_timer.reached_and_reset():
                logger.attr('Status', status)
                status = self.handle_production(status)

            if status == ProductionStatus.FINISH:
                break

        self.config.task_delay(minute=self.config.ProductionInterval_value)
