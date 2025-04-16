from .economy import router as economy_router
from .games import router as games_router
from .roleplay import router as roleplay_router
from .moderation.ban import router as ban_router
from .fun import router as fun_router

def register_all_commands(dp):
    """Регистрирует все команды бота"""
    dp.include_router(economy_router)
    dp.include_router(games_router)
    dp.include_router(roleplay_router)
    dp.include_router(ban_router)
    dp.include_router(fun_router) 