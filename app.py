from database import DataBase
from info import *
from telegram.ext import *
from telegram import *
import telegram

class ChatBot:
    def __init__(self, bot_name, bot_key):
        self.boys = []
        self.girls = []
        self.chat_pair = {}

        self.bot_name, self.bot_key = bot_name, bot_key

        # Calling  database
        self.record = DataBase()

        # Bot command handler
        self.command_handler()

    def common_args(self, update, context):
        if update.message.chat.type != "private":
            user_id = update.message.chat.id
            name = context.bot.get_chat(chat_id=user_id).title
            username = context.bot.get_chat(chat_id=user_id).username

        else:
            user_id = update.message.from_user.id
            name = update.message.from_user.first_name
            username = update.message.from_user.username

        return user_id, name, username

    def start(self, update, context):
        user_id, name, username = self.common_args(update, context)

        # chat type (group or private)
        chat_type = update.message.chat.type

        if chat_type == "private":
            try:
                check_user = self.record.search(user_id)
                if not check_user:
                    # record insertion
                    self.record.insert(user_id, name, username)

                # Typing Action
                context.bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING, timeout=1)
                # User welcome
                update.message.reply_text(text=welcome(name), parse_mode='Markdown')

                if check_user and not check_user.get('gender') and not check_user.get('partner_gender'):
                    self.settings(update, context)

            # if user stop the bot
            except telegram.error.Unauthorized:
                pass

    def help(self, update, context):
        user_id, name, username = self.common_args(update, context)

        # chat type (group or private)
        chat_type = update.message.chat.type

        if chat_type == "private":
            try:
                # Typing Action
                context.bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING, timeout=1)

                # Help user
                update.message.reply_text(text=user_help(), parse_mode='Markdown')

            # if user stop the bot
            except telegram.error.Unauthorized:
                pass

    def settings(self, update, context):
        user_id, name, username = self.common_args(update, context)

        # chat type (group or private)
        chat_type = update.message.chat.type

        if chat_type == "private":
            try:
                # Typing Action
                context.bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING, timeout=1)

                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="🤴🏻 Gender 👸🏻", callback_data='SetGender')]
                ])

                # User info
                update.message.reply_text(text="🛠Settings", reply_markup=reply_markup)

            # if user stop the bot
            except telegram.error.Unauthorized:
                pass