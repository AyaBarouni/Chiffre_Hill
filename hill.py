import numpy as np
from math import gcd

def texte_en_vecteurs(texte, taille_bloc):
    nombres = [ord(c) - 65 for c in texte.upper() if c.isalpha()]  # On met chaque caractère en majuscule puis on soustrait 65 afin que A=0, B=1, etc. Les caractères non alphabétiques sont ignorés.

    while len(nombres) % taille_bloc != 0:
        nombres.append(23)  # On ajoute des "X" tant que le message n'est pas divisible par la taille du bloc, afin de rendre les multiplications matricielles possibles

    vecteurs = []  # Initialisation de la liste de vecteurs
    for i in range(0, len(nombres), taille_bloc):  # On parcourt les index de 0 jusqu'à la fin avec un pas égal à la taille du bloc
        bloc = np.array(nombres[i : i + taille_bloc])  # On extrait la plage de nombres nécessaire pour former un bloc
        vecteurs.append(bloc)  # On ajoute le bloc à la liste de vecteurs
    return vecteurs


# CHIFFREMENT
def chiffrer_hill(vecteurs, matrice_cle):
    vecteurs_chiffres = []
    for v in vecteurs:  # On parcourt la liste de vecteurs
        produit = np.dot(matrice_cle, v)  # Produit matriciel : K * v
        v_chiffre = produit % 26  # On applique le modulo 26 pour rester dans l'alphabet
        vecteurs_chiffres.append(v_chiffre)
    return vecteurs_chiffres


def vecteurs_en_texte(vecteurs_chiffres):
    caracteres = []
    for v in vecteurs_chiffres:
        for nombre in v:
            caracteres.append(chr(int(nombre) + 65))  # chr(n + 65) : 0 → 'A', 1 → 'B', etc. On convertit en int pour s'assurer que chr() fonctionne correctement
    return "".join(caracteres)  # Colle tous les éléments de la liste pour former une unique chaîne de caractères


# EXÉCUTION
cle = np.array([[3, 3],
                [2, 5]])

# Vérification automatique de la validité de la clé
det = int(round(np.linalg.det(cle)))  # Calcul dynamique du déterminant
if gcd(det % 26, 26) != 1:
    print(f"Erreur : det(K) = {det}, pgcd({det % 26}, 26) ≠ 1. La matrice n'est pas inversible dans Z/26Z.")
    exit()
else:
    print(f"Clé valide : det(K) = {det}, pgcd({det % 26}, 26) = 1 ✓")

# Entrée utilisateur
message_clair = input("Entrez le message à chiffrer : ")

# 1. Transformation en vecteurs
v_clairs = texte_en_vecteurs(message_clair, 2)

# 2. Application de la matrice (Chiffrement)
v_chiffres = chiffrer_hill(v_clairs, cle)

# 3. Traduction en lettres
message_chiffre = vecteurs_en_texte(v_chiffres)

print("-" * 30)
print(f"Message d'origine : {message_clair.upper()}")
print(f"Message chiffré   : {message_chiffre}")
print("-" * 30)