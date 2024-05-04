import telebot
from telebot import types
from services import add_task, get_tasks, get_user, add_user, del_task
from dbbbbb import get_connection, init_db

TOKEN = '7018776236:AAGZ52BqeT9fjbifMAjyhyjHml2EQnTghrQ'

bot = telebot.TeleBot(TOKEN)
init_db(get_connection())
db_connection = get_connection()


def inst(message):
    bot.send_message(message.chat.id, 'Добавление задачи:\n'
                                      'Для добавления новой задачи введите команду в формате "/add "задача"" '
                                      '(без кавычек и пробелов после команды add). Например: "/add Купить молоко".\n'
                                      'Просмотр списка задач:\n'
                                      'Для просмотра списка задач введите команду /tsk. '
                                      'Бот отправит вам список всех добавленных задач.\n'
                                      'Удаление задачи:\n'
                                      'Для удаления задачи введите команду в формате "/del номер задачи".'
                                      ' Например: "/del 3".')


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    inst(message)
    user = get_user(user_id=message.from_user.id, conn=db_connection)
    if not user:
        add_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            name=message.from_user.first_name,
            conn=db_connection
        )


@bot.message_handler()
def mes(message: types.Message):
    if message.text == '/tsk':
        if get_tasks(db_connection):
            tasks = get_tasks(db_connection)
            text = ''
            for task in tasks:
                text += ('-' * 20) + str(task[0]) + ('-' * 20) + '\n' + task[2] + '\n\n'
            bot.send_message(message.chat.id, text)
            inst(message)
        else:
            bot.send_message(message.chat.id, 'Список задач пуст')
    elif message.text.startswith('/add '):
        task = message.text.split('/add ')[-1]
        add_task(
             task=task,
             user_id=message.from_user.id,
             conn=db_connection
        )
        inst(message)
    elif message.text.startswith('/del '):
        task_id = message.text.split('/del ')[-1]
        del_task(
             task_id=int(task_id),
             conn=db_connection
        )
        inst(message)


bot.polling(none_stop=True)
