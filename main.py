import telebot

import parser_model

token = '5834434241:AAFkpYXp2eQNS_0TjL74Z02YcO4qjWLRXQk'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['help', 'start'])
def help_command(message):
    bot.send_message(message.chat.id,
                     'Я помогу тебе найти нужную информацию о радиолокаторах. '
                     '\nЧто я могу:\n/models - вывести название всех моделей, \n/start - начать заново')
    bot.send_message(message.chat.id, 'Введите название модели:')


@bot.message_handler(commands=['models'])
def get_models(message):
    models = parser_model.get_models()
    partition = 50

    for i in range(0, len(models), partition):
        result = ', '.join(models[i:min(len(models), i + partition)])
        bot.send_message(message.chat.id, result)

    bot.send_message(message.chat.id, 'Введите название модели:')


@bot.message_handler(content_types=['text'])
def get_description(message):
    try:
        description = parser_model.get_discription_by_model(message.text)
        bot.send_message(message.chat.id, description)
    except:
        bot.send_message(message.chat.id, 'Увы, у меня нет такой информации(')


bot.infinity_polling()
