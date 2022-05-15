from jjpy.carddb.carddb import CardDB
from . import common

types = [
    "normal",
    "effect",
    "ritual",
    "fusion",
    "synchro",
    "xyz",
    "pendulum-normal",
    "pendulum-effect",
    "link",
    "spell",
    "trap",
]
typeOrder = dict()

for i, value in enumerate(types):
    typeOrder[value] = i

statuses = [
    "Banned",
    "Limited",
    "Semilimited",
    "Unlimited",
]
statusOrder = dict()

for i, value in enumerate(statuses):
    statusOrder[value] = i


def createName(id):
    components = id.split("-")
    year = components[1]
    part = components[2][1:]
    return f"{year} Part {part}"


def mapCard(card):
    types = card["types"]
    _type = ""

    if "Pendulum" in types:
        _type += "pendulum-"
        types.remove("Pendulum")

    _type += types[0]
    _type = _type.lower()

    return {
        "name": card["name"],
        "type": _type,
    }


def mapCards(cards):
    cards = list(map(mapCard, cards))
    def f(c): return (typeOrder[c["type"]], c["name"])
    cards.sort(key=f)
    return cards


def mapChange(change):
    return {
        "cardName": change["card"]["name"],
        "from": change["from"].title(),
        "to": change["to"].title(),
    }


def mapBanlist(banlist):
    result = dict()

    result["id"] = banlist["name"]
    result["name"] = createName(banlist["name"])

    result["categories"] = [
        {
            "name": "Banned",
            "cards": mapCards(banlist["banned"]),
        },
        {
            "name": "Limited",
            "cards": mapCards(banlist["limited"]),
        },
        {
            "name": "Semilimited",
            "cards": mapCards(banlist["semilimited"]),
        },
    ]

    changes = list(map(mapChange, banlist["changes"]))

    def f(ch): return (
        statusOrder[ch["to"]],
        statusOrder[ch["from"]],
        ch["cardName"],
    )
    changes.sort(key=f)

    result["changes"] = changes

    return result


def buildBanlists():
    cardDb = CardDB()
    banlists = common.buildBanlists(cardDb)

    if banlists[0]["name"] == "jj-2002-p0":
        banlists = banlists[1:]

    return list(map(mapBanlist, banlists))
