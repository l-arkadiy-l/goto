import json
import telebot
from random import randint

token = "5599310127:AAH_nAAydK5mivzHA58Imk9_zCNYMoPT4YQ"
bot = telebot.TeleBot(token)
model = "hello word"


@bot.message_handler(commands=["start"])
# создаю функцию привествие ->start
def start(message):
    bot.send_message(
        message.chat.id,
        'Приветствую в боте\n'
        'Пришлите мне тайм в таком формате 08:00, 09:10\n'
        '*Важно прислать не менее таймов N \n*'
        '*Также не забывайте о запятой для разделения*', parse_mode="Markdown")

    # передаю сообщение от юзера в функцию constructor
    bot.register_next_step_handler(message, constructor)


@bot.message_handler(content_types=["text"])
def constructor(message):
    text = ' '.join(' '.join(message.text.replace(" ", "").split(",")).split('-')).split()
    # print(text)
    temp = list(filter(lambda x: x in 'вечер, утро, перерыв, работа, еда, спорт'.split(', '), text))
    times = list(filter(lambda x: x not in 'вечер, утро, перерыв, работа, еда, спорт'.split(', '), text))
    # создаем словарь в котором ключ-это тайм,а values - это предикт модели
    dict_of_time = {}
    # кладу в дикт соответствующие значения
    with open('data.json', 'r') as f:
        r = json.load(f)
    # print(temp)
    for i in range(len(times)):
        dict_of_time[times[i]] = r[temp[i]]

    # создаю лист в который кладу строчки c таймом и предиктом
    list_of_time = []
    for key in dict_of_time:
        list_of_time.append(
            f"\n{key} - {':'.join(dict_of_time[key][randint(0, len(dict_of_time[key]))].split(':')[1:])}")
    # делаю join по запятой
    str_of_time = ",".join(list_of_time)
    print(type(str_of_time))
    # отправляю юзеру его сообщение
    print('-->', str_of_time)
    bot.send_message(message.chat.id, str_of_time)


# except Exception:
#     bot.send_message(message.chat.id, 'вы ввели не то или не так')


# запускаем бота
if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
