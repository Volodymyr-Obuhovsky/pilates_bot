from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# reply_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="Topics"),
#             KeyboardButton(text="Portfolio")
#         ],
#         [
#             KeyboardButton(text="FAQ"),
#             KeyboardButton(text="Help")
#         ],
#         [
#             KeyboardButton(text="About")
#         ]
#     ],
#     resize_keyboard=True,
#     input_field_placeholder="What are you interesting in?"
# )

del_keyboard = ReplyKeyboardRemove()


def get_keyboard(buttons: tuple[str],
                 size: tuple,
                 placeholder: str = None,
                 request_contact: int = None,
                 request_location: int = None):

    reply_keyboard = ReplyKeyboardBuilder()

    for index, name_button in enumerate(buttons, start=1):

        if request_contact and request_contact == index:
            reply_keyboard.add(KeyboardButton(text=name_button, request_contact=True))
        if request_location and request_location == index:
            reply_keyboard.add(KeyboardButton(text=name_button, request_location=True))
        else:
            reply_keyboard.add(KeyboardButton(text=name_button))

    # setting size of our keyboards, numbers are buttons quantity in a row
    return reply_keyboard.adjust(*size).as_markup(resize_keyboard=True, input_field_placeholder=placeholder)


# example addition button in existing keyboards
# reply_keyboard.row(KeyboardButton(text="Button"))

