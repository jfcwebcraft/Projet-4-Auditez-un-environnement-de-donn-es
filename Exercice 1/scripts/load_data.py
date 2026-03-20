import pandas as pd
import sqlite3
import sys
import os

# Chemin vers le fichier Excel source (extraction OLAP brute du 14 août 2024)
# Chemins calculés dynamiquement (portables)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EXCEL_PATH = os.path.join(BASE_DIR, "data", "data.xlsx")
LOGS_EXCEL_PATH = os.path.join(BASE_DIR, "data", "Logs.xlsx")
DB_PATH = os.path.join(BASE_DIR, "supersmartmarket.db")

# Note sur les clés étrangères (FK) :
# On DÉSACTIVE les FK pendant le chargement initial car les données source contiennent
# des ventes anonymes (CUSTOMER_ID null ou sans correspondance dans Dim_Clients).
# C'est une pratique standard d'ETL : on charge d'abord les données brutes,
# puis on applique les contraintes pour les nouvelles insertions (via les triggers).


def load_data() -> None:
    """
    Charge l'intégralité des données depuis le fichier Excel source vers la base SQLite.
    Le chargement se fait dimension par dimension, dans l'ordre qui respecte les contraintes
    de clés étrangères, puis la table de faits, et enfin la table de logs.
    Les données sont nettoyées et corrigées à la volée avant insertion.
    """
    try:
        print("[INFO] Ouverture du fichier Excel source (peut prendre quelques secondes)...")
        xl = pd.ExcelFile(EXCEL_PATH)
        conn = sqlite3.connect(DB_PATH)

        # On désactive les FK pendant le chargement initial.
        # Raison : les données source contiennent des ventes anonymes (CUSTOMER_ID
        # null ou non référencé dans Dim_Clients). C'est une anomalie documentée
        # dans le rapport d'audit — pas un bug de notre script.
        # Les FK seront actives pour les nouvelles insertions via les Triggers (Exercice 3).
        conn.execute("PRAGMA foreign_keys = OFF;")

        # --- 1. Chargement des Produits ---
        print("\n[INFO] Importation de la dimension 'Produits'...")
        df_prod = xl.parse('Produits')
        df_prod.columns = df_prod.columns.str.strip()
        # On convertit l'EAN en entier et on exclut les valeurs invalides (prix à 0 ou négatif)
        df_prod['EAN'] = pd.to_numeric(df_prod['EAN'], errors='coerce').fillna(0).astype(int)
        df_prod['prix'] = pd.to_numeric(df_prod['prix'], errors='coerce').fillna(0.0)
        df_prod = df_prod[df_prod['prix'] > 0]
        # On supprime les doublons d'EAN pour respecter la contrainte de clé primaire
        df_prod = df_prod.drop_duplicates(subset=['EAN'])
        df_prod.to_sql('Dim_Produits', conn, if_exists='append', index=False)
        print(f"  -> {len(df_prod)} produits chargés.")

        # --- 2. Chargement des Clients ---
        print("\n[INFO] Importation de la dimension 'Clients'...")
        df_clients = xl.parse('Clients')
        df_clients.columns = df_clients.columns.str.strip()
        # CORRECTION DE L'ANOMALIE SOURCE : "CUSTUMER_ID" -> "CUSTOMER_ID" (faute d'orthographe)
        df_clients = df_clients.rename(columns={'CUSTUMER_ID': 'CUSTOMER_ID'})
        df_clients = df_clients.drop_duplicates(subset=['CUSTOMER_ID'])
        df_clients.to_sql('Dim_Clients', conn, if_exists='append', index=False)
        print(f"  -> {len(df_clients)} clients chargés.")

        # --- 3. Chargement des Employés ---
        print("\n[INFO] Importation de la dimension 'Employés'...")
        df_emp = xl.parse('Employé')
        df_emp.columns = df_emp.columns.str.strip()
        # On supprime les doublons sur l'identifiant employé
        df_emp = df_emp.drop_duplicates(subset=['id_employe'])
        df_emp.to_sql('Dim_Employes', conn, if_exists='append', index=False)
        print(f"  -> {len(df_emp)} employés chargés.")

        # --- 4. Chargement du Calendrier ---
        print("\n[INFO] Importation de la dimension 'Calendrier'...")
        df_cal = xl.parse('Calendrier')
        df_cal.columns = df_cal.columns.str.strip()
        # On renomme les colonnes pour correspondre au schéma de la base de données
        df_cal = df_cal.rename(columns={'date': 'date_excel', 'Jour': 'jour_date'})
        # On convertit la date en chaîne pour éviter les conflits de type pandas
        df_cal['jour_date'] = df_cal['jour_date'].astype(str)
        df_cal = df_cal.drop_duplicates(subset=['date_excel'])
        df_cal.to_sql('Dim_Calendrier', conn, if_exists='append', index=False)
        print(f"  -> {len(df_cal)} jours de calendrier chargés.")

        # --- 5. Chargement des Ventes (Table de Faits) ---
        # On charge en dernier pour respecter les contraintes de clés étrangères
        print("\n[INFO] Importation de la table de faits 'Vente Détail'...")
        df_ventes = xl.parse('Vente Détail')
        df_ventes.columns = df_ventes.columns.str.strip()
        # On renomme les colonnes pour correspondre au schéma SQLite
        df_ventes = df_ventes.rename(columns={
            'Date achat': 'date_achat_excel',
            'ID ticket':  'ID_ticket'
        })
        df_ventes['EAN'] = pd.to_numeric(df_ventes['EAN'], errors='coerce').fillna(0).astype(int)
        df_ventes.to_sql('Fact_Ventes', conn, if_exists='append', index=False)
        print(f"  -> {len(df_ventes)} lignes de ventes chargées.")

        # --- 6. Chargement des Logs (Exercice 2) ---
        print("\n[INFO] Importation de la table de traçabilité 'Logs'...")
        try:
            df_logs = pd.read_excel(LOGS_EXCEL_PATH)
            df_logs.columns = df_logs.columns.str.strip()
            # On standardise les noms de colonnes vers le schéma de la table Logs
            rename_map = {
                'id_user':    'id_user',
                'date':       'date',
                'id_bdd':     'id_bdd',
                'id_produit': 'id_produit',
                'status':     'status',
            }
            # On standardise les noms de colonnes vers le schéma de la table Logs
            # Le fichier source contient 'action' et 'id_ligne', on les mappe vers 'status' et 'id_bdd'
            df_logs = df_logs.rename(columns={'action': 'status', 'id_ligne': 'id_bdd'})
            
            # On ne conserve que les colonnes qui correspondent à notre schéma
            colonnes_cibles = ['id_user', 'date', 'id_bdd', 'id_produit', 'status']
            colonnes_presentes = [c for c in colonnes_cibles if c in df_logs.columns]
            df_logs = df_logs[colonnes_presentes]
            
            # Élimination des lignes invalides (status vide)
            df_logs = df_logs.dropna(subset=['status'])
            
            df_logs.to_sql('Logs', conn, if_exists='append', index=False)
            print(f"  -> {len(df_logs)} entrées de logs chargées.")
        except FileNotFoundError:
            # Le fichier de logs est optionnel à cette étape (il sera chargé dans l'Ex. 2)
            print(f"  -> [AVERTISSEMENT] Fichier Logs.xlsx non trouvé. Exécutez le script d'intégration de l'Exercice 2.")

        conn.close()
        print("\n[SUCCÈS] Toutes les données ont été chargées avec succès !")

    except Exception as e:
        import traceback
        with open('error_details.txt', 'w', encoding='utf-8') as f:
            f.write(f"Erreur : {e}\n")
            traceback.print_exc(file=f)
        print(f"\n[ERREUR] Chargement échoué. Détails dans error_details.txt")
        sys.exit(1)


if __name__ == "__main__":
    load_data()
