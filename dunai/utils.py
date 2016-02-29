# coding=utf-8
import re


def stripped(s):
    return '\n'.join([line.strip() for line in s.strip().split('\n')])


def is_cyrillic(s):
    latin_count = 0
    cyrillic_count = 0

    for char in s:
        if ord(char) > 255:
            cyrillic_count += 1
        elif char.isalpha():
            latin_count += 1

    return cyrillic_count > latin_count


def is_ukrainian(s):
    ukrainian_count = 0
    russian_count = 0

    for char in s:
        if char in (u'і', u'є', u'ї', u"ґ"):
            ukrainian_count += 1
        elif char in (u'ы', u'э', u'ё', u'ъ'):
            russian_count += 1

    return ukrainian_count > russian_count


def detect_latin(s):
    counts = dict(
        en=len(re.findall(r'\b(an|the|or|and|in|is)\b', s)),
        de=len(re.findall(r'\b(die|der|dem|den|das|auf|zu|des)\b', s)),
        fr=len(re.findall(r'\b(le|la|les|un|une|au|de)\b', s))
    )

    if counts['en'] == counts['de'] == counts['fr']:
        return 'en'

    return sorted(counts.items(), key=lambda x: -x[1])[0][0]


def detect_language(s):
    if is_cyrillic(s):
        if is_ukrainian(s):
            return 'uk'
        else:
            return 'ru'
    else:
        return detect_latin(s)


# print detect_language(u'Це - тестова стаття. В ній є декілька латинських символів - "Right Here", наприклад.')
# print detect_language(u'The definite article agrees with a specific noun in gender and number. Like other articles (indefinite, partitive) they present a noun. In English, the definite article is always the (the noun). Unlike English, the French definite article is used also in a general sense, a general statement, or feeling about an idea or thing.')
# print detect_language(u'''À défaut de bonnes nouvelles, Michel Platini n’a pas manqué de soutien ces derniers jours. L’ex-président de l’UEFA, candidat déclaré à la tête de la Fifa mais suspendu de toute activité liée au football par l’instance, a reçu celui du gouvernement français, mardi 22 décembre. Une prise de position incarnée par le ministre français des Sports Patrick Kanner, qui s’est exprimé sur la radio Europe 1.
#
# "Moi je soutiens le président de l'UEFA, même s'il est suspendu, parce que je l'ai vu fonctionner dans le cadre de l'Euro-2016, je trouvais qu'il était vraiment en capacité de pouvoir remettre de l'ordre au sein de la Fifa", a déclaré le ministre, en référence au verdict rendu lundi 21 décembre par la commission d’éthique de la Fifa.
#
# La justice interne Fifa était appelée à se prononcer sur un paiement controversé effectué par l’ex-président de l’instance Sepp Blatter à l’endroit de l’ancien numéro 10 des Bleus. Un versement de 1,8 million d’euros, effectué en 2011 pour une tâche supposément effectuée entre 1998 et 2002, qui a finalement coûté huit années de suspension à Platini et Blatter.''')
