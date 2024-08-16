from constants import *
import telebot
from telebot import types
import botFunctions

# Dictionary to store user states
user_states = {}
username_holder = {}


def main(API_KEY):
    bot = telebot.TeleBot(API_KEY, parse_mode=None)

    # Start command handler
    @bot.message_handler(commands=['start'])
    def start_message(message):
        user_states[message.chat.id] = 'username'
        bot.send_message(message.chat.id, WELCOME_MESSAGE.format(
            first_name=message.from_user.first_name))
        bot.send_message(message.chat.id, USERNAME_PROMPT)

    # Function to authenticate username
    def authenticate_user(message, attempts=1, MAX_ATTEEMPTS=3):
        if attempts > MAX_ATTEEMPTS:
            bot.send_message(
                message.chat.id, MAX_LOGIN_ATTEMPTS_EXCEEDED)
            return

        username = message.text
        if botFunctions.username_check(username):
            user_states[message.chat.id] = 'password'
            bot.send_message(message.chat.id, PASSWORD_PROMPT)
            bot.register_next_step_handler(
                message, authenticate_password, username)
        else:
            bot.send_message(
                message.chat.id, INVALID_USERNAME)
            bot.register_next_step_handler(
                message, authenticate_user, attempts + 1)

    # Function to authenticate password and create menu
    def authenticate_password(message, username, attempts=1, MAX_ATTEEMPTS=3):
        if attempts > MAX_ATTEEMPTS:
            bot.send_message(
                message.chat.id, MAX_LOGIN_ATTEMPTS_EXCEEDED)
            return

        password = message.text

        if botFunctions.password_check(username, password):
            user_first_name, user_last_name = botFunctions.get_name(username)
            bot.send_message(message.chat.id, SUCCESSED_LOGIN_MESSAGE.format(
                first_name=user_first_name, last_name=user_last_name))

            user_states[message.chat.id] = 'menu'
            username_holder[message.chat.id] = username
            create_menu(message)
        else:
            bot.send_message(message.chat.id, INVALID_PASSWORD)
            bot.register_next_step_handler(
                message, authenticate_password, username, attempts + 1)

    # Function to create menu

    def create_menu(message):
        markup = types.ReplyKeyboardMarkup(row_width=1)
        files_btn = types.KeyboardButton(GET_FILE)
        close_btn = types.KeyboardButton(CLOSE_MENU)
        markup.add(files_btn, close_btn)
        bot.send_message(
            message.chat.id, OPTION_MESSAGE, reply_markup=markup)

    # Function to get the file
    @bot.message_handler(chat_types=[GET_FILE])
    def get_file(message):
        file_address = botFunctions.check_file(
            username_holder.get(message.chat.id))

        if file_address:
            try:
                with open(file_address, 'rb') as file:
                    bot.send_document(message.chat.id, file)
                bot.send_message(message.chat.id, SURVEY_MESSAGE)
                user_states[message.chat.id] = 'survey'
                survey(message)
            except Exception as e:
                bot.send_message(message.chat.id, f"Error sending file: {e}")
        else:
            bot.send_message(message.chat.id, FILE_NOT_FOUND_MESSAGE)

    # Exit command handler
    @bot.message_handler(chat_types=[CLOSE_MENU])
    def exit_message(message):
        # حذف منوی کیبورد
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, THANK_YOU_MESSAGE,
                         reply_markup=markup)
        # بازگرداندن استیت به حالت اولیه
        user_states[message.chat.id] = 'username'

    def out_of_condition(message):
        bot.send_message(message.chat.id, OUT_OF_CONDITION)

    def survey(message):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
        markup.add("عالی", "خوب", "متوسط", "ضعیف")
        bot.send_message(
            message.chat.id, SURVEY_ASK, reply_markup=markup)
        bot.register_next_step_handler(message, process_survey)

    def process_survey(message):
        user_opinion = message.text
        if user_opinion == "عالی" or user_opinion == "خوب" or user_opinion == "متوسط" or user_opinion == "ضعیف":
            botFunctions.set_opinion(
                user_opinion, username_holder[message.chat.id])
            # اینجا می‌توانید عملیات ذخیره‌سازی را انجام دهید، مانند ذخیره در دیتابیس یا فایل
            bot.send_message(message.chat.id, SURVEY_DONE)
        else:
            out_of_condition(message)
        # بازگرداندن استیت به حالت اولیه
        user_states[message.chat.id] = 'username'

        # حذف دکمه‌های منوی کیبورد
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, THANK_YOU_MESSAGE,
                         reply_markup=markup)

        # Message handler

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        chat_id = message.chat.id
        state = user_states.get(chat_id)

        if state == 'username':
            authenticate_user(message)
        elif state == 'password':
            authenticate_password(message)
        elif state == 'menu' and message.text == GET_FILE:
            get_file(message)
        elif state == 'menu' and message.text == CLOSE_MENU:
            exit_message(message)
        elif state == 'survey':
            survey(message)
        else:
            out_of_condition(message)

    bot.polling()


if __name__ == "__main__":
    main(API_KEY)
