import importlib

from constantes import M_DEFAUT, N_DEFAUT
from human import Human
from interface import Interface
from manic_minelayers import ManicMinelayers
from partie import Partie

# nom du fichier et de la classe de chaque IA
IA = (
    ("stupid_bot", "StupidBot"),
    ("minmax", "MinMax"),
    ("mcts", "MCTS"),
    ("glouton", "Glouton"),
)


def charger_ia() -> dict:
    #Renvoie les classes des IA déjà présentes dans le projet, rangées par nom.
    classes = {}
    for fichier, nom in IA:
        try:
            module = importlib.import_module(fichier)
        except ModuleNotFoundError as erreur:
            # le fichier n'est pas encore la, on l'enleve juste du menu
            if erreur.name != fichier:
                raise
            continue
        classes[nom] = getattr(module, nom)
    return classes


def demander_entier(question: str, minimum: int, defaut: int) -> int:
    #Pose une question jusqu'à avoir un entier valable et le renvoie.
    while True:
        reponse = input(f"{question} [{defaut}] : ").strip()
        if reponse == "":
            return defaut
        if reponse.isdigit() and int(reponse) >= minimum:
            return int(reponse)
        print(f"Il faut un entier supérieur ou égal à {minimum}.")


def demander_parametres(nom: str) -> dict:
    #Demande les paramètres d'une IA et les renvoie dans un dictionnaire.
    parametres = {}
    if nom == "MinMax":
        parametres["profondeur"] = demander_entier("Profondeur", 1, 4)
        parametres["heuristique"] = demander_entier("Heuristique (1 ou 2)", 1, 1)
    elif nom == "MCTS":
        parametres["iterations_max"] = demander_entier("Itérations", 1, 1000)
    return parametres


def choisir_joueur(numero: int, classes: dict) -> tuple[str, dict]:
    #Fait choisir un joueur et renvoie son nom et ses paramètres.
    noms = ["Humain"]
    for nom in classes:
        noms.append(nom)

    print(f"\nJoueur {numero} :")
    for i in range(len(noms)):
        print(f"  {i + 1}. {noms[i]}")

    choix = demander_entier("Ton choix", 1, 1)
    while choix > len(noms):
        print("Ce numéro n'est pas dans la liste.")
        choix = demander_entier("Ton choix", 1, 1)

    nom = noms[choix - 1]
    return nom, demander_parametres(nom)


def creer_joueur(choix: tuple[str, dict], jeu: ManicMinelayers, numero: int,
                 interface: Interface, classes: dict):
    #Crée le joueur choisi dans le menu et le renvoie.
    nom, parametres = choix
    if nom == "Humain":
        return Human(jeu, numero, interface)
    return classes[nom](jeu, numero, **parametres)


def main() -> None:
    #Affiche le menu puis lance la partie.
    classes = charger_ia()
    print("=== Manic Minelayers ===")
    m = demander_entier("Nombre de lignes", 1, M_DEFAUT)
    n = demander_entier("Nombre de colonnes", 2, N_DEFAUT)
    choix1 = choisir_joueur(1, classes)
    choix2 = choisir_joueur(2, classes)

    jeu = ManicMinelayers(m, n)
    interface = Interface(jeu)
    joueur1 = creer_joueur(choix1, jeu, 1, interface, classes)
    joueur2 = creer_joueur(choix2, jeu, 2, interface, classes)

    partie = Partie(jeu, joueur1, joueur2, interface)
    partie.lancer()
    interface.attendre_fermeture()


if __name__ == "__main__":
    main()
