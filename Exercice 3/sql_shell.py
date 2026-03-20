import sqlite3
import os
import sys

# Chemins relatifs
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "supersmartmarket.db")

def start_shell():
    print("=" * 60)
    print("      SHELL SQL INTERACTIF - SUPERSMARTMARKET")
    print("=" * 60)
    print("Tapez vos requêtes SQL (terminez par ;) ou 'exit' pour quitter.")
    print("-" * 60)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        while True:
            # Saisie de la requête (support multi-lignes rudimentaire)
            query = ""
            while True:
                line = input("sql> " if not query else "...  ")
                if line.lower() == "exit":
                    conn.close()
                    print("Au revoir !")
                    return
                
                # Commandes spéciales (simulant sqlite3 CLI)
                clean_line = line.strip().lower()
                if clean_line == ".tables":
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = [t[0] for t in cursor.fetchall()]
                    print("\n📦 Tables : " + ", ".join(tables) + "\n")
                    break
                if clean_line.startswith(".schema"):
                    parts = clean_line.split()
                    if len(parts) > 1:
                        table = parts[1]
                        cursor.execute(f"PRAGMA table_info({table})")
                        info = cursor.fetchall()
                        if info:
                            print(f"\n📂 Structure de {table} :")
                            for col in info:
                                print(f"  - {col[1]} ({col[2]})")
                            print("")
                        else:
                            print(f"\n❌ Table {table} introuvable.\n")
                    break

                query += " " + line
                if ";" in line:
                    break
            
            if not query.strip():
                continue
            
            # Exécution
            try:
                cmd = query.strip()
                cursor.execute(cmd)
                
                if cmd.upper().startswith("SELECT"):
                    columns = [description[0] for description in cursor.description]
                    results = cursor.fetchall()
                    
                    if results:
                        # Rendu aligné simple
                        widths = [max(len(str(x)) for x in col) for col in zip(*(results + [tuple(columns)]))]
                        header = " | ".join(f"{col:<{widths[i]}}" for i, col in enumerate(columns))
                        print("\n" + header)
                        print("-" * len(header))
                        for row in results:
                            print(" | ".join(f"{str(val):<{widths[i]}}" for i, val in enumerate(row)))
                        print(f"({len(results)} lignes)\n")
                    else:
                        print("\n(Aucun résultat)\n")
                else:
                    conn.commit()
                    print(f"\n✅ Commande exécutée avec succès ({cursor.rowcount} lignes affectées).\n")
            except sqlite3.Error as e:
                print(f"\n❌ Erreur SQL : {e}\n")

    except Exception as e:
        print(f"[ERREUR] Impossible de se connecter à la base : {e}")

if __name__ == "__main__":
    start_shell()
