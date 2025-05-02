class DB:
    class DoesnotExists(Exception):
        pass

    def __init__(self, data):
        self.__db_data = data

    def query_user(self, user):
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
            "nostr": "npub1mk6ht4a96tda4mzdkanjnzcznew3znv6tmmapwj3q0ne2ek8rj5q8vpf5q",
        },
        "bitcoin": {
            "address": "bc1qft4764g468c09rzv6huzjnzcfelzrva9mcjk75",
            "xpub": None,
            "lightning_address": "aviv@paysats.online",
            "silent_payments": None,
        },
    }