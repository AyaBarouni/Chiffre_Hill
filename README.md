# Cryptographie symétrique - Chiffre de Hill

Implémentation en Python du Chiffre de Hill : chiffrement d'un message par multiplication matricielle dans $\mathbb{Z}/26\mathbb{Z}$.

---

## Contexte

Le Chiffre de Hill est un système de chiffrement symétrique classique introduit par Lester S. Hill en 1929. Contrairement aux chiffrements par substitution simple (comme César), il opère sur des blocs de lettres grâce à l'algèbre linéaire, ce qui lui confère une propriété importante en cryptographie : la diffusion. Il constitue l'un des premiers exemples de chiffrement exploitant des structures mathématiques avancées.

---

## Principe mathématique

Le message est découpé en blocs de $n$ lettres, convertis en vecteurs numériques (A = 0, B = 1, ..., Z = 25). Chaque bloc $\mathbf{v}$ est chiffré par :

$$\mathbf{c} = K \cdot \mathbf{v} \pmod{26}$$

Où $K$ est une matrice carrée $n \times n$ choisie comme clé secrète. Pour déchiffrer, on applique l'opération inverse :

$$\mathbf{v} = K^{-1} \cdot \mathbf{c} \pmod{26}$$

---

## Condition d'inversibilité de la clé

On ne peut pas choisir n'importe quelle matrice comme clé. Pour que le déchiffrement soit possible, $K$ doit être inversible dans $\mathbb{Z}/26\mathbb{Z}$, ce qui exige :

$$\text{pgcd}\left(\det(K), 26\right) = 1$$

Le déterminant doit être premier avec 26. Si cette condition n'est pas respectée, plusieurs messages clairs produisent le même message chiffré, ce qui rend le déchiffrement ambigu et impossible.


**Clé utilisée dans ce projet :**

$$
K = \begin{bmatrix} 3 & 3 \\ 2 & 5 \end{bmatrix}, \quad
\det(K) = 9, \quad \gcd(9, 26) = 1 \checkmark
$$

---

## Diffusion de Shannon

L'un des principes fondamentaux de la cryptographie moderne (Shannon, 1949) est la diffusion : modifier un seul caractère du message clair doit modifier l'intégralité du bloc chiffré correspondant, rendant l'analyse statistique très difficile pour un attaquant.

| Message clair | Modification | Message chiffré |
|---|---|---|
| `HI` | -- | `TC` |
| `HJ` | I → J (+1 dans l'alphabet) | `WH` |

Changer uniquement la deuxième lettre modifie les deux lettres du bloc de sortie, car la multiplication matricielle mélange les contributions de chaque caractère sur l'ensemble du bloc.

---

## Fonctionnement

1. Le message est converti en vecteurs numériques (blocs de 2 lettres)
2. Si la longueur n'est pas divisible par 2, des `X` sont ajoutés en fin de message
3. Le programme vérifie automatiquement la validité de la clé ($\pgcd(\det(K), 26) = 1$)
4. Chaque bloc est multiplié par la matrice clé modulo 26
5. Le résultat est retraduit en lettres

---

## Utilisation

```bash
python hill.py
```

```
Clé valide : det(K) = 9, pgcd(9, 26) = 1 ✓
Entrez le message à chiffrer : HELLO
------------------------------
Message d'origine : HELLO
Message chiffré   : TCZGI
------------------------------
```

---

## Structure du code

| Fonction | Rôle |
|---|---|
| `texte_en_vecteurs(texte, taille_bloc)` | Convertit le texte en liste de vecteurs numpy |
| `chiffrer_hill(vecteurs, matrice_cle)` | Applique la multiplication matricielle modulo 26 |
| `vecteurs_en_texte(vecteurs_chiffres)` | Retraduit les vecteurs en chaîne de caractères |

---

## Technologies

- **Python 3**
- Module : `numpy`

---

## Fichiers du projet

| Fichier | Description |
|---|---|
| `hill.py` | Code source Python |
| `preuve_hill.pdf` | Fiche théorique : condition d'inversibilité, exemple d'échec, diffusion de Shannon |
| `calculs.pdf` | Partie manuscrite : algorithme d'Euclide étendu, matrice adjointe, calcul de $K^{-1}$ |

---

## Ce que j'ai appris

- Comprendre pourquoi le choix de la clé est une contrainte mathématique forte : un mauvais déterminant crée des collisions, ce qui rend le déchiffrement structurellement impossible
- Relier le principe de diffusion de Shannon à un comportement concret et observable du chiffrement matriciel
- Manipuler des matrices et des vecteurs avec `numpy` pour des calculs arithmétiques modulo $n$
- Gérer la robustesse du programme : vérification automatique de la validité de la clé avec `math.gcd` avant tout chiffrement, plutôt que de laisser l'erreur survenir silencieusement