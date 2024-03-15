import asyncio
import random
from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import Message
from pyrogram.types.user_and_chats.user import Link

from userutils.data import storage
from userutils.data.storage import config


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def general_task():
    await storage.load()
    storage.check_file_parent('storage/sessions/check')
    app = Client(
        config.data.login_phone.replace('+', ''),
        config.data.api_id,
        config.data.api_hash,
        'Telegram Desktop 4.15 x64',
        'ASUS-PC',
        'Windows 11',
        phone_number=config.data.login_phone,
        password=config.data.login_password,
        workdir='storage/sessions/'
    )
    await app.start()

    @app.on_message(filters.me)
    async def on_my_message(_, event: Message):
        if event.text == '@all':
            if event.chat.type in [ChatType.PRIVATE, ChatType.BOT, ChatType.CHANNEL]:
                return
            ans = []
            async for member in event.chat.get_members():
                if member.user.id == app.me.id or member.user.is_bot:
                    continue
                if member.user.username is None or len(member.user.username) != 0:
                    name = f'@{member.user.username}'
                else:
                    name = str(member.user.first_name)
                ans.append(
                    Link(f'tg://user?id={member.user.id}', name, ParseMode.MARKDOWN)
                )

            await event.delete()
            for chunk in chunks(ans, 5):
                await app.send_message(event.chat.id, ' '.join(chunk))
                await sleep(
                    random.randrange(5, 15) / 10
                )

    # @app.on_deleted_messages()
    # async def on_deleted_message(_, event: list[Message]):
    #     for event_message in event:
    #         try:
    #             if event_message.chat is not None and event_message.chat.type in [ChatType.CHANNEL, ChatType.BOT]:
    #                 continue
    #             await app.send_message(
    #                 # config.data.archive_chat,
    #                 'me',
    #                 f'CHAT #{event_message.chat.id} - {event_message.chat.first_name}\n'
    #                 f'FROM #{event_message.from_user.id} - ' + ' '.join(
    #                     [event_message.from_user.first_name, event.from_user.last_name])
    #             )
    #             await event_message.copy(config.data.archive_chat)
    #         except AttributeError as e:
    #             print(event_message)


def entrypoint():
    asyncio.get_event_loop().create_task(general_task())
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    entrypoint()
