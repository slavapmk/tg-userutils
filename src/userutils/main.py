import asyncio

from pyrogram import Client, filters
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import Message
from pyrogram.types.user_and_chats.user import Link

from userutils.data import storage
from userutils.data.storage import config


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
    async def test(_, event: Message):
        if event.text == '@all':
            if event.chat.type not in (ChatType.PRIVATE, ChatType.BOT, ChatType.CHANNEL):
                ans = []
                async for member in event.chat.get_members():
                    if member.user.id == app.me.id:
                        continue
                    if len(member.user.username) != 0:
                        ans.append(
                            Link(f'tg://user?id={member.user.id}', f'@{member.user.username}', ParseMode.MARKDOWN)
                        )
                    else:
                        ans.append(
                            Link(f'tg://user?id={member.user.id}', f'@{member.user.first_name}', ParseMode.MARKDOWN)
                        )
                await event.edit_text(' '.join(ans))
        else:
            text = event.text
            print(text)


def entrypoint():
    asyncio.get_event_loop().create_task(general_task())
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    entrypoint()
