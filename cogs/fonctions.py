import asyncio
import random
import string

# Symboles pour le mot de passe généré aléatoirement
characters = list(string.ascii_letters + string.digits +
                  "!@#$%^&*()" + "1234567890")


# Toutes les fonctions nécessaire au bon fonctionnement du Bot
def generate_random_password(longueur):
    """Génère un mot de passe aléatoire d'une longueur choisit par l'utilisateur."""
    random.shuffle(characters)

    # picking random characters from the list
    password = []
    for i in range(longueur):
        password.append(random.choice(characters))

    # shuffling the resultant password
    random.shuffle(password)

    # converting the list to string
    # printing the list
    password = ("".join(password))
    return password


def test_bissextile(annee):
    """Retourne True (vrai) si l'année correspond à une année bissextile. Sinon elle retourne False (faux)"""
    annee = annee % 4 == 0 and annee % 100 != 0 or annee % 400 == 0
    return annee


def somme_entier(nombre):
    """Retourne la somme des n premiers entiers"""
    somme = 0
    total = 0

    while somme < nombre:
        somme += 1
        total = total + somme
    return total


def vieillisement(prix, annee, pourcentage):
    """Retourne le nombre d'années où le prix aura diminué de moitié"""

    pourcentage_de_vieillisement = 1 - pourcentage / 100
    prix_de_depart = prix

    while prix > prix_de_depart / 2:
        prix = prix * pourcentage_de_vieillisement
        annee = annee + 1

    return annee


def compare(mot1, mot2):
    """Retourne l'ordre du mot1 par rapport à mot2 dans le dico"""
    resultat = "au même niveau que"
    i = 0
    while resultat == "au même niveau que" and i < len(mot1) and i < len(mot2):
        if mot1[i] < mot2[i]:
            resultat = "avant"
        elif mot1[i] > mot2[i]:
            resultat = "après"
        i += 1
    if len(mot1) != len(mot2):
        if i == len(mot1):
            resultat = "avant"
        if i == len(mot2):
            resultat = "après"
    return resultat


def decversbin(valeurdecimal):
    """Traduit une valeur decimal en une valeur binaire """
    valeurbinaire = 0
    ord = 0
    while valeurdecimal != 0:
        reste = valeurdecimal % 2
        p = 10 ** ord
        valeurbinaire = valeurbinaire + reste * p
        ord = ord + 1
        valeurdecimal = valeurdecimal // 2
    return valeurbinaire


def binversdec(binaire):
    """Traduit une valeur binaire en une valeur decimal"""
    binaire = str(binaire)
    n = len(binaire)
    valeurdecimal = 0
    for i in range(n):
        valeurdecimal = valeurdecimal + int(binaire[n - 1 - i]) * 2 ** i
    return valeurdecimal


# Table de conversion pour l'hexadecimal
conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
                    5: '5', 6: '6', 7: '7',
                    8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
                    13: 'D', 14: 'E', 15: 'F'}


def decimalToHexadecimal(valeurdecimal):
    """Traduit une valeur decimal en une valeur hexadecimal"""
    valeurhexadecimal = ''
    while valeurdecimal > 0:
        remainder = valeurdecimal % 16
        valeurhexadecimal = conversion_table[remainder] + valeurhexadecimal
        valeurdecimal = valeurdecimal // 16

    return valeurhexadecimal


def euroToFrancs(valeurEuro):
    """Convertis des euros en Francs français"""
    valeurFrancs = valeurEuro * 6.5596
    valeurFrancs = round(valeurFrancs, 2)
    return valeurFrancs