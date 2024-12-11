class Vivant:
    _energie_init: int

    def __init__(self, energie_init: int) ->None:
        self._energie_init = energie_init

class Animal(Vivant):
    _energie_min: int
    _energie_max: int

    def __init__(self, energie_min, energie_max)->None:
        self._energie_min = energie_min
        self._energie_max = energie_max

class Renard (Animal):

    def __init__(self,_energie_min, _energie_max, _energie_init) ->None:
        super().__init__(_energie_min, _energie_max,_energie_init)


class Lapin(Animal):

    def __init__(self, _energie_min, energie_max, energie_intit) -> None :
        super().__init__(_energie_min, energie_max, energie_intit)
    

class Plante (Vivant):
    _energie_init: int

    def __init__(self, _energie_init):
        self._energie_init = _energie_init
