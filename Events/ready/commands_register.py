from aiogram import Bot
from aiogram.types import BotCommand
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Функция для получения локальных команд
def get_local_commands():
    # Локальные команды
    return [
        {"name": "start", "description": "Запустить бота", "deleted": False},
        {"name": "help", "description": "Получить справку", "deleted": False},
        {"name": "menu", "description": "Открыть меню", "deleted": False},
        {"name": "feedback", "description": "Оставить отзыв", "deleted": True},  # Удаляемая команда
    ]

# Функция для проверки различий между командами
def are_commands_different(existing_command, local_command):
    return (
        existing_command.command != local_command["name"]
        or existing_command.description != local_command["description"]
    )

# Функция для регистрации/удаления команд
async def register_commands(bot: Bot):
    try:
        # Получаем локальные и зарегистрированные команды
        local_commands = get_local_commands()
        application_commands = await bot.get_my_commands()

        # Преобразуем зарегистрированные команды в словарь
        existing_commands = {cmd.command: cmd for cmd in application_commands}

        for local_command in local_commands:
            name = local_command["name"]
            description = local_command["description"]
            is_deleted = local_command.get("deleted", False)

            # Если команда уже существует
            if name in existing_commands:
                existing_command = existing_commands[name]

                # Если команда помечена на удаление
                if is_deleted:
                    await bot.delete_my_commands(scope=None)
                    logger.info(f"🗑 Удалена команда '{name}'.")
                    continue

                # Если команда изменилась
                if are_commands_different(existing_command, local_command):
                    await bot.set_my_commands(
                        [BotCommand(command=name, description=description)]
                    )
                    logger.info(f"🔁 Изменена команда '{name}'.")
            else:
                # Если команда отсутствует и не помечена как удалённая
                if is_deleted:
                    logger.info(f"⏩ Пропущена команда '{name}', помечена на удаление.")
                    continue

                await bot.set_my_commands(
                    [BotCommand(command=name, description=description)]
                )
                logger.info(f"👍 Зарегистрирована команда '{name}'.")

    except Exception as error:
        logger.error(f"Произошла ошибка: {error}")
