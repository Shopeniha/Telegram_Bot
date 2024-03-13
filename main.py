# подключение библиотек
# в google colab добавить: !pip install pyTelegramBotAPI
# в google colab добавить: !pip install Faker
# для установки необходимо в файл requirements.text добавить строки
# 'PyTelegramBotApi'
# 'faker'

from telebot import TeleBot, types
from faker import Faker
from datetime import datetime, timedelta


bot = TeleBot(token='Вставьте свой токен', parse_mode='html') # создание бота

faker = Faker() # утилита для генерации номеров кредитных карт

# объект клавиатуры
card_type_keybaord = types.ReplyKeyboardMarkup(resize_keyboard=True)
# первый ряд кнопок
card_type_keybaord.row(
    types.KeyboardButton(text='VISA'),
    types.KeyboardButton(text='Mastercard'),
)
# второй ряд кнопок
card_type_keybaord.row(
    types.KeyboardButton(text='Maestro'),
    types.KeyboardButton(text='JCB'),
)

# обработчик команды '/start'
@bot.message_handler(commands=['start'])
# отправляем ответ на команду '/start'
def welcome(message):
    photo = open('welcome_sticker.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    bot.send_message(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        text='Привет! Я умею генерировать тестовые банковские карты.\nПожалуйста, выбери тип карты:', # текст сообщения
        reply_markup=card_type_keybaord,
    )

# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    # проверяем текст сообщения на совпадение с текстом какой-либо из кнопок
    # в зависимости от типа карты присваиваем значение переменной 'card_type'
    if message.text.lower() in ['visa', 'виса', 'виза', 'visа', 'вisa','вiса', 'мшыф']:
        card_type = 'visa'
    elif message.text.lower() in ['mastercard', 'мастеркард', 'мастеркарт', 'мастерка', 'мастер', 'ьфыеуксфкв']:
        card_type = 'mastercard'        
    elif message.text.lower() in ['maestro', 'маэстро', 'маестро', 'маестр', 'ьфуыекщ']:
        card_type = 'maestro'
    elif message.text.lower() in ['jcb', 'джисиби', 'дсб', 'джсб', 'джсиби', 'джисб', 'оси']:
        card_type = 'jcb'
    else:
        # если текст не совпал ни с одной из кнопок 
        # выводим ошибку
        bot.send_message(
            chat_id=message.chat.id,
            text='Не понимаю тебя 😔\n\n⬇️Попробуй выбрать один из вариантов⬇️',
            reply_markup=card_type_keybaord,
        )
        return

    # получаем номер тестовой карты выбранного типа
    # card_type может принимать одно из значений ['maestro', 'mastercard', 'visa13', 'visa16', 'visa19',
    # 'amex', 'discover', 'diners', 'jcb15', 'jcb16']
    start_date = datetime.now() + timedelta(days=365*2)  # текущая дата + 2 года
    card_secret = faker.credit_card_security_code(card_type)
    card_number = faker.credit_card_number(card_type)
    card_date = faker.credit_card_expire(start=start_date, end='+12y', date_format='%m/%y')
    # выводим пользователю
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Тестовая карта {card_type.upper()}:\nНомер карты: <code>{card_number}</code>\nДата: <code>{card_date}</code>\nCVC/CVV: <code>{card_secret}</code>'
    )

# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()

if __name__ == '__main__':
    main()
