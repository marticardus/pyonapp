class OnAppJsonObject(object):
    def __init__(self, json = None, name = None):
        if json and name:
            if name in json:
                json = json[name]

            for name, value in json.items():
                if hasattr(self, name):
                    setattr(self, name, value)

