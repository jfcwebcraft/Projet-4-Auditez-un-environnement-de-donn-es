import sqlite3
import os

# Chemin de la base de données SQLite à créer
# On place la base à la racine du projet pour qu'elle soit partagée entre les exercices
# Chemin de la base de données SQLite
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "supersmartmarket.db")


def init_db() -> None:
    """
    Crée la structure complète de la base de données SuperSmartMarket.
    On repart d'une base vide à chaque exécution pour garantir un état contrôlé.
    Architecture : Modèle en étoile avec table de traçabilité (Logs).
    """
    # On supprime l'ancienne base pour repartir sur un environnement tout propre
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"[INFO] Ancienne base supprimée : {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("[INFO] Activation de l'intégrité référentielle (clés étrangères)...")
    # SQLite ne les active pas par défaut, c'est une mesure de sécurité importante
    cursor.execute("PRAGMA foreign_keys = ON;")

    print("[INFO] Création de la structure en étoile (tables de dimensions)...")

    # --- DIMENSION : Produits ---
    cursor.execute('''
        CREATE TABLE Dim_Produits (
            EAN             INTEGER PRIMARY KEY,
            categorie       TEXT,
            Rayon           TEXT,
            Libelle_produit TEXT,
            prix            REAL CHECK(prix > 0)
        )
    ''')
    print("  -> Table Dim_Produits créée.")

    # --- DIMENSION : Clients ---
    # Note : la colonne est CUSTOMER_ID dans la BDD, malgré la faute CUSTUMER_ID dans l'Excel source
    cursor.execute('''
        CREATE TABLE Dim_Clients (
            CUSTOMER_ID     TEXT PRIMARY KEY,
            date_inscription TEXT
        )
    ''')
    print("  -> Table Dim_Clients créée.")

    # --- DIMENSION : Employés ---
    # Contient des données sensibles RGPD : hash_mdp et mail
    cursor.execute('''
        CREATE TABLE Dim_Employes (
            id_employe  TEXT PRIMARY KEY,
            employe     TEXT,
            prenom      TEXT,
            nom         TEXT,
            date_debut  INTEGER,
            hash_mdp    TEXT,
            mail        TEXT
        )
    ''')
    print("  -> Table Dim_Employes créée.")

    # --- DIMENSION : Calendrier ---
    # Permet d'analyser les ventes par période (jour, mois, trimestre, etc.)
    cursor.execute('''
        CREATE TABLE Dim_Calendrier (
            date_excel      INTEGER PRIMARY KEY,
            annee           INTEGER,
            mois            INTEGER,
            jour_date       TEXT,
            mois_nom        TEXT,
            annee_mois      INTEGER,
            jour_semaine    INTEGER,
            trimestre       TEXT
        )
    ''')
    print("  -> Table Dim_Calendrier créée.")

    # --- TABLE DE FAITS : Ventes ---
    # C'est le cœur du modèle. Chaque ligne = un produit dans un ticket.
    # Les clés étrangères garantissent l'intégrité référentielle.
    cursor.execute('''
        CREATE TABLE Fact_Ventes (
            ID_BDD          TEXT PRIMARY KEY,
            CUSTOMER_ID     TEXT,
            id_employe      TEXT,
            EAN             INTEGER,
            date_achat_excel INTEGER,
            ID_ticket       TEXT,
            FOREIGN KEY (CUSTOMER_ID)       REFERENCES Dim_Clients (CUSTOMER_ID),
            FOREIGN KEY (id_employe)        REFERENCES Dim_Employes (id_employe),
            FOREIGN KEY (EAN)               REFERENCES Dim_Produits (EAN),
            FOREIGN KEY (date_achat_excel)  REFERENCES Dim_Calendrier (date_excel)
        )
    ''')
    print("  -> Table Fact_Ventes créée.")

    # --- TABLE DE TRAÇABILITÉ : Logs ---
    # Indispensable pour l'audit : chaque insertion/modification/suppression est loguée ici.
    # C'est cette table qui permet d'expliquer le delta de CA de 9 057,29 €.
    cursor.execute('''
        CREATE TABLE Logs (
            id_log      INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user     TEXT,
            date        DATETIME DEFAULT CURRENT_TIMESTAMP,
            id_bdd      TEXT,
            id_produit  INTEGER,
            status      TEXT NOT NULL
        )
    ''')
    print("  -> Table Logs créée.")

    conn.commit()
    conn.close()
    print(f"\n[SUCCÈS] Base de données initialisée : {DB_PATH}")


if __name__ == "__main__":
    init_db()
