# Contenu d'une case
VIDE = 0
MARQUE = -1

# Dimensions par défaut du plateau (lignes, colonnes)
M_DEFAUT = 5
N_DEFAUT = 10

# Sauts du cavalier (delta_ligne, delta_colonne)
SAUTS = (
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1),
)

# Valeurs de fin de partie utilisées par les IA
GAIN = 1000
PERTE = -1000
NUL = 0

# Affichage
LARGEUR_MAX = 900
HAUTEUR_MAX = 600
DELAI_COUP_MS = 400
COULEUR_CASE_LIBRE = "#f4f1e8"
COULEUR_CASE_MARQUEE = "#555555"
COULEUR_PION_1 = "#2a6fdb"
COULEUR_PION_2 = "#d63b2f"
COULEUR_CIBLE = "#ffd24a"
COULEUR_DERNIER_COUP = "#9fd8a0"
