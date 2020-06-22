#!/usr/bin/env python3
import random

from reg_data import token, GROUP_ID

import vk_api
import vk_api.bot_longpoll


class Bot:
    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token

        self.vk = vk_api.VkApi(token=token)
        self.api = self.vk.get_api()
        self.long_poller = vk_api.bot_longpoll.VkBotLongPoll(self.vk, self.group_id)

    def start(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event=event)
            except Exception as exc:
                print(exc)

    def on_event(self, event):
        if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            print('Incoming message:', event.object.message['text'])
            user = self.api.users.get(user_ids=event.object.message['from_id'], fields='verified')
            echo_message = f'Здравствуйте, {user[0]["first_name"]}! ' \
                           f'Возвращаю ваше сообщение: {event.object.message["text"]}'
            print('Outgoing message:', echo_message)
            self.api.messages.send(
                random_id=random.randint(0, 2 ** 40),
                message=echo_message,
                peer_id=event.object.message['peer_id']
            )
        else:
            print('While I can not respond to this event,', event.type)


if __name__ == '__main__':
    bot = Bot(group_id=GROUP_ID, token=token)
    bot.start()
