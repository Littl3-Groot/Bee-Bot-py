import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import random

class Levels:
    def __init__(self):
        self.db = db.reference()

    def add_experience(self, user_id, experience):
        # R�cup�rer le niveau actuel de l'utilisateur
        current_level = self.get_level(user_id)
        
        # Ajouter l'exp�rience
        current_level['experience'] += experience
        
        # V�rifier si l'utilisateur a atteint un nouveau niveau
        if current_level['experience'] >= current_level['next_level']:
            current_level['level'] += 1
            current_level['next_level'] = self.calculate_next_level(current_level['level'])
            current_level['experience'] = 0
            self.db.child('users').child(user_id).child('level').set(current_level)

    def get_level(self, user_id):
        # R�cup�rer le niveau de l'utilisateur depuis la base de donn�es Firebase
        level = self.db.child('users').child(user_id).child('level').get()
        
        # Si l'utilisateur n'a pas encore de niveau, initialiser � 0
        if level is None:
            level = {
                'level': 0,
                'experience': 0,
                'next_level': self.calculate_next_level(0)
            }
            self.db.child('users').child(user_id).child('level').set(level)

        return level

    def calculate_next_level(self, level):
        # Calculer le nombre d'exp�rience n�cessaire pour atteindre le prochain niveau
        return int(100 * (1.5 ** level))

    def get_leaderboard(self, limit=10):
        # R�cup�rer les niveaux de tous les utilisateurs dans la base de donn�es Firebase
        levels = self.db.child('users').order_by_child('level/level').limit_to_last(limit).get()
        
        # Trier les niveaux par ordre d�croissant
        sorted_levels = sorted(levels.items(), key=lambda x: x[1]['level']['level'], reverse=True)

        # Retourner les limit premiers niveaux
        return sorted_levels[:limit]
