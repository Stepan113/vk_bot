# photo{}_{}.format(upload_image['owner_id'],upload_image['id'])
# 'attachment':','.join(attachments)
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import token
import add_game
import get_all_game
import select_user
from check_user import check_user
from check_link_on_game import check_link_on_games
from add_user import add_player
from select_all_user import select_all_user
from add_game import add_game


def write_message(user_id_, message_):
    vk.method('messages.send', {'user_id': user_id_,
                                'message': message_,
                                'random_id': get_random_id()})


def image_message(user_id_, attachments):
    vk.method('messages.send', {'user_id': user_id_,
                                'attachment': ','.join(attachments),
                                'random_id': get_random_id()})


class FSM:
    def __init__(self):
        self.name = None
        self.active_bot = 'ab'
        self.start_reg = 'sr'
        self.name_before_check = 'nbc'
        self.link_before_check = 'lbc'
        self.successful_registration = 'sr'

        self.get_player = 'gp'
        self.s_get_game = 'sgg'
        self.get_game = 'gg'
        self.get_all_game = 'gal'

        self.state = None
        self.active_state = None

    def update(self):
        self.active_state = self.state

    def active_bot_(self):
        self.state = self.active_bot

    def start_reg_(self, user_id_: int):
        message = 'Введите имя игрока'
        write_message(user_id_=user_id_, message_=message)
        self.state = self.name_before_check

    def check_name(self, name: str, user_id_: int):
        if all([x not in '0123456789' for x in name]) and len(name) > 3 and check_user(name):
            self.state = self.link_before_check
            self.name = name
            add_player(name=name)
            message = 'Введите ссылку на игру'
        else:
            message = 'Имя не должно содержать числа и должно содержать хотя-бы 3 символа'
            self.state = self.name_before_check
        write_message(user_id_=user_id_, message_=message)

    def check_link(self, link: str, user_id_: int):
        if link.startswith('http://') and check_link_on_games(link=link):
            add_game(name=self.name, link_on_game=link)
            self.state = self.active_bot
            message = 'Вы успешно зарегистрировались!'
        else:
            message = "Ссылка должна начинаться с 'http://'"
            self.state = self.link_before_check
        write_message(user_id_=user_id_, message_=message)

    def s_get_player_(self, user_id_: int):
        self.state = self.get_player
        message = 'Введите имя игрока'
        write_message(user_id_=user_id_, message_=message)

    def get_player_(self, user_id_: int, name: str):
        if not check_user(user=name):
            self.state = self.active_bot
            for i in select_user.select_user(name=name)[0]:
                message = str(i) + ' ' + str(select_user.select_user(name=name)[0].get(i))
                write_message(user_id_=user_id_, message_=message)
            for i in select_user.select_user(name=name)[1]:
                message = i
                write_message(user_id_=user_id_, message_=message)
        else:
            message = 'Такого игрока нет'
            self.state = self.get_player
            write_message(user_id_=user_id_, message_=message)

    def s_get_game_(self, user_id_: int):
        self.state = self.s_get_game
        message = 'Введите имя игрока, кому хотите добавить партию'
        write_message(user_id_=user_id_, message_=message)

    def check_name_for_game(self, name: str, user_id_: int):
        if not check_user(user=name):
            self.state = self.get_game
            self.name = name
            message = "Введите ссылку на игру"
        else:
            message = 'Такого игрока нет'
            self.state = self.s_get_game
        write_message(user_id_=user_id_, message_=message)

    def get_game_(self, link: str, user_id_: int):
        if check_link_on_games(link=link) and link.startswith('http://'):
            self.state = self.active_bot
            add_game(name=self.name, link_on_game=link)
            message = 'Ссылка успешно добавлена!'
        else:
            message = 'Такая ссылка уже есть/Неправильный ввод данных(http://)'
            self.state = self.get_game
        write_message(user_id_=user_id_, message_=message)

    def s_get_all_game(self, user_id_: int):
        message = 'Введите имя игрока'
        write_message(user_id_=user_id_, message_=message)
        self.state = self.get_all_game

    def get_all_game_(self, user_id_: int, name: str):
        self.state = self.active_bot
        if not check_user(user=name):
            for i in get_all_game.get_all_games(name=name):
                message = i
                write_message(user_id_=user_id_, message_=message)
        elif check_user(user=name):
            message = 'Такого игрока нет'
            write_message(user_id_=user_id_, message_=message)
            self.state = self.get_all_game
        else:
            message = 'У игрока нет ссылок на партии'
            write_message(message_=message, user_id_=user_id_)


token = token.token
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
# keyboard = VkKeyboard(one_time=False)
upload = vk_api.VkUpload(vk)
image = 'C:/Users/frens/PycharmProjects/vk_bot/test-1-.jpeg'
link_on_tg = 'https://t.me/shaman_stepan'

fsm = FSM()
fsm.state = fsm.active_bot
fsm.update()

# def add_keyboard():
#     keyboard.add_button('Добавить игрока', color=VkKeyboardColor.PRIMARY)
#     keyboard.add_line()
#     keyboard.add_button('Пока', color=VkKeyboardColor.NEGATIVE)
#     keyboard.add_line()
#     keyboard.add_button('Показать игрока', color=VkKeyboardColor.POSITIVE)
#     keyboard.add_line()
#     keyboard.add_button('Показать игроков', color=VkKeyboardColor.POSITIVE)
#     keyboard.add_line()
#     keyboard.add_button("Добавить партию", color=VkKeyboardColor.POSITIVE)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_message = event.text.lower()
        user_id = event.user_id
        print(user_message)
        if user_message == 'начать' and fsm.active_state == fsm.active_bot:
            message = f"""
                    Приветствую тебя, новый пользователь!
                    Бот максимально сырой, но скоро будут обновления.
                    Версия бота-1.0.0
                    Примерная дата релиза готового бота-1 сентября 2023 года вот здесь 
                    Свои идеи по улучшению бота кидать сюда {link_on_tg}
                    Что умеет этот бот:
                    - Добавить игрока-команда добавляет шахматиста, а также его описание из википедии и одну ссылку на партию
                    - Добавить партию-добавляет партию к коллекции шахматиста, ели он есть в бд
                    - Показать игроков-показывает всех игроков, занесенных в бд
                    - Показать игрока-показывает определенного игрока, его описание и первые три партии
                    - Показать партии-показывает все партии определенного игрока!!!!!!!!!!!
                    - Пока-Очевидно. Взламывает пентагон"""
            write_message(user_id_=user_id, message_=message)
        elif user_message == 'добавить игрока' and fsm.active_state == fsm.active_bot:
            fsm.start_reg_(user_id_=user_id)
            fsm.update()

        elif fsm.active_state == fsm.name_before_check:
            fsm.check_name(name=user_message, user_id_=user_id)
            fsm.update()

        elif fsm.active_state == fsm.link_before_check:
            fsm.check_link(link=user_message, user_id_=user_id)
            fsm.update()

        elif user_message == 'пока' and fsm.active_state == fsm.active_bot:
            message = 'Взлом пентагона\n' \
                      'Пока'
            write_message(user_id_=user_id, message_=message)
            exit()

        elif user_message == 'показать игроков' and fsm.active_state == fsm.active_bot:
            i = 1
            for message in select_all_user():
                write_message(user_id_=user_id, message_=f"{i}. " + message)
                i += 1

        elif user_message == 'показать игрока' and fsm.active_state == fsm.active_bot:
            fsm.s_get_player_(user_id_=user_id)
            fsm.update()

        elif fsm.active_state == fsm.get_player:
            fsm.get_player_(user_id_=user_id, name=user_message)
            fsm.update()

        elif user_message == 'добавить партию' and fsm.active_state == fsm.active_bot:
            fsm.s_get_game_(user_id_=user_id)
            fsm.update()

        elif fsm.active_state == fsm.s_get_game:
            fsm.check_name_for_game(name=user_message, user_id_=user_id)
            fsm.update()

        elif fsm.active_state == fsm.get_game:
            fsm.get_game_(link=user_message, user_id_=user_id)
            fsm.update()

        elif fsm.active_state == fsm.active_bot and user_message == 'показать партии':
            fsm.s_get_all_game(user_id_=user_id)
            fsm.update()

        elif fsm.active_state == fsm.get_all_game:
            fsm.get_all_game_(name=user_message, user_id_=user_id)
            fsm.update()

        else:
            message = 'Я тебя не понимаю'
            write_message(user_id_=user_id, message_=message)
