from aiogram.types import BotCommand

private_commands = [
    BotCommand(command="marathons", description="марафоны"),
    BotCommand(command="buy_marathon", description="стать участником марафона"),
    BotCommand(command="faq", description="часто задаваемые вопросы"),
    BotCommand(command="contacts", description="контакты"),
    BotCommand(command="about", description="о боте"),
    BotCommand(command="help", description="список доступних команд")
]