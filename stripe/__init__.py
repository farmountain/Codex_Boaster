api_key = ""

class Charge:
    @staticmethod
    def create(**kwargs):
        return {"id": "ch_test", **kwargs}
