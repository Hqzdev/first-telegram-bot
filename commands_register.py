import logging
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",

)
logger = logging.getLogger(__name__)


COMMANDS = [
    botCommand(command="/start", description="Start the bot"),
    botCommand(command="/help", description="Get help"),
    botCommand(command="/menu", description="Show the menu"),   
    botCommand(command="/ban", description="Ban a user"),
    botCommand(command="kick", description="Kick a user"),


]



async def register_commands(bot: Bot):
     current_commands = await bot.get_my_commands(scope=BotCommandScopeDefault())
     current_set = {(cmd.command, cmd.description) for cmd in current_commands}
     new_set = {(cmd.command, cmd.description) for cmd in COMMANDS}


     if current_set != new_set:
         await bot.set_my_commands(COMMANDS)


         if current_set - new_set:
             logger.info(f"Removed commands: {current_set - new_set}")
         if new_set - current_set:
             logger.info(f"Added commands: {new_set - current_set}")
     else:
         logger.info("Commands are up to date")

     logger.info(f"Bot is ready! Commands: {len(COMMANDS)}")
        