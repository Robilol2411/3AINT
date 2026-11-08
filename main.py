from concours import Concours
from constantes import M_DEFAUT, N_DEFAUT
from fabrique import NOMS, creer_joueur
from interface import Interface
from manic_minelayers import ManicMinelayers
from partie import Partie


def demander_entier(question, defaut):
    # pose la question jusqu'à obtenir un entier positif
    while True:
        reponse = input(question + " [" + str(defaut) + "] : ")
        if reponse == "":
            return defaut
        if reponse.isdigit() and int(reponse) > 0:
            return int(reponse)
        print("Il faut un entier positif.")


def choisir_joueur(numero):
    # renvoie le choix sous la forme (nom, parametres)
    print("Joueur", numero, ":")
    for i in range(len(NOMS)):
        print(" ", i + 1, "-", NOMS[i])
    choix = demander_entier("Choix", 1)
    while choix > len(NOMS):
        choix = demander_entier("Choix", 1)
    nom = NOMS[choix - 1]

    parametres = {}
    if nom == "minmax":
        parametres["profondeur"] = demander_entier("Profondeur", 4)
        parametres["heuristique"] = demander_entier("Heuristique (1 ou 2)", 1)
    elif nom == "mcts":
        parametres["iterations"] = demander_entier("Itérations", 1000)
        if demander_entier("Politique de simulation (1 = aléatoire, 2 = gloutonne)", 1) == 2:
            parametres["politique"] = "glouton"
    return nom, parametres


def lancer_partie():
    lignes = demander_entier("Nombre de lignes", M_DEFAUT)
    colonnes = demander_entier("Nombre de colonnes", N_DEFAUT)
    choix1 = choisir_joueur(1)
    choix2 = choisir_joueur(2)

    jeu = ManicMinelayers(lignes, colonnes)
    interface = Interface(jeu)
    joueur1 = creer_joueur(choix1[0], jeu, 1, interface, **choix1[1])
    joueur2 = creer_joueur(choix2[0], jeu, 2, interface, **choix2[1])
    Partie(jeu, joueur1, joueur2, interface, True).lancer()
    interface.garder_ouverte()


def lancer_concours():
    parties = demander_entier("Parties par duel", 100)
    print("Combien de joueurs dans le concours ?")
    nombre = demander_entier("Nombre", 3)
    configs = []
    for i in range(nombre):
        choix = choisir_joueur(i + 1)
        if choix[0] == "humain":
            print("Un humain ne peut pas jouer dans un concours, ignoré.")
        else:
            configs.append(choix)
    concours = Concours(parties)
    concours.tournoi(configs)
    concours.afficher()


def main():
    print("=== Manic Minelayers ===")
    print("1 - Jouer une partie (avec fenêtre)")
    print("2 - Concours (sans affichage)")
    if demander_entier("Choix", 1) == 2:
        lancer_concours()
    else:
        lancer_partie()


if __name__ == "__main__":
    main()
