from module.logger import logger
from module.base.base import ModuleBase
from tasks.guild.gacha import Gacha
from tasks.guild.battle import Battle


class Guild(ModuleBase):
    def run(self):
        """
        Run all freebie tasks
        """
        if self.config.GuildCheckIn_Enable:
            logger.hr('Guild Check In')
            from tasks.guild.check_in import CheckIn
            CheckIn(config=self.config, device=self.device).run()

        if self.config.GuildBattle_Enable:
            logger.hr('Guild Battle')
            Battle(config=self.config, device=self.device).run()

        if self.config.GuildGacha_Enable:
            logger.hr('Guild Gacha')
            Gacha(config=self.config, device=self.device).run()
            
        self.config.task_delay(server_update=True)