import asyncio
import random
from asyncio import sleep
from datetime import datetime, timedelta

import aiocron
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ParseMode
from pyrogram.raw.functions.messages import ReadMentions
from pyrogram.types import Message
from pyrogram.types.user_and_chats.user import Link

from userutils.data import storage
from userutils.data.storage import config

fap_chat = -1002053312362
ege_chat = -1001707241381


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def general_task():
    await storage.load()
    storage.check_file_parent('storage/sessions/check')
    client = Client(
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
    await client.start()

    @client.on_message(filters.me)
    async def on_my_message(_, event: Message):
        if event.text == '@all':
            if event.chat.type in [ChatType.PRIVATE, ChatType.BOT, ChatType.CHANNEL]:
                return
            ans = []
            async for member in event.chat.get_members():
                if member.user.id == client.me.id or member.user.is_bot:
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
                await client.send_message(event.chat.id, ' '.join(chunk))
                await sleep(
                    random.randrange(5, 15) / 10
                )
        elif event.text == '!stop confirm':
            exit(0)

    peer = await client.resolve_peer(fap_chat)

    @aiocron.crontab('*/10 * * * *')
    async def process_fap():
        await client.send_message(
            fap_chat,
            'Дроч'
        )

    @aiocron.crontab('0 * * * *')
    async def process_dick():
        await client.send_message(
            fap_chat,
            '/dick'
        )

    @aiocron.crontab('0 0 * * *')
    async def process_grow():
        await client.send_message(
            -1001874841071,
            '/grow',
            reply_to_message_id=14071
        )

    ege_date = datetime(2024, 5, 28)

    @aiocron.crontab('0 0 * * *')
    async def process_ege():
        delta: timedelta = ege_date - datetime.now()
        await client.send_message(
            ege_chat,
            f'Кайфуем, у нас ещё {delta.days}д отдыха'
        )

    @client.on_message(filters.chat(fap_chat))
    async def on_message(_client: Client, _message: Message):
        await client.read_chat_history(fap_chat)
        await client.invoke(ReadMentions(peer=peer))


def entrypoint():
    asyncio.get_event_loop().create_task(general_task())
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    entrypoint()
