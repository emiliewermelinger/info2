class Animal:
    _energie_min: int
    _energie_max: int
    pelage : str
    taille: int

    def __init__(self, energie_min, energie_max)->None:
        self._energie_min = energie_min
        self._energie_max = energie_max

    def deplacement(self) ->None:
       pass 
    
    def reproduction(self) ->None:
        pass

    def alimentation(self) ->None:
        pass

class Vivant:
    _energie_init: int
    _vie: int # attention mettre par rapport à chaque sorte dans la classe fille

    def __init__(self, energie_init: int, vie:int) ->None:
        self._energie_init : energie_init
        self._vie : vie

class Renard (Animal, Vivant):
    pelage : str #spécifier le pelage du renard et du lapin
    taille: int

    def __init__(self,_energie_min, _energie_max, _energie_init, _vie, pelage, taille) ->None:
        super().__init__(_energie_min, _energie_max,_energie_init, _vie)
        self.pelage = pelage
        self.taille = taille

    def deplacement(self) ->None:
        pass

    def reproduction(self)-> None:
        pass
    
    def alimentation(self) ->None:
        pass


class Lapin(Animal,Vivant):
    pelage: str
    taille : int

    def __init__(self, _energie_min, energie_max, energie_intit, _vie, pelage, taille) -> None :
        super().__init__(_energie_min, energie_max, energie_intit, _vie,)
        self.pelage = pelage
        self.taille = taille
        
    def etre_mange(self)-> None :
        pass

    

class Plante (Vivant):
    _energie_init: int
    _vie: int

    def __init__(self, _energie_init, _vie):
        self._energie_init = _energie_init
        self._vie = _vie

    def etre_mange(self)-> None :
        pass

