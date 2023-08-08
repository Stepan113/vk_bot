import wikipedia

wikipedia.set_lang('ru')


def get_description(name: str):
    try:
        s = wikipedia.page(name)
        des = s.summary
        link = s.url
    except:
        des = 'Такой статьи нет'
        link = 'Ссылки тоже нет)'
    return [des, link]
