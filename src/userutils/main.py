import asyncio
import random
from asyncio import sleep

import aiocron
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
        elif event.text == '!stop confirm':
            exit(0)

    @aiocron.crontab('*/10 * * * *')
    async def process_10m():
        await app.send_message(
            -1002053312362,
            'Дроч'
        )
        await sleep(3)
        await app.read_chat_history(-1002053312362)

    @aiocron.crontab('0 * * * *')
    async def process_1h():
        await app.send_message(
            -1002053312362,
            '/dick'
        )

    @aiocron.crontab('0 0 * * *')
    async def process_24h():
        await app.send_message(
            -1001874841071,
            '/grow',
            reply_to_message_id=14071
        )


def entrypoint():
    asyncio.get_event_loop().create_task(general_task())
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    entrypoint()
