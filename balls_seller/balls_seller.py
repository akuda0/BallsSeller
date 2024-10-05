from keyboard_handlers.handlers import *
from db_handlers.handlers import *
from third_party.ops import *

# TODO: 1) добавить кнопки "В начало" во все клавиатуры
#       2) Удалить картинку из shaped, когда их уже 0 на складе



async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    await query.answer()
    if query.data == 'our_balls':
        await show_our_balls(query)

    elif query.data.startswith("back|"):
        await back(query, context)

    elif query.data == 'own_balls':
        await show_own_balls(query, context)

    elif query.data == "our_balls_common":
        await show_common_types(query, context)

    elif query.data == "our_balls_shaped":
        await show_shaped_types(query, context)

    elif context.user_data['shape'] == 'shaped' and query.data in get_shaped_types_from_DB():
        await show_shaped_subtypes(query, context)

    elif context.user_data['shape'] == 'shaped' and query.data in get_shaped_subtypes_from_DB(context.user_data['type']) :
        await show_shaped_pictures(update, query, context)

    elif context.user_data['shape'] == 'common' and query.data in get_common_types_from_DB():
        await show_common_materials(query, context)

    elif context.user_data['shape'] == 'common' and query.data in get_common_materials_from_DB(context.user_data['type']):
        await show_common_colors_and_amount(query, context)

    elif context.user_data['shape'] == 'common' and query.data in get_common_colors_from_DB():  #  "yellow|common"   "yellow|circle"
        await show_common_pictures(update, query, context)

    elif context.user_data['shape'] == 'common' and parse_pic_name_from_query_data(query.data, "common") in \
          get_common_pictures_from_DB(context.user_data["type"], context.user_data["material"], context.user_data["color"])[1]:
        await ask_common_ball_amount(query, parse_pic_name_from_query_data(query.data, "common"), context)

    elif context.user_data['shape'] == 'shaped' and parse_pic_name_from_query_data(query.data, "shaped") in \
          get_shaped_pictures_from_DB(context.user_data["type"], context.user_data["subtype"])[1]:
        await ask_shaped_ball_amount(query, parse_pic_name_from_query_data(query.data, "shaped"), context)


def main():
    application = Application.builder().token("6619622284:AAGBuuwM9P4i8Duc41bWTKDl7PWXRFWYBew").build()
    application.add_handler(CommandHandler(["start"], start))
    application.add_handler(CommandHandler(["cart"], cart))
    application.add_handler(CommandHandler(["orders"], orders))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.Regex("^\d+$"), order_registrar)) # MessageHandler(filters.Regex("^(Boy|Girl|Other)$")
    application.add_handler(MessageHandler(filters.TEXT, notes_registrar)) # MessageHandler(filters.Regex("^(Boy|Girl|Other)$")

    application.run_polling()
    application.start()



if __name__ == "__main__":
    main()
