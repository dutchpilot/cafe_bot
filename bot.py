import config
import telebot
import requests
import os
import datetime

bot = telebot.TeleBot(config.TOKEN)
start_time = str(datetime.datetime.now())
print('MLK bot started at ' + start_time)

problem = 0
period = 1

if problem:
    problem_message = 'Остутствует доступ к серверу с данными.\n'
else:
    problem_message = ''

def get_exchange(key):
    query_params = {
        'key': config.API_KEY,
        'conv': key
    }
    URL = 'https://free.currconv.com/api/v7/convert?q={conv}&compact=ultra&apiKey={key}'.format(**query_params)
    response = requests.get(URL).json()
    # print(response)
    return '1 ' + key[:3] + ' = ' + str(response[key]) + ' RUB'


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Вас приветствует Мебельная фабрика "MLK"!\n' +
        '\n' +
        problem_message +
        'Для получения сведений по обедам за текущий месяц введите последние четыры цифры вашего штрихкода (последнюю четвертую цифру указывать не обязательно).\n' +
        'Заказы, введенные по ведомости, будут выгружаться с некоторым опозданием, так как вводятся вручную.\n' +
        '\n' +
        'Результат работы столовой за текущий день /total\n' +
        '\n' +
        'Курсы валют /exchange\n' +
        '\n' +
        'Для вызова справки нажмите /help\n' +
        '\n' +
        'Время последнего запуска бота: ' + start_time + '\n'
    )


@bot.message_handler(commands=['help', 'h'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    bot.send_message(
        message.chat.id,
        problem_message +
        '1) Для получения сведений по обедам за текущий месяц введите последние четыры цифры вашего штрихкода (последнюю четвертую цифру указывать не обязательно).\n' +
        'Заказы, введенные по ведомости, будут выгружаться с некоторым опозданием, так как вводятся вручную.\n' +
        '2) Результат работы столовой за текущий день /total\n' +
        '3) Курсы валют /exchange\n' +
        '4) Для вызова справки нажмите /help\n' +
        '\n' +
        'Время последнего запуска бота: ' + start_time + '\n',
        reply_markup=keyboard
    )


@bot.message_handler(commands=['stolovaya'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Текущий месяц', callback_data='CurrentMonth'),
        telebot.types.InlineKeyboardButton('Прошлый месяц', callback_data='PreviousMonth')
    )
    bot.send_message(
        message.chat.id,
        'Выберите период',
        reply_markup=keyboard
    )


@bot.message_handler(commands=['exchange'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('USD', callback_data='get-USD'),
        telebot.types.InlineKeyboardButton('EUR', callback_data='get-EUR')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('BTC', callback_data='get-BTC')
    )
    bot.send_message(
        message.chat.id,
        'Выберите валюту:',
        reply_markup=keyboard
    )

@bot.message_handler(commands=['total'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    mypath = config.PATH + 'total.txt'

    if os.path.exists(mypath):
        # try:
        info = open(mypath).read()
        if len(info) > 4096:
            for x in range(0, len(info), 4096):
                bot.send_message(message.chat.id, info[x:x + 4096])
        else:
            bot.send_message(
                message.chat.id,
                info,
                reply_markup=keyboard,
            )
        bot.send_message(
            message.chat.id,
            u'\U0001F957' + u'\U0001F370' + u'\U0001F363' + u'\U0001F349' + u'\U0001F372' + u'\U0001F354' + u'\U0001F951' + '\nДля вызова справки нажмите /help\n',
            reply_markup=keyboard,
        )
        print(datetime.datetime.now())
        print('Total OK')
        nofile = 0
    else:
        keyboard.add(telebot.types.InlineKeyboardButton(
            'Сообщить об ошибке разработчику', url='telegram.me/s1esarev'))
        bot.send_message(message.chat.id,
                         'Произошла ошибка! Был введен неверный код или остутствует доступ к серверу с данными по столовой. \nДля вызова справки нажмите /help',
                         reply_markup=keyboard,
                         )

        print(datetime.datetime.now())
        print(message.text[0:3] + ' Error')


def get_ex_callback(query):
    bot.answer_callback_query(query.id)
    send_exchange_result(query.message, query.data[4:] + '_RUB')


def send_exchange_result(message, ex_code):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
        message.chat.id, get_exchange(ex_code)
    )
    help_command(message)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_chat_action(message.chat.id, 'typing')

    keyboard = telebot.types.InlineKeyboardMarkup()
    if period:
        mypath = config.PATH + message.text[0:3] + '.txt'
    else:
        mypath = config.PATH +  'previous\\' + message.text[0:3] + '.txt'

    if message.text.title() == 'Имбирева':
        bot.send_message(message.chat.id, u'\U0001F9E1')
    elif os.path.exists(mypath):
        # try:
        info = open(mypath).read()
        if len(info) > 4096:
            for x in range(0, len(info), 4096):
                bot.send_message(message.chat.id, info[x:x + 4096])
        else:
            bot.send_message(
                message.chat.id,
                info,
                reply_markup=keyboard,
            )
        bot.send_message(
            message.chat.id,
            u'\U0001F957' + u'\U0001F370' + u'\U0001F363' + u'\U0001F349' + u'\U0001F372' + u'\U0001F354' + u'\U0001F951' + '\nДля вызова справки нажмите /help\n',
            reply_markup=keyboard,
        )
        print(datetime.datetime.now())
        print(message.text[0:3] + ' OK')
        nofile = 0
    else:
        keyboard.add(telebot.types.InlineKeyboardButton(
            'Сообщить об ошибке разработчику', url='telegram.me/s1esarev'))
        bot.send_message(message.chat.id,
                         'Произошла ошибка! Был введен неверный код или остутствует доступ к серверу с данными по столовой. \nДля вызова справки нажмите /help',
                         reply_markup=keyboard,
                         )

        print(datetime.datetime.now())
        print(message.text[0:3] + ' Error')


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception:
            pass
     # bot.remove_webhook()
