from bs4 import BeautifulSoup
from vk_api.longpoll import VkLongPoll, VkEventType
import urllib.request
import vk_api


def get_token(path):
    file = open(path, 'r')
    data = file.readline()
    file.close()
    # with open(path, 'r') as data:
    return data


vk_token = get_token(path='ApiToken.txt')
vk = vk_api.VkApi(token=vk_token)
vk._auth_token(reauth=None)
values = {'message_ids': 18}

links = {'programming': 'http://www.vega.fcyb.mirea.ru/disc/disc.php?id=121',
         'practice': 'http://www.vega.fcyb.mirea.ru/disc/disc.php?id=122'}


def get_html(url):
    print(url)
    response = urllib.request.urlopen(url)
    return response.read()


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find_all('div')
    for block in div:
        if block.find('label'):
            is_homework = False
            try:
                is_homework = True \
                    if block.find('label').text.strip(' ').index('Домашнее задание') >= 0 \
                    else False
            except ValueError:
                is_homework = False
                continue
            if is_homework:
                li = block.find('li')
                if li:
                    return li.text


def write_msg(user_id, s):
    vk.method('messages.send', {'user_id': user_id, 'message': s})


def formating(msg):
    msg = msg.lower()
    msg = msg.strip(' ')
    return msg


def get_help_text():
    text = """Я Бот для получения домашних заданий. \
    \nСписок доступных команд: \
    \n"Справка", "Помощь", "Команды" \
    \n"Программирование"; \
    \n"Практика" """
    return text


def in_list(msg: str, words: list):
    for word in msg.split(' '):
        if word in words:
            return True
    return False


def main():
    longpoll = VkLongPoll(vk)

    # hello_command_keys = ['привет', 'hello']
    help_command_keys = ['справка', 'помощь', 'help', 'команды', 'команда']
    programming_command_keys = ['программирование', 'программирования',
                                'программированию', 'программирование',
                                'программированием', 'программировании',
                                'прога',
                                'домашнее задание по программированию']
    practice_command_keys = ['практика', 'практики', 'практике',
                             'практику', 'практикой', 'практике',
                             'домашнее задание по практике',
                             'practice']

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text
            msg = formating(msg)
            user_id = event.user_id
            if in_list(msg, help_command_keys):
                print("Текст: ", msg)
                write_msg(user_id, 'Привет\n' + get_help_text())

            elif in_list(msg, programming_command_keys):
                print("Текст: ", msg)
                html = get_html(links['programming'])
                mess = parse(html)
                print(mess)
                write_msg(user_id=user_id,
                          s=('Домашнее задание по программированию: ' + mess))

            elif in_list(msg, practice_command_keys):
                print("Текст: ", msg)
                html = get_html(links['practice'])
                mess = parse(html)
                print(mess)
                write_msg(user_id=user_id,
                          s=('Домашнее задание по практике: ' + mess))

            else:
                write_msg(user_id=user_id,
                          s='Такой команды не существует\n' + get_help_text())


if __name__ == '__main__':
    main()
