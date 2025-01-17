## Ce qu'il y a à faire

Finir la défintion des classes et réfléchir aux liens qu'il y a entre elles
classes lapin et renard dans le document testcompilation

# Prise de notes pour comprendre le code

lapins : au bout d'un moment l'énergie descend et donc il faut faire disparaître les lapins quand ils ont plus d'énergies
Renard: il faudrait qu'à partir d'un certain temps les renards qui n'ont rien mangé disparaissent
#il faut pouvoir recalculer la vitesse à chaque déplacement des renards

#taille du lapin qui change? ou bien il faut un print? same question pour les renards voir doc collisionchat sous les collisions pour ajouter une condition
faire accouplement des renards

# Critères remplis

Création de plantes
utilisation de ChatGPT afin de faire une boucle pour créer les 700 plantes.

#clamp_ip() permet de faire en sorte que les objets ne sortent pas de l'écran
vient juste après move_ip

# Les collisions avec aide ChatGpt

commentaires de CHatGPT:

Merci pour le code ! Voici comment intégrer la logique pour gérer les collisions entre les renards, les lapins, et les plantes :

1. Détecter les collisions entre les sprites.
2. Si une collision est détectée :
   - Si un renard touche un lapin : le lapin disparaît et le renard gagne de l'énergie.
   - Si un lapin touche une plante : la plante disparaît et le lapin gagne de l'énergie.

Je vais ajouter ces fonctionnalités au code tout en incluant des explications détaillées pour chaque ajout.

J'ai ajouté les fonctionnalités suivantes :

1. **Groupes spécifiques pour les plantes, lapins et renards :**

   - Les plantes sont dans le groupe `self.plants`.
   - Les lapins sont dans le groupe `self.lapins`.
   - Les renards sont dans le groupe `self.renards`.

2. **Gestion des collisions :**

   - Les lapins mangent les plantes (les plantes disparaissent après une collision).
   - Les renards mangent les lapins (les lapins disparaissent après une collision).

3. **Placeholders pour l'énergie :**
   - J'ai ajouté des commentaires pour indiquer où intégrer une logique d'énergie si nécessaire.




code durée de vie
le problème vient de 'groupe.copy'
# durée de vie 
        # Supprimer les entités mortes
        for groupe in [self.lapins, self.renards]:
            for entite in groupe.copy():
                if entite.energie <= 0 or entite.age >= entite.age_max:
                    groupe.remove(entite)
                    self.__actors_sprites.remove(entite)

      #durée de vie 
        for entite_type, params in ENTITES.items():
            for _ in range(params["nombre"]):
                position = pygame.Vector2(randint(0, WINDOW_SIZE[0] - 10), randint(0, WINDOW_SIZE[1] - 10))
                speed = pygame.Vector2(randint(-params["vitesse"], params["vitesse"]), randint(-params["vitesse"], params["vitesse"]))
                energie = params["energie_initiale"]
                energie_max = params["energie_max"]
                age_max = params["age_max"]
                reproduction_range = params["reproduction"]

                if entite_type == "Plante":
                    actor = Plante(position, speed, energie, energie_max, age_max)
                    ActorSpriteDrivenBySpeed(self.__screen, actor, "green", [self.plants, self.__actors_sprites])
                elif entite_type == "Lapin":
                    actor = Lapin(position, speed, energie, energie_max, age_max, reproduction_range)
                    ActorSpriteDrivenByRandom(self.__screen, actor, "white", [self.lapins, self.__actors_sprites])
                elif entite_type == "Renard":
                    actor = Renard(position, speed, energie, energie_max, age_max, reproduction_range)
                    ActorSpriteDrivenByRandom(self.__screen, actor, "red", [self.renards, self.__actors_sprites])  

              




              ''' collisions = pygame.sprite.groupcollide(self.lapins, self.lapins, False, False)
        for lapin1, lapins_touches in collisions.items():
            for lapin2 in lapins_touches:
                if lapin1 != lapin2 and lapin1._actor.energie > 15 and lapin2._actor.energie > 15:
            # Créez un nouveau lapin
                    num_new_lapins= randint(1,3)
                    for _ in range(num_new_lapins):
                        position = pygame.Vector2(randint(0, WINDOW_SIZE[0] - 10), randint(0, WINDOW_SIZE[1] - 10))
                        speed = pygame.Vector2(randint(-1, 1), randint(-1, 1))
                        energie = 10  # Énergie initiale du nouveau lapin
                        energie_max = 20
                        actor = Actor(position, speed, energie, energie_max)
                        ActorSpriteDrivenByRandom(self.__screen, actor, "yellow", [self.lapins, self.__actors_sprites])
            
            # Réduisez l'énergie des parents
                        lapin1._actor.energie -= 5
                        lapin2._actor.energie -= 5

# Renards se reproduisent
 collisions = pygame.sprite.groupcollide(self.renards, self.renards, False, False)
        for renard1, renards_touches in collisions.items():
            for renard2 in renards_touches:
                if renard1 != renard2 and renard1._actor.energie > 30 and renard2._actor.energie > 30:
            # Créez un nouveau renard
                    num_new_renards= randint(1,5)
                    for _ in range(num_new_renards):
                        position = pygame.Vector2(randint(0, WINDOW_SIZE[0] - 10), randint(0, WINDOW_SIZE[1] - 10))
                        speed = pygame.Vector2(randint(-2, 2), randint(-2, 2))
                        energie = 15  # Énergie initiale du nouveau renard
                        energie_max = 50
                        actor = Actor(position, speed, energie, energie_max)
                        ActorSpriteDrivenByRandom(self.__screen, actor, "orange", [self.renards, self.__actors_sprites])
            
            # Réduisez l'énergie des parents
                        renard1._actor.energie -= 10
                        renard2._actor.energie -= 10'''






                          # Plantes
        '''for _ in range(700): 
            position = pygame.Vector2(randint(0, WINDOW_SIZE[0]-10), randint(0, WINDOW_SIZE[1]-10))
            speed= pygame.Vector2(0,0)
            plante= Plante(position,speed)
            ActorSpriteDrivenBySpeed(self.__screen, plante, "green", [self.plants, self.__actors_sprites])

        # Lapins
        for _ in range(520):
            position = pygame.Vector2(randint(0, WINDOW_SIZE[0] - 10), randint(0, WINDOW_SIZE[1] - 10))
            speed = pygame.Vector2(randint(-1,1), randint(-1,1))
            energie = 10
            energie_max = 20
            lapin = Lapin(position,speed,energie,energie_max)
            ActorSpriteDrivenByRandom(self.__screen, lapin, "white", [self.lapins, self.__actors_sprites])
            
            energie_min = 0

        # Renards
        for _ in range(22): 
            position = pygame.Vector2(randint(0, WINDOW_SIZE[0]-10), randint(0, WINDOW_SIZE[1]-10))
            speed= pygame.Vector2 (randint(-2,2),randint(-2,2))
            energie = 25
            energie_max = 50
            renard= Renard(position, speed,energie,energie_max)
            ActorSpriteDrivenByRandom(self.__screen, renard, "red", [self.renards, self.__actors_sprites])
            
            energie_min = 0'''


              # Handle collisions
        # Lapins eat plants
        #collisions = pygame.sprite.groupcollide(self.lapins, self.plants, False, True)
        #for lapin in collisions:
            #lapin._actor.change_energie(10)
          # lapin.energie += 10 
        #taille du lapin qui change? ou bien il faut un print? same question pour les renards

        # Renards eat lapins
       # collisions = pygame.sprite.groupcollide(self.renards, self.lapins, False, True)
        #for renard in collisions:
            # Add logic to increase renard energy here (not yet implemented)
            #renard._actor.change_energie(15)




           