import tkinter as tk
from tkinter import messagebox, ttk
import random
import math

# Données statistiques du championnat FC 24
classement = [
    {"Equipe": "Liverpool", "MJ": 34, "V": 22, "N": 6, "P": 6, "DB": "87-39", "Pts": 72},
    {"Equipe": "Milan", "MJ": 34, "V": 22, "N": 4, "P": 8, "DB": "83-45", "Pts": 70},
    {"Equipe": "Galatasaray", "MJ": 34, "V": 19, "N": 6, "P": 9, "DB": "79-53", "Pts": 63},
    {"Equipe": "Bayer 04", "MJ": 34, "V": 20, "N": 3, "P": 11, "DB": "70-43", "Pts": 63},
    {"Equipe": "Brighton et Hove Albion", "MJ": 34, "V": 18, "N": 5, "P": 11, "DB": "73-47", "Pts": 59},
    {"Equipe": "Benfica", "MJ": 35, "V": 17, "N": 6, "P": 12, "DB": "82-68", "Pts": 57},
    {"Equipe": "Sporting Clube de Portugal", "MJ": 35, "V": 17, "N": 5, "P": 13, "DB": "67-66", "Pts": 56},
    {"Equipe": "Olympique de Marseille", "MJ": 35, "V": 15, "N": 10, "P": 10, "DB": "60-54", "Pts": 55},
    {"Equipe": "Real Betis", "MJ": 34, "V": 15, "N": 9, "P": 10, "DB": "63-48", "Pts": 54},
    {"Equipe": "Bergamo Calcio", "MJ": 34, "V": 16, "N": 6, "P": 12, "DB": "82-70", "Pts": 54},
    {"Equipe": "Villarreal", "MJ": 34, "V": 16, "N": 5, "P": 13, "DB": "68-57", "Pts": 53},
    {"Equipe": "AEK Athens", "MJ": 34, "V": 13, "N": 11, "P": 10, "DB": "69-58", "Pts": 50},
    {"Equipe": "Freiburg", "MJ": 34, "V": 14, "N": 7, "P": 13, "DB": "58-45", "Pts": 49},
    {"Equipe": "Feyenoord", "MJ": 35, "V": 13, "N": 8, "P": 14, "DB": "70-65", "Pts": 47},
    {"Equipe": "West Ham United", "MJ": 35, "V": 12, "N": 5, "P": 18, "DB": "44-64", "Pts": 41},
    {"Equipe": "Roma", "MJ": 34, "V": 10, "N": 6, "P": 18, "DB": "65-72", "Pts": 36},
    {"Equipe": "Rangers", "MJ": 34, "V": 8, "N": 10, "P": 16, "DB": "47-76", "Pts": 34},
    {"Equipe": "Toulouse", "MJ": 34, "V": 8, "N": 9, "P": 17, "DB": "40-64", "Pts": 33},
    {"Equipe": "LASK", "MJ": 35, "V": 3, "N": 3, "P": 29, "DB": "34-129", "Pts": 12},
    {"Equipe": "Sparta Praha", "MJ": 35, "V": 0, "N": 0, "P": 35, "DB": "15-105", "Pts": 0},  # Corrigé
]

# Fonctions de prédiction améliorées

def get_team_stats(team_name):
    """Récupère les stats d'une équipe avec gestion d'erreur"""
    if not team_name:
        return None
    for team in classement:
        if team["Equipe"].lower() == team_name.lower():
            return team
    return None

def parse_goals(db_string):
    """Parse les buts avec gestion d'erreur robuste"""
    try:
        if not db_string or db_string == "0-0":
            return 0, 0
        goals_for, goals_against = map(int, db_string.split("-"))
        return max(0, goals_for), max(0, goals_against)
    except (ValueError, AttributeError):
        return 0, 0

def goal_difference(db):
    """Calcule la différence de buts"""
    goals_for, goals_against = parse_goals(db)
    return goals_for - goals_against

def calculate_team_strength(team_data):
    """Calcule la force d'une équipe basée sur plusieurs critères"""
    if not team_data:
        return 0
    
    # Points par match
    points_per_game = team_data["Pts"] / max(team_data["MJ"], 1)
    
    # Pourcentage de victoires
    win_rate = team_data["V"] / max(team_data["MJ"], 1)
    
    # Différence de buts
    goal_diff = goal_difference(team_data["DB"])
    goal_diff_per_game = goal_diff / max(team_data["MJ"], 1)
    
    # Score composite
    strength = (points_per_game * 40) + (win_rate * 30) + (goal_diff_per_game * 10)
    return max(0, strength)

def predict_winner(team1, team2):
    """Prédiction du gagnant avec algorithme amélioré"""
    t1 = get_team_stats(team1)
    t2 = get_team_stats(team2)
    
    if not t1 or not t2:
        return "Équipe(s) introuvable(s)"
    
    strength1 = calculate_team_strength(t1)
    strength2 = calculate_team_strength(t2)
    
    # Ajouter un facteur aléatoire pour simuler l'incertitude du sport
    random_factor = random.uniform(0.8, 1.2)
    strength1 *= random_factor
    
    difference = abs(strength1 - strength2)
    
    if strength1 > strength2:
        confidence = min(95, 50 + (difference * 2))
        return f"{team1} ({confidence:.1f}% de confiance)"
    elif strength2 > strength1:
        confidence = min(95, 50 + (difference * 2))
        return f"{team2} ({confidence:.1f}% de confiance)"
    else:
        return "Match nul (très équilibré)"

def double_chance(team1, team2):
    """Calcule les options de double chance"""
    t1 = get_team_stats(team1)
    t2 = get_team_stats(team2)
    
    if not t1 or not t2:
        return "Données insuffisantes"
    
    strength1 = calculate_team_strength(t1)
    strength2 = calculate_team_strength(t2)
    
    if strength1 > strength2 * 1.2:
        return f"Double chance recommandée: {team1} ou Nul"
    elif strength2 > strength1 * 1.2:
        return f"Double chance recommandée: {team2} ou Nul"
    else:
        return f"Match équilibré: {team1} ou {team2} conseillé"

def btts_prediction(team1, team2):
    """Prédiction Both Teams To Score améliorée"""
    t1 = get_team_stats(team1)
    t2 = get_team_stats(team2)
    
    if not t1 or not t2:
        return "BTTS: Données insuffisantes"
    
    # Analyse des buts marqués et encaissés
    gf1, ga1 = parse_goals(t1["DB"])
    gf2, ga2 = parse_goals(t2["DB"])
    
    # Moyennes par match
    avg_goals_for_t1 = gf1 / max(t1["MJ"], 1)
    avg_goals_for_t2 = gf2 / max(t2["MJ"], 1)
    avg_goals_against_t1 = ga1 / max(t1["MJ"], 1)
    avg_goals_against_t2 = ga2 / max(t2["MJ"], 1)
    
    # Probabilité de marquer pour chaque équipe
    prob_t1_scores = min(0.9, (avg_goals_for_t1 + avg_goals_against_t2) / 3)
    prob_t2_scores = min(0.9, (avg_goals_for_t2 + avg_goals_against_t1) / 3)
    
    btts_probability = prob_t1_scores * prob_t2_scores * 100
    
    if btts_probability > 60:
        return f"BTTS: OUI ({btts_probability:.1f}% de probabilité)"
    else:
        return f"BTTS: NON ({btts_probability:.1f}% de probabilité)"

def predict_total_goals(team1, team2):
    """Prédiction du nombre total de buts dans le match"""
    t1 = get_team_stats(team1)
    t2 = get_team_stats(team2)
    
    if not t1 or not t2:
        return "Prédiction buts: Impossible"
    
    gf1, ga1 = parse_goals(t1["DB"])
    gf2, ga2 = parse_goals(t2["DB"])
    
    avg_goals_t1 = (gf1 + ga1) / max(t1["MJ"], 1) / 2
    avg_goals_t2 = (gf2 + ga2) / max(t2["MJ"], 1) / 2
    
    predicted_total = avg_goals_t1 + avg_goals_t2
    
    if predicted_total > 3:
        return f"Plus de 2.5 buts attendus ({predicted_total:.1f} buts prédits)"
    else:
        return f"Moins de 2.5 buts attendus ({predicted_total:.1f} buts prédits)"

def get_head_to_head_advice(team1, team2):
    """Conseils basés sur les statistiques des équipes"""
    t1 = get_team_stats(team1)
    t2 = get_team_stats(team2)
    
    if not t1 or not t2:
        return "Analyse impossible"
    
    advice = []
    
    # Conseil sur la forme
    if t1["Pts"] > t2["Pts"] + 10:
        advice.append(f"📈 {team1} en meilleure forme générale")
    elif t2["Pts"] > t1["Pts"] + 10:
        advice.append(f"📈 {team2} en meilleure forme générale")
    
    # Conseil sur l'attaque/défense
    gf1, ga1 = parse_goals(t1["DB"])
    gf2, ga2 = parse_goals(t2["DB"])
    
    if gf1 > gf2 * 1.3:
        advice.append(f"⚽ {team1} a une meilleure attaque")
    elif gf2 > gf1 * 1.3:
        advice.append(f"⚽ {team2} a une meilleure attaque")
    
    if ga1 < ga2 * 0.7:
        advice.append(f"🛡️ {team1} a une meilleure défense")
    elif ga2 < ga1 * 0.7:
        advice.append(f"🛡️ {team2} a une meilleure défense")
    
    return " | ".join(advice) if advice else "Match très équilibré"

# Interface graphique améliorée
def create_gui():
    def show_prediction():
        team1 = combo1.get()
        team2 = combo2.get()
        
        if not team1 or not team2:
            messagebox.showwarning("Attention", "Veuillez sélectionner les deux équipes")
            return
            
        if team1 == team2:
            messagebox.showwarning("Erreur", "Veuillez choisir deux équipes différentes")
            return

        # Effacer les résultats précédents
        for widget in result_frame.winfo_children():
            widget.destroy()

        # Calculs des prédictions
        gagnant = predict_winner(team1, team2)
        dc = double_chance(team1, team2)
        btts_result = btts_prediction(team1, team2)
        total_goals = predict_total_goals(team1, team2)
        advice = get_head_to_head_advice(team1, team2)

        # Affichage des résultats avec style
        ttk.Label(result_frame, text="🏆 RÉSULTATS DE LA PRÉDICTION", 
                 font=("Verdana", 12, "bold")).pack(pady=(10, 5))
        
        ttk.Separator(result_frame, orient='horizontal').pack(fill='x', pady=5)
        
        ttk.Label(result_frame, text=f"🥇 Gagnant prédit: {gagnant}", 
                 font=("Verdana", 10)).pack(pady=2)
        
        ttk.Label(result_frame, text=f"🎯 {dc}", 
                 font=("Verdana", 10)).pack(pady=2)
        
        ttk.Label(result_frame, text=f"⚽ {btts_result}", 
                 font=("Verdana", 10)).pack(pady=2)
        
        ttk.Label(result_frame, text=f"📊 {total_goals}", 
                 font=("Verdana", 10)).pack(pady=2)
        
        ttk.Separator(result_frame, orient='horizontal').pack(fill='x', pady=5)
        
        ttk.Label(result_frame, text=f"💡 Conseils: {advice}", 
                 font=("Verdana", 9), wraplength=450).pack(pady=5)

    def clear_results():
        for widget in result_frame.winfo_children():
            widget.destroy()
        combo1.set("")
        combo2.set("")

    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("🏆 Prédicteur FC 24 - Version Pro")
    root.geometry("600x700")
    root.configure(bg="#f0f4f8")

    # Configuration des styles
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Title.TLabel", background="#f0f4f8", foreground="#1a365d", 
                   font=("Verdana", 16, "bold"))
    style.configure("TLabel", background="#f0f4f8", foreground="#2d3748", 
                   font=("Verdana", 10))
    style.configure("TButton", font=("Verdana", 11), padding=8)
    style.configure("TCombobox", font=("Verdana", 11))

    # Titre principal
    title_label = ttk.Label(root, text="⚽ PRÉDICTEUR FC 24 ⚽", style="Title.TLabel")
    title_label.pack(pady=20)

    # Frame principal
    main_frame = ttk.Frame(root)
    main_frame.pack(padx=20, pady=10, fill='both', expand=True)

    # Sélection des équipes
    ttk.Label(main_frame, text="🏠 Équipe Domicile:", font=("Verdana", 11, "bold")).pack(pady=(10, 5))
    combo1 = ttk.Combobox(main_frame, values=[t["Equipe"] for t in classement], 
                         font=("Verdana", 11), width=35, state="readonly")
    combo1.pack(pady=5)

    ttk.Label(main_frame, text="🚌 Équipe Extérieur:", font=("Verdana", 11, "bold")).pack(pady=(15, 5))
    combo2 = ttk.Combobox(main_frame, values=[t["Equipe"] for t in classement], 
                         font=("Verdana", 11), width=35, state="readonly")
    combo2.pack(pady=5)

    # Boutons
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=20)

    predict_button = ttk.Button(button_frame, text="🔍 PRÉDIRE LE MATCH", 
                               command=show_prediction)
    predict_button.pack(side='left', padx=5)

    clear_button = ttk.Button(button_frame, text="🧹 EFFACER", 
                             command=clear_results)
    clear_button.pack(side='left', padx=5)

    # Frame pour les résultats
    result_frame = ttk.LabelFrame(main_frame, text="Résultats", padding=10)
    result_frame.pack(pady=20, fill='both', expand=True)

    # Informations sur l'application
    info_label = ttk.Label(root, text="Prédictions basées sur les statistiques réelles • Version Pro", 
                          font=("Verdana", 8), foreground="#6b7280")
    info_label.pack(pady=10)

    return root

if __name__ == "__main__":
    app = create_gui()
    app.mainloop()