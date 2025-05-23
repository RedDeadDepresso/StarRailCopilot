import re

from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit, DigitCounter
from tasks.base.page import page_main
from tasks.base.ui import UI
from tasks.item.assets.assets_item_data import OCR_COIN, OCR_CRYSTAL, OCR_JUICY_STAMINA_JELLY, OCR_STAMINA_JELLY


class ResourceDigit(Digit):
    def after_process(self, result):
        result = result.replace(",", "")
        return super().after_process(result)


class ResourceDigitCounter(DigitCounter):
    def after_process(self, result):
        result = result.replace(",", "")
        return super().after_process(result)


class DataUpdate(UI):

    def _get_unlimited_resource(self, resource_name, ocr_button):
        ocr = ResourceDigit(ocr_button)

        timeout = Timer(2, count=6).start()
        resource = 0
        for _ in self.loop():
            resource = ocr.ocr_single_line(self.device.image)
            if resource > 0:
                break
            logger.warning(f'Invalid {resource_name} amount: {resource}')
            if timeout.reached():
                logger.warning('Get data timeout')
                break

        logger.attr(f'{resource_name.title()}', resource)
        return resource

    def _get_limited_resource(self, resource_name, ocr_button):
        ocr = ResourceDigitCounter(ocr_button)
        timeout = Timer(2, count=6).start()
        resource = 0
        for _ in self.loop():
            resource, _, total = ocr.ocr_single_line(self.device.image)
            if resource > 0:
                break
            logger.warning(f'Invalid {resource_name} amount: {resource}/{total}')
            if timeout.reached():
                logger.warning(f'Get {resource_name} timeout')
                break

        logger.attr(f'{resource_name.title()}', resource)
        return resource, total

    def run(self):
        self.ui_ensure(page_main, acquire_lang_checked=False)
        # item tab stays at the last used tab, switch to UpgradeMaterials
        coin = self._get_unlimited_resource('coin', OCR_COIN)
        crystal = self._get_unlimited_resource('crystal', OCR_CRYSTAL)
        stamina_jelly, stamina_jelly_total = self._get_limited_resource('stamina jelly', OCR_STAMINA_JELLY)
        juicy_stamina_jelly, juicy_stamina_jelly_total = self._get_limited_resource('juicy stamina jelly', OCR_JUICY_STAMINA_JELLY)

        with self.config.multi_set():
            self.config.stored.Coin.value = coin
            self.config.stored.Crystal.value = crystal
            self.config.stored.StaminaJelly.set(stamina_jelly, stamina_jelly_total)
            self.config.stored.JuicyStaminaJelly.set(juicy_stamina_jelly, juicy_stamina_jelly_total)
            self.config.task_delay(server_update=True)
