class DB:
    class DoesnotExists(Exception):
        pass

    def __init__(self, data):
        self.__db_data = data

    def query_user(self, user: str) -> dict:
        user = user.lower()
        u = self.__db_data.get("users", {}).get(user)
        if u is None:
            raise self.DoesnotExists()
        return u

server_db_dict = {
    "users":{}
}

server_db_dict["users"]["aviv"] = {
        "contact": {
            "nickname":"aviv",
            "x": "@Aviv__BarEl",
            "email": "aviv@paysats.online",
            "nostr": "nprofile1qqsdmdt467ja9k76a3xmweef3vpfuhg3fkd9aa7shfgs8eu4vmr3e2qpz3mhxue69uhhyetvv9ujuerpd46hxtnfduqs6amnwvaz7tmwdaejumr0ds0trnjy",
        },
        "bitcoin": {
            "address": "bc1qft4764g468c09rzv6huzjnzcfelzrva9mcjk75",
            "lightning_address": "aviv@paysats.online",
            "payment_url": None,
            "silent_payments": None,
        },
    }

server_db_dict["users"]["sni"] = {
        "contact": {
            "nickname":"Satoshi Nakamoto Institute",
            "x": "@NakamotoInst",
            "email": None,
            "nostr": "nprofile1qqs8pvzl39y6h730jnctmfvhrgsj8y2v6wlhqry8juh9dkjvuj8u9pspz3mhxue69uhhyetvv9ujuerpd46hxtnfduqs6amnwvaz7tmwdaejumr0dshlg0u3",
        },
        "bitcoin": {
            "address": None,
            "lightning_address": "sni@primal.net",
            "payment_url": "https://pay.zaprite.com/pl_vNYDp4YBSd",
            "silent_payments": None,
        },
    }

server_db_dict["users"]["oria"] = {
        "contact": {
            "nickname":"Oria",
            "x": None,
            "email": None,
            "nostr": None,
        },
        "bitcoin": {
            "address": None,
            "lightning_address": "toda@walletofsatoshi.com",
            "payment_url": "https://prime-previously-vulture.ngrok-free.app/apps/2B9WcQXU8fNZVsfgcrebWyk7xxqz/pos",
            "silent_payments": None,
        },
    }


# mock user for demo purposes
server_db_dict["users"]["mockuser"] = {
        "contact": {
            "nickname":"Mock User",
            "x": "@mockuser",
            "email": "mock@domain.com",
            "nostr": "npubmockuser",
        },
        "bitcoin": {
            "address": "bc1qmockaddress",
            "lightning_address": "mockmock@primal.net",
            "payment_url": None,
            "silent_payments": "spmockusermockmockmockmockmock",
        },
    }