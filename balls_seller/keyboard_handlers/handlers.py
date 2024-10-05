import os
import sys

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, InputMediaPhoto, Bot
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

sys.path.append("../")
from db_handlers.handlers import *
from third_party.picture_redactor import *
from third_party.ops import *


def get_avaliable_common_pictures(common_ball_type=None, common_ball_material=None, common_ball_color=None):
    pictures_paths, pictures_names = get_common_pictures_from_DB(common_ball_type, common_ball_material,
                                                                 common_ball_color)
    keyboard = []
    kbrd_line = []
    kbrd_line_length = 2
    picture_counter = 1
    for i in range(len(pictures_paths)):
        kbrd_line.append(InlineKeyboardButton(
            f"{common_ball_color} {picture_counter}",
            callback_data="[" + common_ball_type + "]=[" + common_ball_material + "]=[" + common_ball_color + "]=[" +
                          pictures_names[i] + "]"))
        picture_counter += 1
        if len(kbrd_line) == kbrd_line_length:
            keyboard.append(kbrd_line)
            kbrd_line = []
    if len(kbrd_line) != 0:
        keyboard.append(kbrd_line)
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back|show_common_colors")])
    return keyboard, pictures_paths


def get_avalible_common_colors_and_amount(common_ball_type=None, common_ball_material=None):
    common_colors_price_amount = get_common_color_price_amount_DB(common_ball_type, common_ball_material)
    if len(common_colors_price_amount) == 0:
        price = 0
    else:
        price = common_colors_price_amount[0][1]
    keyboard = []
    colors = set([line[0] for line in common_colors_price_amount if line[2] != 0])
    for color in colors:
        keyboard.append([InlineKeyboardButton(f"{color}", callback_data=color)])
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back|show_common_materials")])
    return keyboard, price


def get_avalible_common_types():
    common_types = get_common_types_from_DB()
    keyboard = []
    kbrd_line = []
    kbrd_line_length = 2
    for i in range(len(common_types)):
        kbrd_line.append(InlineKeyboardButton(
            f"{common_types[i]}",
            callback_data=common_types[i]))
        if len(kbrd_line) == kbrd_line_length:
            keyboard.append(kbrd_line)
            kbrd_line = []
    if len(kbrd_line) != 0:
        keyboard.append(kbrd_line)
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back|show_our_balls")])
    return keyboard


def get_avalible_common_materials(common_ball_type=None):
    common_materials = get_common_materials_from_DB(common_ball_type)
    keyboard = []
    for i in range(len(common_materials)):
        keyboard.append([InlineKeyboardButton(
            f"{common_materials[i]}",
            callback_data=common_materials[i])])
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back|show_common_types")])
    return keyboard


def get_avaliable_shaped_types():
    shaped_types = get_shaped_types_from_DB()
    keyboard = []
    kbrd_line = []
    kbrd_line_length = 2
    for i in range(len(shaped_types)):
        kbrd_line.append(InlineKeyboardButton(
            f"{shaped_types[i]}",
            callback_data=shaped_types[i]))
        if len(kbrd_line) == kbrd_line_length:
            keyboard.append(kbrd_line)
            kbrd_line = []
    if len(kbrd_line) != 0:
        keyboard.append(kbrd_line)
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back|show_our_balls")])
    return keyboard


def get_avaliable_shaped_subtypes(shaped_ball_type=None):
    shaped_subtypes = get_shaped_subtypes_from_DB(shaped_ball_type)
    keyboard = []
    kbrd_line = []
    kbrd_line_length = 2
    for i in range(len(shaped_subtypes)):
        kbrd_line.append(InlineKeyboardButton(
            f"{shaped_subtypes[i]}",
            callback_data=shaped_subtypes[i]))
        if len(kbrd_line) == kbrd_line_length:
            keyboard.append(kbrd_line)
            kbrd_line = []
    if len(kbrd_line) != 0:
        keyboard.append(kbrd_line)
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back|show_shaped_types")])
    return keyboard


def get_avaliable_shaped_pictures(shaped_ball_type=None, shaped_ball_subtype=None):
    pictures_paths, pictures_names = get_shaped_pictures_from_DB(shaped_ball_type, shaped_ball_subtype)
    keyboard = []
    kbrd_line = []
    kbrd_line_length = 2
    picture_counter = 1
    for i in range(len(pictures_paths)):
        kbrd_line.append(InlineKeyboardButton(
            f"{shaped_ball_subtype} {picture_counter}",
            callback_data="[" + shaped_ball_type + "]=[" + shaped_ball_subtype + "]=[" + pictures_names[i] + "]"))
        # callback_data=pictures_paths[i]))  # TODO: Пути к картинкам делают клавиатуру невалидной
        picture_counter += 1
        if len(kbrd_line) == kbrd_line_length:
            keyboard.append(kbrd_line)
            kbrd_line = []
    if len(kbrd_line) != 0:
        keyboard.append(kbrd_line)
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back|show_shaped_subtypes")])
    return keyboard, pictures_paths


keyboard_dict = {
    "start": {
        "keyboard": [
            [
                InlineKeyboardButton("Купить", callback_data="our_balls"),
                InlineKeyboardButton("Надуть", callback_data="own_balls"),
            ]
        ],
        "text": "Привет, я Baloobot. Мы продаем самые дешевые шарики в Москве.\n\nЗдесь Вы можете приобрести наши шарики или надуть Ваши собственные"
    },
    "show_our_balls": {
        "keyboard": [
            [
                InlineKeyboardButton("Обычные", callback_data="our_balls_common"),
                InlineKeyboardButton("Фигурные", callback_data="our_balls_shaped"),
            ],
            [InlineKeyboardButton("Назад", callback_data="back|start")]
        ],
        "text": "У нас в наличии два вида шариков: обыкновенные и фигурные"
    },
    "show_own_balls": {
        "keyboard": [
            [InlineKeyboardButton("Назад", callback_data="back|start")]
        ],
        "text": "Тут вы можете надуть свои шарики нашим гелием\n Введите количестов шариков ниже:"
    },
    "show_common_types": {
        "keyboard": get_avalible_common_types(),
        "text": "Выберите вариант надписи на шарике"
    },
    "show_common_materials": {
        "keyboard": get_avalible_common_materials(),
        "text": "Выберите материал для шарика"
    },
    "show_common_colors": {
        "keyboard": get_avalible_common_colors_and_amount(),
        "text": "Выберите цвет с учетом остатка товаров"
    },
    "show_shaped_types": {
        "keyboard": get_avaliable_shaped_types(),
        "text": "вот фигурные шарики"
    },
    "show_shaped_subtypes": {
        "keyboard": get_avaliable_shaped_subtypes(),
        "text": "Выберите материал для шарика"
    },
    "show_shaped_pictures": {
        "keyboard": get_avaliable_shaped_pictures(),
        "text": "Выберите материал для шарика"
    },
}


async def show_own_balls(query, context: ContextTypes.DEFAULT_TYPE):
    keyboard_level = "show_own_balls"
    context.user_data['order_type'] = "own_balls"
    await query.edit_message_text(keyboard_dict[keyboard_level]['text'],
                                   reply_markup=InlineKeyboardMarkup(keyboard_dict[keyboard_level]['keyboard']))


def update_common_colors_keyboard(type: str, material: str):
    keyboard_dict['show_common_colors']['keyboard'], _ = get_avalible_common_colors_and_amount(type, material)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard_level = "start"
    await update.message.reply_text(
        keyboard_dict[keyboard_level]['text'],
        reply_markup=InlineKeyboardMarkup(keyboard_dict[keyboard_level]['keyboard']))


def gen_cart_msg(common_orders=None, shaped_orders=None, own_orders=None):
    all_orders = ""
    if common_orders:
        for i in range(len(common_orders)):
            all_orders += (f"\t\t\[{i+1}] -- заказано {common_orders[i][4]} шт., "
                           f"итоговая стоимость - {common_orders[i][5] * common_orders[i][4]} ₽\n")
    if shaped_orders:
        for i in range(len(shaped_orders)):
            all_orders += (f"\t\t\[{i + len(common_orders) + 1}] -- заказано {shaped_orders[i][3]} шт., "
                           f"итоговая стоимость - {shaped_orders[i][4] * shaped_orders[i][3]} ₽\n")

    if own_orders:
        all_orders += f"\n\t\tСвоих шариков заказано: {own_orders[0][0]} шт."

    return str(all_orders)


async def cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nickname = update.effective_user.name
    dict_of_nicks = dict(get_id_and_nicknames_from_DB())
    if nickname not in dict_of_nicks.keys():
        text = "Вы еще ничего не заказали"
    else:
        ordered_common_balls_info = get_ordered_common_balls_from_DB(dict_of_nicks[nickname])
        ordered_shaped_balls_info = get_ordered_shaped_balls_from_DB(dict_of_nicks[nickname])

        common_pictures_paths = [i[3] for i in ordered_common_balls_info]
        for i in range(len(common_pictures_paths)):
            common_pictures_paths[i] = gen_picture_path(common_pictures_paths[i], balloon_type="common")
        shaped_pictures_paths = [i[2] for i in ordered_shaped_balls_info]
        for i in range(len(shaped_pictures_paths)):
            shaped_pictures_paths[i] = gen_picture_path(shaped_pictures_paths[i], balloon_type="shaped")

        pictures_paths = common_pictures_paths + shaped_pictures_paths
        chat_id = update.effective_chat.id
        i = 1
        list_of_media = []
        media_per_msg = []
        for path in pictures_paths:
            trash_path = add_sign_to_picture_and_save_to_trash(path, "[" + str(i) + "]")
            with open(trash_path, 'rb') as file:
                media_per_msg.append(InputMediaPhoto(file))
                i += 1
            if i % 10 == 0:
                list_of_media.append(media_per_msg)
                media_per_msg = []
        if i % 10 != 0:
            list_of_media.append(media_per_msg)
            media_per_msg = []

        for msg in list_of_media:
            await context.bot.send_media_group(chat_id, msg)
        path_to_trash_dir = remove_last_segment_in_path(trash_path)
        trash_files_names = os.listdir(path_to_trash_dir)
        for file_name in trash_files_names:
            os.remove(os.path.join(path_to_trash_dir, file_name))

        ordered_own_balls_info = get_own_shaped_balls_from_DB(dict_of_nicks[nickname])
        text = gen_cart_msg(ordered_common_balls_info, ordered_shaped_balls_info, ordered_own_balls_info)

    await update.message.reply_text('''\U0001F388 Ваша корзина:\n\n_Если в сообщении выше не видно номеров на картинках, откройте их, пожалуйста, по одной и убедитесь в правильности бронирования_\n\n'''
                                    + text, parse_mode="Markdown")



async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "100500 ₽"  # TODO: handle in BD
    await update.message.reply_text(text)


async def show_our_balls(query):
    keyboard_level = "show_our_balls"
    await query.edit_message_text(keyboard_dict[keyboard_level]['text'],
                                  reply_markup=InlineKeyboardMarkup(keyboard_dict[keyboard_level]['keyboard']))


async def show_common_types(query, context: ContextTypes.DEFAULT_TYPE):
    keyboard = get_avalible_common_types()
    text = "Выберите вариант надписи на шарике"
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['shape'] = 'common'
    await query.edit_message_text(text, reply_markup=reply_markup)


async def show_common_materials(query, context: ContextTypes.DEFAULT_TYPE):
    keyboard = get_avalible_common_materials(query.data.strip())
    text = "Выберите материал для шарика"
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['type'] = query.data.strip()
    await query.edit_message_text(text, reply_markup=reply_markup)


async def show_common_colors_and_amount(query, context: ContextTypes.DEFAULT_TYPE):
    keyboard, price = get_avalible_common_colors_and_amount(context.user_data['type'], query.data.strip())
    text = "Выберите цвет с учетом остатка товаров. Цена: " + str(price) + " руб."
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['material'] = query.data.strip()
    await query.edit_message_text(text, reply_markup=reply_markup)


async def show_common_pictures(update, query, context: ContextTypes.DEFAULT_TYPE):
    keyboard, pictures_paths = get_avaliable_common_pictures(context.user_data['type'], context.user_data['material'],
                                                             query.data.strip())
    text = "Выберите изображение шарика по картинке, нажав соответствующую кнопку:"

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['color'] = query.data.strip()
    chat_id = update.effective_chat.id
    i = 1
    L = []
    for path in pictures_paths:
        trash_path = add_sign_to_picture_and_save_to_trash(path, "[" + str(i) + "]")
        with open(trash_path, 'rb') as file:
            L.append(InputMediaPhoto(file))
            i += 1
    await context.bot.send_media_group(chat_id, L)
    path_to_trash_dir = remove_last_segment_in_path(trash_path)
    trash_files_names = os.listdir(path_to_trash_dir)
    for file_name in trash_files_names:
        os.remove(os.path.join(path_to_trash_dir, file_name))
    await context.bot.send_message(chat_id, text, reply_markup=reply_markup)


async def ask_common_ball_amount(query, picture_name, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['picture_name'] = picture_name
    await query.message.reply_text("Введите количество шариков:")


async def ask_shaped_ball_amount(query, picture_name, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['picture_name'] = picture_name
    await query.message.reply_text("Введите количество шариков:")


async def show_shaped_types(query, context: ContextTypes.DEFAULT_TYPE):
    keyboard = get_avaliable_shaped_types()
    text = "Выберите одну из форм шарика"
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['shape'] = 'shaped'
    await query.edit_message_text(text, reply_markup=reply_markup)


async def show_shaped_subtypes(query, context: ContextTypes.DEFAULT_TYPE):
    keyboard = get_avaliable_shaped_subtypes(query.data.strip())
    text = "Уточните вид шарика из предложенных подвидов выбранного ранее типа:"
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['type'] = query.data.strip()
    await query.edit_message_text(text, reply_markup=reply_markup)


async def show_shaped_pictures(update, query, context: ContextTypes.DEFAULT_TYPE):
    keyboard, pictures_paths = get_avaliable_shaped_pictures(context.user_data['type'], query.data.strip())
    text = "Выберите изображение шарика по картинке, нажав соответствующую кнопку:"
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['subtype'] = query.data.strip()
    chat_id = update.effective_chat.id
    i = 1
    L = []
    for path in pictures_paths:
        trash_path = add_sign_to_picture_and_save_to_trash(path, "[" + str(i) + "]")
        with open(trash_path, 'rb') as file:
            L.append(InputMediaPhoto(file))
            i += 1
    await context.bot.send_media_group(chat_id, L)
    path_to_trash_dir = remove_last_segment_in_path(trash_path)
    trash_files_names = os.listdir(path_to_trash_dir)
    for file_name in trash_files_names:
        os.remove(os.path.join(path_to_trash_dir, file_name))
    await context.bot.send_message(chat_id, text, reply_markup=reply_markup)


async def back(query, context):
    keyboard_level = query.data.split("|")[1]
    if keyboard_level == "show_common_materials":
        keyboard_dict[keyboard_level]["keyboard"] = get_avalible_common_materials(context.user_data['type'])
    if keyboard_level == "show_common_colors":
        keyboard_dict[keyboard_level]["keyboard"] = get_avalible_common_colors_and_amount(context.user_data['type'],
                                                                                          context.user_data['material'])[0]
    if keyboard_level == "show_shaped_subtypes":
        keyboard_dict[keyboard_level]["keyboard"] = get_avaliable_shaped_subtypes(context.user_data['type'])

    await query.edit_message_text(keyboard_dict[keyboard_level]['text'],
                                  reply_markup=InlineKeyboardMarkup(keyboard_dict[keyboard_level]['keyboard']))


#TODO:
# 1. заказы одного типа шариков на разные адреса
# 2. суммирование заказов одного шарика на один адрес (common)
async def notes_registrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'shape' in context.user_data.keys() and context.user_data['shape'] == 'common':
        if 'color' not in context.user_data.keys() \
                or 'material' not in context.user_data.keys() \
                or 'type' not in context.user_data.keys() \
                or 'picture_name' not in context.user_data.keys() \
                or 'amount' not in context.user_data.keys():
            return
        color = context.user_data['color']
        material = context.user_data['material']
        type = context.user_data['type']
        picture = context.user_data['picture_name']
        amount = context.user_data['amount']
        curr_amount = get_amount_of_common_balls(type, material, color, picture)
        nickname = update.effective_user.name
        note = update.message.text
        complete_common_order(type, material, color, picture, amount, curr_amount, nickname, note)

    elif 'shape' in context.user_data.keys() and context.user_data['shape'] == 'shaped':
        if 'type' not in context.user_data.keys() \
                or 'subtype' not in context.user_data.keys() \
                or 'picture_name' not in context.user_data.keys() \
                or 'amount' not in context.user_data.keys():
            return
        type = context.user_data['type']
        subtype = context.user_data['subtype']
        picture_name = context.user_data['picture_name']
        amount = context.user_data['amount']
        curr_amount = get_amount_of_shaped_balls(type, subtype, picture_name)
        nickname = update.effective_user.name
        note = update.message.text
        complete_shaped_order(type, subtype, picture_name, amount, curr_amount, nickname, note)
    elif 'order_type' in context.user_data.keys() and context.user_data['order_type'] == 'own_balls':
        if 'amount' not in context.user_data.keys():
            return
        amount = context.user_data['amount']
        nickname = update.effective_user.name
        note = update.message.text
        complete_blowing_order(amount, nickname, note)
    await update.effective_message.reply_text(f"Ваш адрес успешно принят. Вы заказали доставку {context.user_data['amount']} шариков")
    context.user_data.clear()


async def order_registrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = int(update.message.text)
    if context.user_data:
        if 'shape' in context.user_data.keys() and context.user_data['shape'] == 'common':
            if 'color' not in context.user_data.keys() \
                    or 'material' not in context.user_data.keys() \
                    or 'type' not in context.user_data.keys() \
                    or 'picture_name' not in context.user_data.keys():
                return
            color = context.user_data['color']
            material = context.user_data['material']
            type = context.user_data['type']
            picture = context.user_data['picture_name']
            curr_amount = get_amount_of_common_balls(type, material, color, picture)
            if curr_amount < int(amount):
                await update.message.reply_text(f"Количество шариков в заказе превышает количество шариков в наличии. "
                                                f"Введите новое значение (в наличии шариков цвета {color} {curr_amount} шт.)")
                return
            else:
                if amount == 0:  # не может быть меньше нуля из-за регулярки
                    await update.effective_message.reply_text(
                        f"Нельзя делать заявки на 0 шариков. Введите новое количество шариков")
                    return
        elif 'shape' in context.user_data.keys() and context.user_data['shape'] == 'shaped':
            if 'type' not in context.user_data.keys() \
                            or 'subtype' not in context.user_data.keys() \
                            or 'picture_name' not in context.user_data.keys():
                        return
            type = context.user_data['type']
            subtype = context.user_data['subtype']
            picture_name = context.user_data['picture_name']
            curr_amount = get_amount_of_shaped_balls(type, subtype, picture_name)
            if curr_amount < int(amount):
                await update.message.reply_text(f"Количество шариков в заказе превышает количество шариков в наличии. "
                                                f"Введите новое значение (в наличии выбранных Вами шариков {curr_amount} шт.)")
                return
            else:
                if amount == 0:  # не может быть меньше нуля из-за регулярки
                    await update.effective_message.reply_text(
                        f"Нельзя делать заявки на 0 шариков. Введите новое количество шариков")
                    return
        elif 'order_type' in context.user_data.keys() and context.user_data['order_type'] == 'own_balls':
            if amount == 0:
                await update.effective_message.reply_text(
                    f"Нельзя делать заявки на 0 шариков. Введите новое количество шариков")
                return
    context.user_data["amount"] = amount
    await update.effective_message.reply_text(f"Ваша заявка на {amount} шарик(-ов, -a) сформирована. Для завершения оформления заказа впишите адрес, на который требуется доставка.")




# async def order_registrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     amount = int(update.message.text)
#     nickname = update.effective_user.name
#     if 'shape' in context.user_data.keys() and context.user_data['shape'] == 'common':
#         if 'color' not in context.user_data.keys() \
#                 or 'material' not in context.user_data.keys() \
#                 or 'type' not in context.user_data.keys() \
#                 or 'picture_name' not in context.user_data.keys():
#             return
#         color = context.user_data['color']
#         material = context.user_data['material']
#         type = context.user_data['type']
#         picture = context.user_data['picture_name']
#         curr_amount = get_amount_of_common_balls(type, material, color, picture)
#         if curr_amount < int(amount):
#             await update.message.reply_text(f"Количество шариков в заказе превышает количество шариков в наличии. "
#                                             f"Введите новое значение (в наличии шариков цвета {color} {curr_amount} шт.)")
#             return
#         else:
#             if amount <= 0:
#                 await update.effective_message.reply_text(f"Нельзя делать заявки на 0 шариков. Введите новое количество шариков")
#                 return
#             # complete_order(type, material, color, picture, amount, curr_amount, nickname)
#             # update_common_colors_keyboard(type, material)
#             await update.effective_message.reply_text(f"Ваша заявка на {amount} шарик(-ов, -а) принята",
#                                                     reply_markup=InlineKeyboardMarkup(
#                                                         keyboard_dict['start']['keyboard']))
#
#
#     elif 'shape' in context.user_data.keys() and context.user_data['shape'] == 'shaped':
#         if 'type' not in context.user_data.keys() \
#                 or 'subtype' not in context.user_data.keys() \
#                 or 'picture_name' not in context.user_data.keys():
#             return
#         type = context.user_data['type']
#         subtype = context.user_data['subtype']
#         picture_name = context.user_data['picture_name']
#         curr_amount = get_amount_of_shaped_balls(type, subtype, picture_name)
#         if curr_amount < int(amount):
#             await update.message.reply_text(f"Количество шариков в заказе превышает количество шариков в наличии. "
#                                             f"Введите новое значение (в наличии выбранных Вами шариков {curr_amount} шт.)")
#             return
#         else:
#
#             if amount <= 0:
#                 await update.effective_message.reply_text(
#                     f"Нельзя делать заявки на 0 шариков. Введите новое количество шариков")
#                 return
#             # complete_shaped_order(type, subtype, picture_name, amount, curr_amount, nickname)
#             await update.effective_message.reply_text(f"Ваша заявка на {amount} шарик(-ов, -а) принята",
#                                                       reply_markup=InlineKeyboardMarkup(
#                                                           keyboard_dict['start']['keyboard']))
#
#
#     elif 'order_type' in context.user_data.keys() and context.user_data['order_type'] == 'own_balls':
#
#         if amount <= 0:
#             await update.effective_message.reply_text(
#                 f"Нельзя делать заявки на 0 шариков. Введите новое количество шариков")
#             return
#         # complete_blowing_order(amount, nickname)
#         await update.effective_message.reply_text(f"Ваша заявка на {amount} шарик(-ов, -a) принята",
#                                                   reply_markup=InlineKeyboardMarkup(
#                                                       keyboard_dict['start']['keyboard']))
#     # context.user_data.clear()