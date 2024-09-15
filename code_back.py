import streamlit as st
import sqlite3
from typing import List, Tuple

# Chemin vers la base de données
db: str = 'C:/Users/there/Documents/GitHub/projetH/PYTHON_SITE_WEB/static/base_donnees.db'

def authenticate_user(email: str, password: str) -> Tuple[bool, str]:
    """
    Authentifie l'utilisateur en vérifiant les informations d'identification dans la base de données.

    Args:
        email (str): L'e-mail de l'utilisateur.
        password (str): Le mot de passe de l'utilisateur.

    Returns:
        Tuple[bool, str]: Un tuple contenant un booléen indiquant si l'authentification a réussi et l'e-mail de l'utilisateur.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute("SELECT email, password FROM Medecin WHERE email=? AND password=?", (email, password))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result is not None, result[0] if result else None  

def fetch_specialties() -> List[Tuple[str]]:
    """
    Récupère les spécialités des médecins depuis la base de données.

    Returns:
        List[Tuple[str]]: Une liste de tuples contenant les spécialités.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute("SELECT specialite FROM Medecin")
    specialites = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return specialites

def fetch_hospitals() -> List[Tuple[str, str, float]]:
    """
    Récupère les hôpitaux depuis la base de données.

    Returns:
        List[Tuple[str, str, float]]: Une liste de tuples contenant les informations des hôpitaux (nom, date, rémunération).
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute("SELECT nom, date, remuneration FROM Hopital")
    hopitaux = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return hopitaux

def create_medecins_enregistres_table() -> None:
    """
    Crée la table 'medecins_enregistres' dans la base de données si elle n'existe pas.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS medecins_enregistres (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT,
                        specialite TEXT,
                        hopital TEXT
                    )''')
    
    conn.commit()
    conn.close()

def save_selections_to_database(email: str, specialite: str, hopital: str) -> None:
    """
    Enregistre les sélections d'un médecin dans la base de données.

    Args:
        email (str): L'e-mail du médecin.
        specialite (str): La spécialité choisie par le médecin.
        hopital (str): L'hôpital choisi par le médecin.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO medecins_enregistres (email, specialite, hopital) VALUES (?, ?, ?)", (email, specialite, hopital))
    
    conn.commit()
    conn.close()

def display_specialties_and_hospitals() -> None:
    """
    Affiche les spécialités et les hôpitaux disponibles pour le médecin.
    """
    st.title("Liste des spécialités")
    st.subheader("Choisissez les spécialités qui vous correspondent :")
    
    email = st.session_state.get("user_email")  # Récupérer l'e-mail stocké dans la session
    
    # Vérifier si des enregistrements existent déjà pour cet utilisateur dans la base de données
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT specialite, hopital FROM medecins_enregistres WHERE email=?", (email,))
    previous_selections = cursor.fetchall()
    conn.close()
    
    if previous_selections:
        st.write("Vos choix précédents :")
        for spec, hosp in previous_selections:
            st.write(f"- Spécialité : {spec}, Hôpital : {hosp}")
    
    specialites = fetch_specialties()
    select_specialite = st.selectbox("Choisissez une spécialité", [s[0] for s in specialites], key="specialite_selec")
    valider_specialite = st.button("Valider spécialité", key="valider_specialite")
    
    if valider_specialite:
        st.session_state["select_specialite"] = select_specialite
        st.write(f"La spécialité choisie est :  {select_specialite}")

    st.title("Liste des hôpitaux")
    st.write("")
    st.subheader("Vous avez ci-dessous une liste des différents hôpitaux disponibles")

    hopitaux = fetch_hospitals()
    hop_select = st.selectbox("Choisissez un hôpital", [hopital[0] for hopital in hopitaux])
    valider_hopital = st.button("Valider hôpital", key="valider_hopital")

    if valider_hopital:
        selected_hopital = next(hopital for hopital in hopitaux if hopital[0] == hop_select)
        
        if st.session_state.get("hop_select") == hop_select:
            st.write("Erreur : Vous avez déjà été enregistré dans cet hôpital.")
        else:
            st.session_state["hop_select"] = hop_select
            st.write(f"Vous avez sélectionner : {hop_select}")
            st.write(f"La date à laquelle vous devez être disponible est le : {selected_hopital[1]}")
            st.write(f"Votre Rémunération : {selected_hopital[2]}")
            
            save_selections_to_database(email, select_specialite, hop_select)
            st.success("Informations enregistrées avec succès !")


def authenticate_and_redirect() -> None:
    """
    Authentifie l'utilisateur et redirige en fonction du résultat de l'authentification.
    """
    st.title("DocRelay")
    st.write("")
    st.subheader("Votre santé, notre priorité!")
    
    st.header("E-mail")
    e_mail = st.text_input("E-mail", key="email_input")

    st.header("Mot de passe")
    password = st.text_input("Mot de passe", type="password", key="password_input")
    
    if st.button("Se connecter"):
        authenticated, email = authenticate_user(e_mail, password)
        if authenticated:
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.experimental_rerun()
        else:
            st.error("Echec de l'authentification")

create_medecins_enregistres_table()

if "authenticated" not in st.session_state:
    authenticate_and_redirect()
else:
    display_specialties_and_hospitals()
