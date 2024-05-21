from enum import Enum

from aiogram import F, Router, types
from aiogram.types import CallbackQuery
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.formatting import Bold

from app_filters.chat_types import ChatTypes, IsAdmin
from handlers.navigation_proccesing import get_banner_data, get_marathon_capacities
from keyboards.reply import get_keyboard
from keyboards.inline import marathons_buttons, AdminCallBack, get_callback_buttons, finish_add_marathon_buttons, \
    change_marathon_buttons
from database.crud import MarathonsQuery

admin_router = Router()
admin_router.message.filter(ChatTypes(['private']))
admin_router.edited_message.filter(ChatTypes(['private']))


# Contents
# 1. FSM to add marathon
# 2. FSM to change marathon

@admin_router.callback_query(AdminCallBack.filter(F.banner == "admin_panel"))
async def admin_panel_callback(callback: CallbackQuery, callback_data: AdminCallBack):
    media, keyboards = await get_banner_data(level=1, banner_name=callback_data.banner)

    if callback_data.after_add:
        await callback.message.answer_photo(media.media, caption=media.caption, reply_markup=keyboards)
    else:
        await callback.message.edit_media(media=media, reply_markup=keyboards)
        await callback.answer()


# *********************** FSM to add marathon **********************


class AddMarathon(StatesGroup):
    # Шаги состояний
    name = State()
    header = State()
    description = State()
    price = State()
    discount = State()
    image = State()

    marathon_for_change = None

    texts = {
        "AddMarathon:name": "Введите название заново:",
        "AddMarathon:header": "Введите заголовок заново:",
        "AddMarathon:description": "Введите описание заново:",
        "AddProduct:price": "Введите стоимость заново:",
        "AddProduct:discount": "Введите скидку заново:",
        "AddProduct:image": "Этот пункт последний, поэтому...",
    }


# 1. FSM to add marathon

# 1.0 Становимся в состояние ожидания ввода name
@admin_router.callback_query(StateFilter(None), AdminCallBack.filter(F.banner == "add_marathon"))
async def add_marathon_callback(
        callback: types.CallbackQuery,
        state: FSMContext
):
    await callback.message.answer("Введите название марафона:")
    await state.set_state(AddMarathon.name)


# Хендлер отмены и сброса состояния должен быть всегда именно здесь,
# после того, как только встали в состояние номер 1 (элементарная очередность фильтров)
@admin_router.message(StateFilter("*"), Command("отмена"))
@admin_router.message(StateFilter("*"), F.text == "ОТМЕНА❌")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    media, keyboards = await get_banner_data(level=1, banner_name="admin_panel")
    await message.answer_photo(media.media, caption=media.caption, reply_markup=keyboards)


# Вернутся на шаг назад (на прошлое состояние)
@admin_router.message(StateFilter("*"), Command("назад"))
@admin_router.message(StateFilter("*"), F.text == "⬅️НАЗАД")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddMarathon.name:
        await message.answer(
            'Предидущего шага нет, или введите название марафона или напишите "отмена"'
        )
        return

    previous = None
    for step in AddMarathon.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу \n {AddMarathon.texts[previous.state]}"
            )
            return
        previous = step


# 1.1 Ловим данные для состояния name и потом меняем состояние на description
@admin_router.message(AddMarathon.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    if 4 >= len(message.text) >= 150:
        await message.answer(
            "Название марафона не должно превышать 150 символов\n"
            "или быть менее 5ти символов. \n Введите заново"
        )
        return

    keyboard = get_keyboard(buttons=("⬅️НАЗАД", "ОТМЕНА❌"))
    await state.update_data(name=message.text)
    await message.answer("Введите заголовок", reply_markup=keyboard)
    await state.set_state(AddMarathon.header)


# Хендлер для отлова некорректных вводов для состояния name
@admin_router.message(AddMarathon.name)
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст названия марафона")


# 1.2 Ловим данные для состояния header и потом меняем состояние на description
@admin_router.message(AddMarathon.header, F.text)
async def add_header(message: types.Message, state: FSMContext):
    if 4 >= len(message.text):
        await message.answer(
            "Слишком короткий заголовок. \n Введите заново"
        )
        return
    header = message.text
    keyboard = get_keyboard(buttons=("⬅️НАЗАД", "ОТМЕНА❌"))

    await state.update_data(header=header)
    await message.answer("Введите описание:", reply_markup=keyboard)
    await state.set_state(AddMarathon.description)


# Хендлер для отлова некорректных вводов для состояния description
@admin_router.message(AddMarathon.header)
async def add_header2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите заголовок")


# 1.3 Ловим данные для состояния description и потом меняем состояние на price
@admin_router.message(AddMarathon.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    if 4 >= len(message.text):
        await message.answer(
            "Слишком короткое описание. \n Введите заново"
        )
        return

    keyboard = get_keyboard(buttons=("⬅️НАЗАД", "ОТМЕНА❌"))
    await state.update_data(description=message.text)
    await message.answer("Введите цену:", reply_markup=keyboard)
    await state.set_state(AddMarathon.price)


# Хендлер для отлова некорректных вводов для состояния description
@admin_router.message(AddMarathon.description)
async def add_description2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите описание")


# 1.4 Ловим данные для состояния price и потом меняем состояние на discount
@admin_router.message(AddMarathon.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        await message.answer("Введите корректное значение цены")
        return

    keyboard = get_keyboard(buttons=("⬅️НАЗАД", "ОТМЕНА❌"))
    await state.update_data(price=price)
    await message.answer("Введите процент скидки:", reply_markup=keyboard)
    await state.set_state(AddMarathon.discount)


# Хендлер для отлова некорректного ввода для состояния price
@admin_router.message(AddMarathon.price)
async def add_price2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите стоимость товара")


# 1.5 Ловим данные для состояния discount и потом меняем состояние на image
@admin_router.message(AddMarathon.discount, F.text)
async def add_discount(message: types.Message, state: FSMContext):
    try:
        discount = int(message.text)
    except ValueError:
        await message.answer("Введите корректное значение цены")
        return

    await state.update_data(discount=discount)
    await message.answer("Загрузите изображение для поста марафона", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddMarathon.image)


# Хендлер для отлова некорректного ввода для состояния discount
@admin_router.message(AddMarathon.discount)
async def add_discount2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите процент скидки на марафон")


# 1.6 Ловим данные для состояния image и потом выходим из состояний
@admin_router.message(AddMarathon.image, or_f(F.photo))
async def add_image(message: types.Message, state: FSMContext):
    if message.photo:
        await state.update_data(image=message.photo[-1].file_id)
    else:
        await message.answer("Отправьте изображение для марафона")
        return

    data = await state.get_data()
    sub_data = {"header": data["header"], "text": data["description"]}
    new_instance = {attr: value for attr, value in data.items() if attr != "header" and attr != "description"}
    keyboard = finish_add_marathon_buttons()
    try:
        await MarathonsQuery.add_instance(new_instance=new_instance, sub_data=sub_data)
        text = f"Марафон {data['header']} успешно добавлен"
        await message.answer(text, reply_markup=keyboard)
        await state.clear()

    except Exception as e:
        await message.answer(
            f"Ошибка: \n{str(e)}\nЧто-то пошло не так🤷‍♂️",
            reply_markup=keyboard,
        )
        await state.clear()


# Ловим все прочее некорректное поведение для этого состояния
@admin_router.message(AddMarathon.image)
async def add_image2(message: types.Message, state: FSMContext):
    await message.answer("Отправьте изображение")


# *********************** To change marathon **********************


# 2. To change marathon

capacities_text = {"name": "Введите новое название",
                   "header": "Ведите новый заголовок",
                   "description": "Введите новое описание",
                   "price": "Введите новую цену",
                   "discount": "Введите новую скидку",
                   "image": "Добавьте новое изображение"}

capacities_buttons = {
    "name": "НАЗВАНИЕ",
    "header": "ЗАГОЛОВОК",
    "description": "ОПИСАНИЕ",
    "price": "ЦЕНА",
    "discount": "СКИДКА"
}


class ChangeMarathon(StatesGroup):
    # Шаги состояний
    marathon = State()
    marathon_id = State()
    attribute = State()
    capacity = State()


# 2.0 Отлавливаем нажатие кнопки "Изменить марафон"
@admin_router.callback_query(AdminCallBack.filter(F.banner == "change_marathon"))
async def change_marathon_callback(callback: types.CallbackQuery):
    keyboard = await marathons_buttons(level=2, role="admin", change_button=True)
    await callback.message.answer(
        "Выберете марафон, который Вы хотите изменить:",
        reply_markup=keyboard
    )


@admin_router.callback_query(AdminCallBack.filter(F.change))
async def change_marathon_callback(callback: types.CallbackQuery,
                                   callback_data: AdminCallBack):
    media, keyboard = await get_marathon_capacities(marathon=callback_data.marathon)
    await callback.message.delete()
    await callback.message.answer_photo(photo=media.media,
                                        caption=f"Марафон {media.caption}\n\nВыберите что Вы хотите изменить:",
                                        reply_markup=keyboard)


@admin_router.callback_query(StateFilter(None), AdminCallBack.filter(F.attribute))
async def change_marathon_capacity_callback(callback: types.CallbackQuery,
                                            callback_data: AdminCallBack,
                                            state: FSMContext):
    await state.update_data(marathon=callback_data.marathon)
    await state.update_data(marathon_id=callback_data.marathon_id)
    await state.update_data(attribute=callback_data.attribute)
    await callback.answer()
    await callback.message.answer(text=capacities_text[callback_data.attribute])
    await state.set_state(ChangeMarathon.capacity)


@admin_router.message(ChangeMarathon.capacity, or_f(F.text, F.photo))
async def update_marathon_capacity(message: types.Message, state: FSMContext):
    if message.text:
        if 2 >= len(message.text):
            await message.answer(f"Некорректное значение. Введите заново")
            return
        await state.update_data(capacity=message.text)
    elif message.photo:
        await state.update_data(capacity=message.photo[-1].file_id)

    data = await state.get_data()
    marathon = data["marathon"]
    new_data = {data["attribute"]: data["capacity"]}

    try:
        await MarathonsQuery.update_instance(instance_id=data["marathon_id"],
                                             new_instance_data=new_data,
                                             relationship="description")
        await message.answer(f"Значение для {capacities_buttons[data['attribute']]} "
                             f"было изменено на {data['capacity']}")

        if data["attribute"] == "name":
            media, keyboard = await get_marathon_capacities(marathon=new_data[data["attribute"]])
        else:
            media, keyboard = await get_marathon_capacities(marathon=marathon)

        await message.answer_photo(media.media,
                                   caption="Выберите что Вы хотите изменить:",
                                   reply_markup=keyboard)
        await state.clear()

    except Exception as e:
        await message.answer(
            f"Ошибка: \n{str(e)}\n",
        )
        await state.clear()
