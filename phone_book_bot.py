from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
import sqlite3

# conn = sqlite3.connect('phonebook.db')
# cursor = conn.cursor()


bot_token = '5718269028:AAGqKrvYv5WFM_B_KpxUOGET187cpw-c6YA'
bot = Bot(bot_token)
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(update.effective_chat.id, f"Выберите действие:\n" 
                            f"Открыть всю телефонную книгу /open \n"
                            f"Выбрать человека по фамилии /select_person\n"
                            f"Удалить запись /del_write\n"
                            f"Добавить запись /add_write\n")


def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def open(update, context):
    conn = sqlite3.connect('phonebook.db')  
    cursor = conn.cursor()
    cursor.execute("select * from phonebook")  
    results = cursor.fetchall()
    context.bot.send_message(update.effective_chat.id,
                             f"{results}")

def select_person(update, context):
    context.bot.send_message(update.effective_chat.id,
                             f"Введите фамилию: \n Для выхода напишите /stop")
    return 1


def select_person_out(update, context):
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    text = update.message.text  
    cursor.execute(
        f"select * from phonebook where surname like '%{text}%'")
    results = cursor.fetchall()
    update.message.reply_text(f"{results}")


select_person_handler = ConversationHandler(
        entry_points=[CommandHandler('select_person', select_person)],

    # Состояние внутри диалога.
    states={
        # обработка запроса 
        1: [MessageHandler(Filters.text & ~Filters.command, select_person_out)],
    },

    # Точка прерывания диалога
    fallbacks=[CommandHandler('stop', stop)]
)


def del_write(update, context):
    context.bot.send_message(
        update.effective_chat.id, f"Введите номер строки для удаления: \n Для выхода напишите /stop")
    return 1

def del_write_out(update, context):
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    text = update.message.text  
    cursor.execute(
        f"delete from phonebook where id={text}")
    conn.commit()
    update.message.reply_text(f"Строка удалена")


del_write_handler = ConversationHandler(
    # входная точка
    entry_points=[CommandHandler('del_write', del_write)],

    # Состояние внутри диалога.
    states={
        # обработка запроса 
        1: [MessageHandler(Filters.text & ~Filters.command, del_write_out)],
    },

    # Точка прерывания диалога
    fallbacks=[CommandHandler('stop', stop)]
)

def add_write(update, context):
    context.bot.send_message(
        update.effective_chat.id, f"Введите новые данные: \n Для выхода напишите /stop")
    return 1


def add_write_out(update, context):
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    text = update.message.text  
    text = text.split() 
    cursor.execute(
        f"insert into phonebook (surname, name, patronymic, phone)"
        f"values ('{text[0]}', '{text[1]}', '{text[2]}', '{text[3]}', '{text[4]})')")
    conn.commit()
    update.message.reply_text(f"новая информация добавлена")


add_write_handler = ConversationHandler(
    # попадаем сюда при вводе в боте /add_write
    entry_points=[CommandHandler('add_write', add_write)],

    # Состояние внутри диалога.
    states={
        # обработка запроса 
        1: [MessageHandler(Filters.text & ~Filters.command, add_write_out)],
    },
    # Точка прерывания диалога.
    fallbacks=[CommandHandler('stop', stop)]
)


start_handler = CommandHandler('start', start)
open_handler = CommandHandler('open', open)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(open_handler)
dispatcher.add_handler(select_person_handler)    
dispatcher.add_handler(del_write_handler)    
dispatcher.add_handler(add_write_handler)
updater.start_polling()
updater.idle()