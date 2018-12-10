import requests
import config
import telebot
from datetime import datetime, time, date
from bs4 import BeautifulSoup
from typing import Optional, Tuple
from telebot import apihelper

apihelper.proxy = {'https': 'socks5://telegram:telegram@sr.spry.fail:1080'}
week_days = ['/monday', '/tuesday', '/wednesday',
             '/thursday', '/friday', '/saturday', '/sunday']
name_days = ['Понедельник', 'Вторник', 'Среда',
             'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
bot = telebot.TeleBot(config.access_token)


def get_page(group: str, week: str='') -> str:
    if week:
        week = str(week) + '/'
    url = f'{config.domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_day(web_page, day_number: str) -> Optional[tuple]:
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием
    schedule_table = soup.find("table", attrs={"id": day_number + "day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.replace('\n', '').replace(
        '\t', '') for lesson in lessons_list]
    return times_list, locations_list, lessons_list


def week_and_day(n_week: int, n_day: int) -> Tuple[int, str]:
    """ Получение информации через проверку на четность и вскр. """
    # Определение недели по четности
    week = 1 if n_week % 2 else 2

    # Определние дня, если день недели - воскресенье
    week = 2 if (n_day == 7 and week == 1) else 1
    day = '1' if n_day == 7 else str(n_day)

    return week, day


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    try:
        message_info = message.text.split()
        if len(message_info) == 2:
            week_day, group = message_info
            web_page = get_page(group)
            day = str(week_days.index(week_day) + 1)
        else:
            week_day, week, group = message_info
            web_page = get_page(group, week)
            day = str(week_days.index(week_day) + 1)
    except:
        bot.send_message(
            message.chat.id, 'Вы ввели неверные данные. ')
        return None

    try:
        times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(
            web_page, day)
        resp = ''
        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            resp += f'<b>{time}</b>, {location}, {lesson}' + '\n\n'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except AttributeError:
        bot.send_message(
            message.chat.id, 'У вас нет пар в этот день.', parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _, group = message.text.split()
    today = datetime.now().isocalendar()
    week, day = week_and_day(today[1], today[2])
    current_time = datetime.strftime(datetime.now(), "%H:%M")
    web_page = get_page(group, week)
    times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(
        web_page, day)
    resp = ''
    resp += f"<b>Время: </b>{current_time}\n<b>Ближайшее занятие: </b>\n"
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        try:
            class_time = datetime.strftime(
                datetime.strptime(time[:4], "%H:%M"), "%H:%M")
            if class_time > current_time:
                resp += f'<b>{time}</b>, {location}, {lesson}' + '\n\n'
                break
        except:
            resp = 'У вас нет занятий в ближайшее время.'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получть расписание на завтра для указанной группы """
    _, group = message.text.split()
    today = datetime.now().isocalendar()
    week, day = week_and_day(today[1], today[2] + 1)
    try:
        web_page = get_page(group, week)
        times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(
            web_page, day)
        resp = ''
        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            resp += f'<b>{time}</b>, {location}, {lesson}' + '\n\n'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except:
        resp = 'Занятий завтра нет.'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    try:
        message_info = message.text.split()
        if len(message_info) == 2:
            _, group = message.text.split()
            web_page = get_page(group)
        else:
            _, week, group = message_info
            web_page = get_page(group, week)
    except:
        bot.send_message(
            message.chat.id, 'Вы ввели неверные данные. ')
        return None
    resp = ''
    for day in range(6):  # выводим расписание для всех 6 учебных дней в неделе
        try:
            times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(
                web_page, str(day + 1))
            # если занятия есть и все прошло гладко, выводим имя дня недели
            resp += '\n\n<b>' + name_days[day] + '</b>\n'
        except:
            continue
        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            resp += f'<b>{time}</b>, {location}, {lesson}' + '\n\n'

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
