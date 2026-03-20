import sqlite3
import sys
import os
import re

# Chemins relatifs
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "supersmartmarket.db")

def clean_sql(sql: str) -> str:
    """Supprime les commentaires et nettoie la requête."""
    # Supprimer les commentaires --
    sql = re.sub(r'--.*', '', sql)
    # Supprimer les sauts de ligne inutiles
    return sql.strip()

def run_sql_file(file_path: str) -> None:
    """Exécute un fichier SQL sur la base et affiche le résultat proprement."""
    if not os.path.exists(file_path):
        print(f"[ERREUR] Le fichier '{file_path}' n'existe pas.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            full_sql = f.read()
            
        # On split par point-virgule
        commands = full_sql.split(';')
            
        print(f"\n🚀 AUDIT TERMINAL - Fichier : {os.path.basename(file_path)}")
        print("=" * 70)
        
        for command in commands:
            cmd = clean_sql(command)
            if not cmd:
                continue
            
            # Détection de la commande principale
            first_word = cmd.split()[0].upper() if cmd.split() else ""
            
            if first_word == "SELECT":
                try:
                    cursor.execute(cmd)
                    columns = [description[0] for description in cursor.description]
                    results = cursor.fetchall()
                    
                    print(f"\n📊 RÉSULTAT REQUÊTE :")
                    if results:
                        # Rendu simple et aligné
                        widths = [max(len(str(x)) for x in col) for col in zip(*(results + [tuple(columns)]))]
                        header = " | ".join(f"{col:<{widths[i]}}" for i, col in enumerate(columns))
                        print(header)
                        print("-" * len(header))
                        for row in results:
                            print(" | ".join(f"{str(val):<{widths[i]}}" for i, val in enumerate(row)))
                        print(f"({len(results)} lignes)")
                    else:
                        print("(Aucun résultat)")
                except sqlite3.Error as e:
                    print(f"❌ Erreur SQL (SELECT) : {e}")
            else:
                # Commandes INSERT, UPDATE, DELETE, etc.
                try:
                    cursor.execute(cmd)
                    conn.commit()
                    rows = cursor.rowcount
                    if rows > 0:
                        print(f"✅ {first_word} : {rows} ligne(s) affectée(s).")
                    else:
                        print(f"ℹ️ {first_word} exécuté (0 ligne affectée).")
                except sqlite3.Error as e:
                    # On ignore les erreurs mineures type "table already exists" si besoin
                    if "already exists" not in str(e):
                        print(f"❌ Erreur SQL ({first_word}) : {e}")

        conn.close()
        print("\n" + "=" * 70 + "\n")

    except Exception as e:
        print(f"[ERREUR FATALE] {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("💡 Usage: python terminal_audit.py <votre_fichier.sql>")
        print("   Exemple: python terminal_audit.py enquete_delta_ca.sql")
    else:
        run_sql_file(sys.argv[1])
