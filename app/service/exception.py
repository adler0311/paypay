

class ObjectNotFound(Exception):
    def __init__(self, obj_name: str, id_: str):
        self.obj_name = obj_name
        self.id_ = id_

    def __str__(self):
        return f'{self.obj_name} not found. id:{self.id_}'


