import config
import telebot
from telebot import types
from database import Database

db = Database('db.db')
bot = telebot.TeleBot(config.TOKEN)

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('💼 Профил')
    item2 = types.KeyboardButton('👥 Ҷустуҷуи дуст')
    markup.add(item1, item2)
    return markup

def stop_dialog():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('🗣 Фиристодани ник - и худ ба дуст')
    item2 = types.KeyboardButton('/stop')
    markup.add(item1, item2)
    return markup

def stop_search():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('❌  Манъ кардани ҷустуҷӯ')
    markup.add(item1)
    return markup

@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Ман писар 👨')
    item2 = types.KeyboardButton('Ман духтар 👩‍🦱')
    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Салом, {0.first_name}! ХУШ ОМАДЕД БА БОТИ МО, лутфан ҷинсияти худро интихоб намоед! '.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('💼 Профил')
    item2 = types.KeyboardButton('👥 Ҷустуҷуи дуст')
    markup.add(item1,)
    markup.add(item2,)

    bot.send_message(message.chat.id, '📝 Меню'.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info != False:
        db.delete_chat(chat_info[0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('✏️ Ҷустуҷуи дигар')
        item2 = types.KeyboardButton('/menu')
        markup.add(item1, item2)

        bot.send_message(chat_info[1], '❌  Дуст чатро тарк кард!', reply_markup = markup)
        bot.send_message(message.chat.id, '❌  Шумо аз чат баромадед!', reply_markup = markup)
    else:
        bot.send_message(message.chat.id, '❌  Шумо ҳоло чатро сар накардед!', reply_markup = main_menu())


@bot.message_handler(content_types = ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '👥 Ҷустуҷуи дуст' or message.text == '✏️ Ҷустуҷуи дигар':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('🔎 Писар')
            item2 = types.KeyboardButton('🔎 Духтар')
            item3 = types.KeyboardButton('👩‍👨 Рандом')
            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'Киро меҷӯед?', reply_markup = markup)

            
        elif message.text == '❌  Манъ кардани ҷустуҷӯ':
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, '❌  Ҷустуҷу манъ карда шуд ба /menu гузаред! ', reply_markup = main_menu())

        
        elif message.text == '🔎 Писар':
            user_info = db.get_gender_chat('male')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Дар ҳоли ҷустуҷӯ, интизор шавед бо нафаре пайваст мешавед!', reply_markup = stop_search())
            else:
                mess = 'Нафаре ёфт шуд ки бо шумо дар алоқа аст суҳбатро оғоз намоед \n Барои қатъи сӯҳбат /stop - ро пахш намоед!'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())

        
        elif message.text == '🔎 Духтар':
            user_info = db.get_gender_chat('female')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Дар ҳоли ҷустуҷӯ, интизор шавед бо нафаре пайваст мешавед!', reply_markup = stop_search())
            else:
                mess = 'Нафаре ёфт шуд ки бо шумо дар алоқа аст суҳбатро оғоз намоед \n Барои қатъи сӯҳбат /stop - ро пахш намоед!'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        

        elif message.text == '👩‍👨 Рандом':
            user_info = db.get_chat()
            chat_two = user_info[0]

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Дар ҳоли ҷустуҷӯ, интизор шавед бо нафаре пайваст мешавед!', reply_markup = stop_search())
            else:
                mess = 'Нафаре ёфт шуд ки бо шумо дар алоқа аст суҳбатро оғоз намоед \n Барои қатъи сӯҳбат /stop - ро пахш намоед!'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        elif message.text == '🗣 Фиристодани ник - и худ ба дуст':
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info != False:
                if message.from_user.username:
                    bot.send_message(chat_info[1], 'Дуст барои Шумо username-и аккаунташро фиристод: \n @' + message.from_user.username)
                    bot.send_message(message.chat.id, '✅ Ник - и аккаунти Шумо ба дуст фиристода шуд! ')
                else:
                    bot.send_message(message.chat.id, '❌  Дар аккаунти Шумо username (ник) мавҷуд нест!')
            else:
                bot.send_message(message.chat.id, '❌ Шумо ҳоло чатро сар накардед!')

        

        elif message.text == 'Ман писар 👨':
            if db.set_gender(message.chat.id, 'male'):
                bot.send_message(message.chat.id, '✅  Ҷинси Шумо ҳамчун "писар" қабул гардид! ', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id, '❌  Шумо аллакай ҷинсияти худро интихоб кардаед лутфан ба қисми /menu гузаред!')
        
        elif message.text == 'Ман духтар 👩‍🦱':
            if db.set_gender(message.chat.id, 'female'):
                bot.send_message(message.chat.id, '✅  Ҷинси Шумо ҳамчун "духтар" қабул гардид! ', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id, '❌  Шумо аллакай ҷинсияти худро интихоб кардаед лутфан ба қисми /menu гузаред!')
        
        elif message.text == '💼 Профил':
            bot.send_message(message.chat.id, f'ID-ии Шумо: `{message.from_user.id}` \n Статуси Шумо:' + str(db.get_vip (message.from_user.id)),  parse_mode="MARKDOWN")

        
        else:
            if db.get_active_chat(message.chat.id) != False:
                chat_info = db.get_active_chat(message.chat.id)
                bot.send_message(chat_info[1], message.text)
            else:
                bot.send_message(message.chat.id, '❌ Шумо ҳоло чатро сар накардед!')



@bot.message_handler(content_types='sticker')
def bot_sticker(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_sticker(chat_info[1], message.sticker.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Шумо ҳоло чатро сар накардед!')

@bot.message_handler(content_types='voice')
def bot_voice(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_voice(chat_info[1], message.voice.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Шумо ҳоло чатро сар накардед!')
 
@bot.message_handler(content_types='photo')
def bot_photo(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_photo(chat_info[1], message.photo.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Шумо ҳоло чатро сар накардед!')
 
@bot.message_handler(content_types='video')
def bot_video(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_video(chat_info[1], message.video.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Шумо ҳоло чатро сар накардед!')

@bot.message_handler(content_types='video_note')
def bot_video_note(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_video_note(chat_info[1], message.video_note.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Шумо ҳоло чатро сар накардед!')

bot.polling(none_stop = True)