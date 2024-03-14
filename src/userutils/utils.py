def markdown_escaped(text: str | int) -> str:
    if isinstance(text, int):
        text = str(text)
    escaping = ['*', '_', '~', '|', '[', ']', '!', '`', '>', '{', '}', '+', '-']
    for escape in escaping:
        text = text.replace(escape, f'\\{escape}')
    return text


def index_to_day(day: int) -> str:
    days = [
        'Понедельник',
        'Вторник',
        'Среда',
        'Четверг',
        'Пятница',
        'Суббота',
        'Воскресенье'
    ]
    return days[day % 7]


__days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']


def day_to_index(day: str) -> int:
    day = day.lower()
    if day in __days:
        return __days.index(day.lower())
    else:
        return -1
