import sqlite3
import pandas as pd
import os
import sys

# Chemins calculés dynamiquement (portables)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "supersmartmarket.db")
EXCEL_PATH = os.path.join(BASE_DIR, "data", "data.xlsx")
LOGS_EXCEL_PATH = os.path.join(BASE_DIR, "data", "Logs.xlsx")


def init_sqlite_demo() -> None:
    """
    Initialise une base SQLite complète pour la démonstration en soutenance.
    Charge les données depuis les fichiers Excel, crée les triggers d'audit,
    et affiche un résumé prêt à utiliser dans DB Browser for SQLite.
    """
    print("=" * 60)
    print("  INITIALISATION DE LA BASE SQLITE (DÉMO SOUTENANCE)")
    print("=" * 60)

    # On supprime l'ancienne base pour garantir un état propre
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print(f"[INFO] Ancienne base supprimée.")
        except PermissionError:
            print("[ERREUR] La base est peut-être ouverte dans un autre programme (DB Browser ?).")
            print("  -> Fermez DB Browser for SQLite et relancez ce script.")
            sys.exit(1)

    conn = sqlite3.connect(DB_PATH)

    try:
        print(f"\n[INFO] Lecture du fichier Excel : {EXCEL_PATH}")
        xl = pd.ExcelFile(EXCEL_PATH)

        # --- Chargement des données dimension par dimension ---
        for sheet_name, table_name, rename_map in [
            ('Produits',     'Dim_Produits',   {}),
            ('Clients',      'Dim_Clients',    {'CUSTUMER_ID': 'CUSTOMER_ID'}),
            ('Employé',      'Dim_Employes',   {}),
            ('Calendrier',   'Dim_Calendrier', {'date': 'date_excel', 'Jour': 'jour_date'}),
            ('Vente Détail', 'Fact_Ventes',    {'Date achat': 'date_achat_excel', 'ID ticket': 'ID_ticket'}),
        ]:
            print(f"  -> Import '{sheet_name}' vers '{table_name}'...", end=" ")
            df = xl.parse(sheet_name)
            df.columns = df.columns.str.strip()

            # Renommage des colonnes si nécessaire (ex: correction CUSTUMER_ID)
            if rename_map:
                df = df.rename(columns=rename_map)

            # Conversion du Jour en String pour le Calendrier
            if sheet_name == 'Calendrier' and 'jour_date' in df.columns:
                df['jour_date'] = df['jour_date'].astype(str)

            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"{len(df)} lignes ✓")

        # --- Création de la table Logs ---
        print("\n[INFO] Création de la table Logs...")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS Logs (
            id_log      INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user     TEXT,
            date        DATETIME DEFAULT CURRENT_TIMESTAMP,
            id_bdd      TEXT,
            id_produit  INTEGER,
            status      TEXT NOT NULL
        )""")
        print("  -> Table Logs créée.")

        # --- Chargement des Logs depuis Excel (si disponible) ---
        if os.path.exists(LOGS_EXCEL_PATH):
            print(f"\n[INFO] Chargement des logs depuis Logs.xlsx...")
            df_logs = pd.read_excel(LOGS_EXCEL_PATH)
            df_logs.columns = df_logs.columns.str.strip()
            
            # Mapping des colonnes réelles vers le schéma BDD
            rename_logs = {'action': 'status', 'id_ligne': 'id_bdd'}
            df_logs = df_logs.rename(columns=rename_logs)
            
            # Conversion de la date Excel si nécessaire
            if 'date' in df_logs.columns and df_logs['date'].dtype != 'object':
                # Si c'est un format Excel sériel (45518), on le laisse ou on le convertit
                # Pour le POC, on s'assure que c'est exploitable
                pass

            # On ne garde que les colonnes attendues par le schéma
            colonnes_cibles = ['id_user', 'date', 'id_bdd', 'id_produit', 'status']
            # On ajoute id_produit à None si absent (car absent de Logs.xlsx)
            if 'id_produit' not in df_logs.columns:
                df_logs['id_produit'] = None
                
            colonnes_ok = [c for c in colonnes_cibles if c in df_logs.columns]
            df_logs[colonnes_ok].to_sql('Logs', conn, if_exists='append', index=False)
            print(f"  -> {len(df_logs)} entrées de logs chargées.")
        else:
            print(f"\n[AVERTISSEMENT] Fichier Logs.xlsx non trouvé. Les requêtes d'audit sur les logs seront vides.")

        # --- Installation des Triggers d'Audit ---
        print("\n[INFO] Installation des Triggers d'audit...")
        conn.executescript("""
        -- Trigger 1 : Tracé automatique de chaque insertion de vente
        CREATE TRIGGER IF NOT EXISTS audit_vente_insert
        AFTER INSERT ON Fact_Ventes
        FOR EACH ROW
        BEGIN
            INSERT INTO Logs (id_user, id_bdd, id_produit, status)
            VALUES (NEW.id_employe, NEW.ID_BDD, NEW.EAN, 'INSERT_AUTO');
        END;

        -- Trigger 2 : Blocage si le prix du produit est nul ou négatif
        CREATE TRIGGER IF NOT EXISTS validate_price_before_insert
        BEFORE INSERT ON Fact_Ventes
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN (SELECT prix FROM Dim_Produits WHERE EAN = NEW.EAN) <= 0
                THEN RAISE(ABORT, 'Prix invalide : insertion refusee')
            END;
        END;

        -- Trigger 3 : Tracé automatique de chaque suppression de vente
        CREATE TRIGGER IF NOT EXISTS audit_vente_delete
        AFTER DELETE ON Fact_Ventes
        FOR EACH ROW
        BEGIN
            INSERT INTO Logs (id_user, id_bdd, id_produit, status)
            VALUES (OLD.id_employe, OLD.ID_BDD, OLD.EAN, 'DELETE_AUDIT');
        END;

        -- Trigger 4 : Tracé automatique de chaque modification de vente
        CREATE TRIGGER IF NOT EXISTS audit_vente_update
        AFTER UPDATE ON Fact_Ventes
        FOR EACH ROW
        BEGIN
            INSERT INTO Logs (id_user, id_bdd, id_produit, status)
            VALUES (NEW.id_employe, NEW.ID_BDD, NEW.EAN, 'UPDATE_AUDIT');
        END;
        """)
        print("  -> 4 triggers installés (INSERT, BEFORE INSERT, DELETE, UPDATE).")

        conn.commit()

        # --- Résumé Final ---
        print("\n" + "=" * 60)
        print("  BASE SQLITE PRÊTE POUR LA DÉMO !")
        print("=" * 60)
        print(f"  Fichier : {os.path.abspath(DB_PATH)}")
        print("\n  Tables disponibles :")
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        for t in tables:
            count = conn.execute(f"SELECT COUNT(*) FROM {t[0]};").fetchone()[0]
            print(f"    - {t[0]:<20} {count:>8} lignes")

        print("\n  Prochaine étape :")
        print("  -> Ouvrez 'supersmartmarket.db' dans DB Browser for SQLite")
        print("  -> Exécutez 'demo_presentation_sqlite.sql' pour les tests en direct")

    except Exception as e:
        import traceback
        print(f"\n[ERREUR] Initialisation échouée : {e}")
        traceback.print_exc()
        conn.close()
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    init_sqlite_demo()
