import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import random

class Levels:
    def __init__(self):
        self.db = db.reference()

    def add_experience(self, user_id, experience):
        # Récupérer le niveau actuel de l'utilisateur
        current_level = self.get_level(user_id)
        
        # Ajouter l'expérience
        current_level['experience'] += experience
        
        # Vérifier si l'utilisateur a atteint un nouveau niveau
        if current_level['experience'] >= current_level['next_level']:
            current_level['level'] += 1
            current_level['next_level'] = self.calculate_next_level(current_level['level'])
            current_level['experience'] = 0
            self.db.child('users').child(user_id).child('level').set(current_level)

    def get_level(self, user_id):
        # Récupérer les données de l'utilisateur dans la base de données Firebase
        user_ref = self.root.child('users').child(user_id)
        user_data = user_ref.get()

        # Vérifier si l'utilisateur existe dans la base de données Firebase
        if user_data is not None:
            # Mettre à jour l'expérience de l'utilisateur
            user_ref.update({
                'experience': user_data['experience'] + exp
            })
        else:
            # Créer un nouvel utilisateur avec l'expérience donnée
            user_ref.set({
                'experience': exp
            })

    def calculate_next_level(self, level):
        # Calculer le nombre d'expérience nécessaire pour atteindre le prochain niveau
        return int(100 * (1.5 ** level))

    def get_leaderboard(self, limit=10):
        # Récupérer les niveaux de tous les utilisateurs dans la base de données Firebase
        levels = self.db.child('users').order_by_child('level/level').limit_to_last(limit).get()
        
        # Trier les niveaux par ordre décroissant
        sorted_levels = sorted(levels.items(), key=lambda x: x[1]['level']['level'], reverse=True)

        # Retourner les limit premiers niveaux
        return sorted_levels[:limit]
