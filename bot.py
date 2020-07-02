#!/usr/bin/env python3
import logging.config
import random

try:
    import settings
except ImportError:
    exit('Do cp settings.py.default settings.py and set token!')

from log_config import log_config

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


logging.config.dictConfig(log_config)
log = logging.getLogger('file_stream')
users_log = logging.getLogger('users_handler')


class MyVkBotLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as exc:
                # print('error', exc)
                pass


class Bot:
    """
    Echo bot for vk.com
    Use python 3.7
    """
    def __init__(self, group_id, token):
        """
        :param group_id: group id из группы vk
        :param token: секретный токен
        """
        self.group_id = group_id
        self.token = token

        self.vk = vk_api.VkApi(token=token)
        self.api = self.vk.get_api()
        self.long_poller = MyVkBotLongPoll(self.vk, self.group_id)

    def start(self):
        """Запуск бота"""
        for event in self.long_poller.listen():
            try:
                self.on_event(event=event)
            except Exception as exc:
                log.exception('Ошибка в обработке события')

    def on_event(self, event):
        """
        Отправляет сообщение назад, если это текст
        :param event: VkBotMessageEvent object
        :return: None
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.debug('Отправляем сообщение назад')
            # print('Incoming message:', event.object.message['text'])
            user = self.api.users.get(user_ids=event.object.message['from_id'], fields='verified')
            sticker = ''
            if event.object.message['attachments']:
                sticker = 'К сожалению, стикеры возвращать я ещё не умею((('
            # if user[0]["first_name"] == '':
            #     echo_message = f'Привет, {user[0]["first_name"]}! ' \
            #                    f'Возвращаю ваше сообщение: {event.object.message["text"] + sticker}' \
            #                    f'\nИ, также, напоминаю вам о необходимости оплаты сервера.)))' \
            #                    f'\nПриятно было тебя услышать!!! 😎'
            # else:
            echo_message = f'Здравствуйте, {user[0]["first_name"]}! ' \
                           f'Возвращаю ваше сообщение: {event.object.message["text"] + sticker}'
            # print('Outgoing message:', echo_message)
            self.api.messages.send(
                random_id=random.randint(0, 2 ** 40),
                message=echo_message,
                peer_id=event.object.message['peer_id']
            )
            users_log.info('user_id %s', event.object.message["from_id"])
        else:
            log.info('While I can not respond to this event, %s', event.type)


if __name__ == '__main__':
    bot = Bot(group_id=settings.GROUP_ID, token=settings.TOKEN)
    bot.start()
