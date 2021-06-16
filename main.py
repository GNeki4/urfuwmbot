import logging
import dataset as ds
import addition

from gsheet import MySheet
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

logger = logging.getLogger(__name__)

hours = "10:00 11:00 12:00"
sheet = MySheet(hours_string=hours, amount_of_days=4,
                amount_of_washing_machines=3, time_to_wait=1)

REGISTRATION, ROOM, CHECK_NAME, CHECK_ROOM, END_OF_REGISTER, \
MAIN_MENU, MAKE_NOTE, CHOOSE_NOTE, MAKE_NOTE_2, CHECK_NOTE, END_NOTE,\
DELETE_DATA, NOTIFY, NOTIFY_SPECIFIC, NOTIFY_ALL, NOT_DONE, NOTIFY_SPECIFIC_2, NOTIFY_ALL_2 = range(18)


def start(update, context):
    try:
        user_ds = ds.get_user_info(update.message.from_user.id)

        if user_ds['realname'] == '' and user_ds['room'] == -1:
            reply_keyboard = [['Регистрация']]
            user_name = update.message.from_user.first_name
            text = f'Привет, {user_name}!\n' \
                   f'С моей помощью ты сможешь занять очередь в прачечную комнату, но для начала нужно зарегистрироваться.\n' \
                   f'Нажми на кнопку Регистрация.'

            update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                             one_time_keyboard=True))

            return REGISTRATION

        elif user_ds['realname'] != '' and user_ds['room'] == -1:
            reply_keyboard = [['В начало']]

            text = f'Привет, {user_ds["realname"]}!\n' \
                   f'Мы не закончили регистрацию. Пришли номер комнаты, в которой ты живешь.\n' \
                   f'Пример: 311'
            update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                             one_time_keyboard=True))

            return CHECK_ROOM

        elif user_ds['realname'] != '' and user_ds['room'] != -1 and user_ds['is_admin'] == 0:
            reply_keyboard = [['Занять очередь', 'Отменить запись', 'Мой профиль']]
            text = 'Главное меню:'
            update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                         one_time_keyboard=True))

            return MAIN_MENU
        elif user_ds['realname'] != '' and user_ds['room'] != -1 and user_ds['is_admin'] == 1:
            reply_keyboard = [['Занять очередь', 'Отменить запись', 'Мой профиль', 'Отправить уведомление']]
            text = 'Главное меню:'
            update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                         one_time_keyboard=True))

            return MAIN_MENU
    except:
        ds.add_user(update.message.from_user.id, update.message.from_user.first_name, '', -1, 1)

    reply_keyboard = [['Регистрация']]
    user_name = update.message.from_user.first_name
    text = f'Привет, {user_name}!\n' \
           f' С моей помощью ты сможешь занять очередь в прачечную комнату, но для начала нужно зарегистрироваться.\n' \
           f'Нажми на кнопку Регистрация.'

    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))

    return REGISTRATION


def register(update, context):
    reply_keyboard = [['В начало']]
    user = update.message.from_user
    text = 'Введите свою фамилию с инициалами.\n' \
           'Пример: Иванов И.И.'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))
    return CHECK_NAME


def check_name(update, context):
    reply_keyboard = [['Да, все верно', 'В начало']]
    user_name = update.message.text

    ds.update_user_realname(update.message.from_user.id, user_name)

    text = f'Ты уверен что написал свое имя правильно?\n' \
           f'Тебя зовут: "{user_name}"?\n' \
           f'Если да, ответь "Да все верно".\n' \
           f'Если нет, просто введи имя снова.'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))

    return ROOM


def room(update, context):
    reply_keyboard = [['В начало']]
    user_ds = ds.get_user_info(update.message.from_user.id)

    text = f'Отлично, {user_ds["realname"]}!\n' \
           f'Теперь пришли номер комнаты, в которой ты живешь.\n' \
           f'Пример: 311'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))

    return CHECK_ROOM


def check_room(update, context):
    reply_keyboard = [['Да, все верно', 'В начало']]
    user_room = update.message.text

    ds.update_user_room(update.message.from_user.id, user_room)

    text = f'Ты уверен что написал свою комнату правильно?\n' \
           f'Твоя комната: "{user_room}"?\n' \
           f'Если да, ответь "Да, все верно".\n' \
           f'Если нет, просто введи комнату снова.'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))

    return END_OF_REGISTER


def end_of_register(update, context):
    reply_keyboard = [['В главное меню']]
    text = 'Готово!\n' \
           'В дальнейшем ты сможешь изменить данные в личном кабинете.'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))

    return MAIN_MENU


def main_menu(update, context):
    if ds.get_user_info(update.message.from_user.id)['is_admin'] == 1:
        reply_keyboard = [['Занять очередь', 'Отменить запись', 'Мой профиль', 'Отправить уведомление']]
    else:
        reply_keyboard = [['Занять очередь', 'Отменить запись', 'Мой профиль']]

    text = 'Главное меню:'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))
    return MAIN_MENU


def send_notification(update, context):
    if ds.get_user_info(update.message.from_user.id)['is_admin'] == 0: # not admin
        reply_keyboard = [['Занять очередь', 'Отменить запись', 'Мой профиль']]
        text = 'Вы не являетесь администратором.'
        update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))
        return MAIN_MENU
    else:
        reply_keyboard = [['Конкретным пользователям', 'Всем пользователям', 'В главное меню']]
        text = 'Выбери, кому хочешь отправить уведомление:'
        update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))
        return NOTIFY


def to_all_users(update, context):
    reply_keyboard = [['В главное меню']]
    text = 'Напиши одно сообщение, которое мы отправим всем пользователям бота.'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                 one_time_keyboard=True))
    return NOTIFY_ALL


def notify_all_confirm(update, context):
    ##########__MAGICK__##########
    msg = update.message.text
    context.user_data["msg"] = msg
    ##########__MAGICK__##########

    reply_keyboard = [['В главное меню']]

    try:
        addition.send_announcments_to_all(msg)
        text = f"Сообщение: '{context.user_data['msg']}' отправлено всем пользователям."
    except:
        text = "Что-то пошло не так!"

    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                 one_time_keyboard=True))

    return MAIN_MENU


def to_specific_users(update, context):
    reply_keyboard = [['В главное меню']]
    text = 'Напиши фамилии с инициалами (как они записаны в таблице) тех пользователей, кому хочешь передать сообщение.\n' \
           'Каждое имя с новой строки.\n' \
           'Пример:\n' \
           'Иванов И.И.\n' \
           'Петров П.П.'

    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                 one_time_keyboard=True))
    return NOTIFY_SPECIFIC


def notify_specific_stage_username(update, context):
    ##########__MAGICK__##########
    names = update.message.text
    context.user_data["names"] = names
    ##########__MAGICK__##########

    reply_keyboard = [['В главное меню']]
    text = 'Напиши одно сообщение, которое мы отправим следующим пользователям:\n' \
           f'{context.user_data["names"]}'

    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                 one_time_keyboard=True))
    return NOTIFY_SPECIFIC_2


def notify_specific_confirm(update, context):
    ##########__MAGICK__##########
    msg = update.message.text
    context.user_data["msg"] = msg
    ##########__MAGICK__##########

    try:
        addition.send_announcments_to_specific(context.user_data["names"], context.user_data["msg"])
        text = f"Сообщение: '{context.user_data['msg']}'\n" \
           f"Отправлено пользователям:\n" \
           f"{context.user_data['names']}"
    except:
        text = "Что-то пошло не так!"

    reply_keyboard = [['В главное меню']]
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                 one_time_keyboard=True))
    return MAIN_MENU


def undo_note(update, context):
    reply_keyboard = [['В главное меню']]
    text = 'Вы никуда не записаны.'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))
    return MAIN_MENU


def make_note_1(update, context):
    reply_keyboard = [['Прачечная', 'В главное меню']]
    text = 'Выбери, куда хочешь занять очередь:'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))
    return CHOOSE_NOTE


def make_note_2(update, context):
    reply_keyboard = [['Посмотреть таблицу', 'Заполнить заявку', 'В главное меню']]
    text = 'Чтобы записаться:\n' \
           '1. Откройте с помощью меню таблицу, ' \
           'чтобы посмотреть свободное время для записи и наличие свободных машинок.\n' \
           '2. Выберите время и количество свободных машинок.\n' \
           '3. Нажмите "Заполнить заявку" и введите данные.'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))
    return MAKE_NOTE


def make_note_3(update, context):
    reply_keyboard = [['В главное меню']]
    text = 'В заявке укажи:\n' \
           '1. Количество машинок\n' \
           '2. День (ДД.ММ)\n' \
           '3. Время (ЧЧ:ММ)\n' \
           'Каждое значение в новой строке.\n' \
           'Соблюдай формат данных.\n' \
           'Отправь ОДНО сообщение.\n' \
           'Пример заявки:\n2\n14.05\n10:00'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))

    return CHECK_NOTE


def check_note(update, context):
    ##########__MAGICK__##########
    msg = update.message.text
    context.user_data["sign_data"] = msg
    ##########__MAGICK__##########

    reply_keyboard = [['Да, все верно', 'В главное меню']]
    user_time = update.message.text

    text = f'Ты уверен что написал время правильно?\n' \
           f'{user_time}\n' \
           f'Если да, ответь "Да, все верно".\n' \
           f'Если нет, просто введи время снова.'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))

    return END_NOTE


def note_result(update, context):
    result = sheet.register(context.user_data["sign_data"], ds.get_user_info(update.message.from_user.id)["realname"])

    if result == "True":
        text = 'Готово!'
    else:
        text = result

    reply_keyboard = [['В главное меню']]
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))
    return MAIN_MENU


def give_table_url(update, context):
    reply_keyboard = [['Посмотреть таблицу', 'Заполнить заявку', 'В главное меню']]
    text = 'https://docs.google.com/spreadsheets/d/1IQOeMlwpEYU95hyyrIQ09vJiyWaNu1ndFKjuybeT74Q/edit?usp=sharing'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))
    return MAKE_NOTE


def my_profile(update, context):
    reply_keyboard = [['Удалить профиль', 'В главное меню']]
    user_ds = ds.get_user_info(update.message.from_user.id)
    text = f'Имя: {user_ds["realname"]}\n' \
           f'Комната: {user_ds["room"]}'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))
    return MAIN_MENU


def delete_data_question(update, context):
    reply_keyboard = [['Да', 'Мой профиль', 'В главное меню']]
    text = 'Вы точно хотите изменить свое имя и комнату?\n' \
           'Для этого вам придется пройти регистрацию снова.\n' \
           'Если же вы хотите удалить свой профиль, просто не проходите регистрацию заново.\n' \
           'Вы точно уверены в своем решении?'

    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))

    return DELETE_DATA


def delete_data_complete(update, context):
    text = 'Ваши данные были удалены.\n' \
           'Чтобы начать регистрацию заново, нажмите /start'
    ds.delete_user_info(update.message.from_user.id)
    update.message.reply_text(text)

    return REGISTRATION


def not_done(update, context):
    reply_keyboard = [['В главное меню']]
    text = 'Этот метод не сделан.'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))

    return NOT_DONE


def main():
    updater = Updater("859875977:AAEwxEpOtglH0-tvwI-xmJc_2BmrNnEbmPE", use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.text, start),
        ],
        states={
            REGISTRATION: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(Регистрация)$'), register)],

            MAIN_MENU: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(Мой профиль)$'), my_profile),
                MessageHandler(Filters.regex('^(Удалить профиль)$'), delete_data_question),
                MessageHandler(Filters.regex('^(В главное меню)$'), main_menu),
                MessageHandler(Filters.regex('^(Занять очередь)$'), make_note_1),
                MessageHandler(Filters.regex('^(Отменить запись)$'), undo_note),
                MessageHandler(Filters.regex('^(Отправить уведомление)$'), send_notification)],

            NOT_DONE: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(В главное меню)$'), main_menu),],

            ROOM: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(Да, все верно)$'), room),
                MessageHandler(Filters.regex('^(В начало)$'), start),
                MessageHandler(Filters.text, check_name)],

            CHECK_NAME: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(В начало)$'), start),
                MessageHandler(Filters.text, check_name)],

            CHECK_ROOM: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(В начало)$'), start),
                MessageHandler(Filters.text, check_room)],

            END_OF_REGISTER: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(Да, все верно)$'), end_of_register),
                MessageHandler(Filters.regex('^(В начало)$'), start),
                MessageHandler(Filters.text, check_room)],

            MAKE_NOTE: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(Посмотреть таблицу)$'), give_table_url),
                MessageHandler(Filters.regex('^(Заполнить заявку)$'), make_note_3),
                MessageHandler(Filters.regex('^(В главное меню)$'), main_menu)],

            MAKE_NOTE_2: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(Да, все верно)$'), note_result),
                MessageHandler(Filters.regex('^(В главное меню)$'), main_menu),
                MessageHandler(Filters.text, check_note)],

            CHOOSE_NOTE: [
                MessageHandler(Filters.regex('^(Прачечная)$'), make_note_2),
                MessageHandler(Filters.regex('^(В главное меню)$'), main_menu)],

            CHECK_NOTE: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(В главное меню)$'), main_menu),
                MessageHandler(Filters.text, check_note)],

            END_NOTE: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(В главное меню)$'), main_menu),
                MessageHandler(Filters.regex('^(Да, все верно)$'), note_result),
                MessageHandler(Filters.regex('^(В начало)$'), start),
                MessageHandler(Filters.text, check_note)],

            DELETE_DATA: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(Да)$'), delete_data_complete),
                MessageHandler(Filters.regex('^(Мой профиль)$'), my_profile),
                MessageHandler(Filters.regex('^(В главное меню)$'), main_menu),],

            NOTIFY: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(Конкретным пользователям)$'), to_specific_users),
                MessageHandler(Filters.regex('^(Всем пользователям)$'), to_all_users),
                MessageHandler(Filters.regex('^(В главное меню)$'), main_menu),],

            NOTIFY_SPECIFIC: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(В главное меню)$'), main_menu),
                MessageHandler(Filters.text, notify_specific_stage_username),],

            NOTIFY_SPECIFIC_2: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(В главное меню)$'), main_menu),
                MessageHandler(Filters.text, notify_specific_confirm),],

            NOTIFY_ALL: [
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(В главное меню)$'), main_menu),
                MessageHandler(Filters.text, notify_all_confirm),],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
