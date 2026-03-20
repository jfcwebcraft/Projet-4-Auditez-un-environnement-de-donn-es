import pandas as pd
import sqlite3
import sys
import os

# Chemin vers le fichier Excel des logs (source : Exercice 2)
# Chemins calculés dynamiquement (portables)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOGS_EXCEL_PATH = os.path.join(BASE_DIR, "data", "Logs.xlsx")
DB_PATH = os.path.join(BASE_DIR, "supersmartmarket.db")


def integrate_logs() -> None:
    """
    Lit le fichier Logs.xlsx et insère son contenu dans la table Logs de la base SQLite.
    Cette étape est essentielle pour l'audit car les logs permettent d'expliquer
    le delta de 9 057,29 euros constaté sur le CA du 14 août 2024.
    """
    # Vérification préalable de l'existence du fichier source
    if not os.path.exists(LOGS_EXCEL_PATH):
        print(f"[ERREUR] Fichier introuvable : {LOGS_EXCEL_PATH}")
        sys.exit(1)

    # Vérification préalable de l'existence de la base de données
    if not os.path.exists(DB_PATH):
        print("[ERREUR] La base de données n'existe pas.")
        print("  -> Exécutez d'abord : python 'Exercice 1/scripts/init_db.py'")
        print("  -> Puis           : python 'Exercice 1/scripts/load_data.py'")
        sys.exit(1)

    try:
        print("[INFO] Lecture du fichier Logs.xlsx (fichier volumineux, patience...)...")
        df_logs = pd.read_excel(LOGS_EXCEL_PATH)
        nb_lignes_brutes = len(df_logs)
        print(f"  -> {nb_lignes_brutes} lignes lues depuis Logs.xlsx.")

        # Nettoyage des noms de colonnes (suppression des espaces parasites)
        df_logs.columns = df_logs.columns.str.strip()

        print(f"  -> Colonnes détectées dans le fichier : {list(df_logs.columns)}")

        # Standardisation des noms de colonnes vers le schéma de la table Logs en BDD
        # On mappe les noms du fichier Excel vers les noms attendus en base
        colonnes_attendues = {
            'id_user':    'id_user',
            'date':       'date',
            'id_ligne':   'id_bdd',
            'detail':     'id_produit',
            'action':     'status',
        }
        # On ne garde que les colonnes dont on a besoin et qui existent
        colonnes_a_garder = {k: v for k, v in colonnes_attendues.items() if k in df_logs.columns}
        df_logs = df_logs[list(colonnes_a_garder.keys())].rename(columns=colonnes_a_garder)

        # Suppression des lignes sans status (données invalides)
        df_logs = df_logs.dropna(subset=['status'])
        nb_lignes_propres = len(df_logs)
        print(f"  -> {nb_lignes_brutes - nb_lignes_propres} lignes écartées (données invalides).")

        print("\n[INFO] Connexion à la base de données SQLite...")
        conn = sqlite3.connect(DB_PATH)

        # On vide la table Logs avant de la repeupler pour éviter les doublons
        conn.execute("DELETE FROM Logs;")
        print("  -> Table Logs vidée avant rechargement.")

        # Insertion des données dans la table Logs
        df_logs.to_sql('Logs', conn, if_exists='append', index=False)

        # --- Rapport de synthèse de l'audit ---
        print("\n" + "="*60)
        print("  RAPPORT DE SYNTHÈSE DE L'INTÉGRATION DES LOGS")
        print("="*60)

        # Répartition par type d'opération
        print("\n  Répartition par type d'opération (status) :")
        df_status = pd.read_sql("SELECT status, COUNT(*) as nb FROM Logs GROUP BY status ORDER BY nb DESC;", conn)
        print(df_status.to_string(index=False))

        # Employés les plus actifs dans les logs
        print("\n  Top 5 des utilisateurs les plus actifs dans les logs :")
        df_users = pd.read_sql("""
            SELECT id_user, COUNT(*) as nb_operations 
            FROM Logs 
            GROUP BY id_user 
            ORDER BY nb_operations DESC 
            LIMIT 5;
        """, conn)
        print(df_users.to_string(index=False))

        # Logs concernant le 14 août 2024 spécifiquement
        print("\n  Logs du 14 août 2024 (date de l'anomalie de CA) :")
        df_14aout = pd.read_sql("""
            SELECT status, COUNT(*) as nb 
            FROM Logs 
            WHERE date LIKE '2024-08-14%' 
            GROUP BY status;
        """, conn)
        print(df_14aout.to_string(index=False))

        print("="*60)

        conn.commit()
        conn.close()
        print(f"\n[SUCCÈS] {nb_lignes_propres} logs intégrés dans la base de données.")

    except Exception as e:
        import traceback
        print(f"\n[ERREUR] Intégration échouée : {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    integrate_logs()
