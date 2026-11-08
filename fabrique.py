from glouton import Glouton
from human import Human
from mcts import MCTS
from minmax import MinMax
from stupid_bot import StupidBot

NOMS = ["humain", "stupid", "glouton", "minmax", "mcts"]


def creer_joueur(nom, jeu, numero, interface=None, **parametres):
    # crée le joueur et les parametres sont ceux de sa classe
    if nom == "humain":
        return Human(jeu, numero, interface)
    if nom == "stupid":
        return StupidBot(jeu, numero)
    if nom == "glouton":
        return Glouton(jeu, numero)
    if nom == "minmax":
        return MinMax(jeu, numero, **parametres)
    if nom == "mcts":
        return MCTS(jeu, numero, **parametres)
    raise ValueError("Joueur inconnu : " + nom)
