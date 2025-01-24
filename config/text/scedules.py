ONE_TIME_GREET = '''
*Давай запланируем прием у специалиста!*

Назови его для себя, так чтоб тебе было удобно и понятно, к кому именно и на что ты хочешь записаться.
Длина названия не более 25 символов.
После этого сможешь добавить описание событию и укажешь дату и время когда мне об этом следует напомнить.
'''

IS_REGULAR = '''
Это регулярное событие?
'''

REGULAR_GREET = '''
*Давай запланируем прием лекарств или посещение процедуры!*
'''

SCHEDULE_NAMING = '''
Дай название напоминанию. После этого создадим описание и установим время.
'''

REGULAR_DESCR = '''
Опиши для себя, так чтоб тебе было удобно и понятно, какое именно лекарство и как нужно принять. После этого установим время.
'''

REGULAR_SHCED = '''
Я ежедневно буду напоминать тебе об этом. Укажи время в формате:
"ЧЧ:ММ"

Например:
12:00
'''

ENTER_DESCR = '''
Опиши событие.
'''

ENTER_DATE = '''
Введи дату и время когда мне об этом тебе напомнить? Укажи время заранее, чтоб не опоздать.
Запиши это без кавычек, разделяя пробелом, в формате:
"ДД.ММ.ГГГГ  ЧЧ:ММ"

Например:
01.12.2001 12:00
'''

DATE_ERR = '''
Кажется ошибка в формате записи. Обратите внимание что мне нужна именно форма:
"ДД.ММ.ГГГГ ЧЧ:ММ"

Обрати внимание что между датой и временем один пробел.
Например:
01.12.2001 12:00
'''

TIME_ERR = '''
Кажется ошибка в формате записи. Обратите внимание что мне нужна именно форма:
"ЧЧ:ММ"

Например:
12:00
'''


DATE_LOSE = '''
Кажется указанное время уже прошло. Напиши дату из будущего.
'''

SCHED_FUTURE = '''
Я напомню о "{event_name}"  в {specified_time}
'''

SCHED = '''
С радостью напоминаю о "{event_name}"
'''

ANOTHER_ONE_TIME_GREET = '''
Опиши для себя, так чтоб тебе было удобно и понятно, какое именно лекарство и как нужно принять. После этого уже укажешь дату и время.
'''

REGULAR_GREET = '''
Давай запланируем прием лекарств или посещение процедуры!
'''

TEXT_ERR = '''
Напиши текстом. Я понимаю только текст
'''