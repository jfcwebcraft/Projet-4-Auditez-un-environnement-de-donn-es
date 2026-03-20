# Exercice 2 : Audit de Qualité et Analyse des Logs

## Objectifs
Investiguer l'instabilité du chiffre d'affaires (CA) du 14 août 2024 et auditer la qualité globale des données de SuperSmartMarket.

## Travaux Réalisés

### 1. Analyse des Logs (`Logs.xlsx`)
L'analyse croisée du fichier de logs (+200 000 entrées) avec la table des ventes a livré les réponses attendues :
- **Identification du Delta** : La différence de **+9 057,29 €** provient de **1 379 tickets** enregistrés physiquement dans le système le 15 août, mais antidatés au 14 août. Power BI les a donc comptabilisés a posteriori.
- **Intégration SQL** : Importation automatisée du fichier de logs dans SQLite via le script `scripts/integrate_logs_to_db.py`.

### 2. Audit de Qualité de Données
- **Historique Produit Défaillant** : 575 modifications de prix (UPDATE) ont été constatées sans aucune trace historisée.
- **Anomalie de Nommage** : Faute de frappe critique à la source (`CUSTUMER_ID`). Le script de chargement ETL gère automatiquement cette correction.
- **Vérification d'Unicité** : Aucun doublon technique d'`ID_BDD` détecté.
- **Données RGPD** : `hash_mdp` et `mail` des employés identifiés comme données sensibles à pseudonymiser.

## Livrables
- [`audit_rapport.md`](../Livrables/Chaussoy_Jean_Francois_1_rapport-audit_022026.md) : Rapport complet avec analyse financière, anomalies, et recommandations.
- [`scripts/integrate_logs_to_db.py`](scripts/integrate_logs_to_db.py) : Script d'intégration des logs + rapport de synthèse d'audit.
- `../supersmartmarket.db` : Base de données enrichie avec la table des logs.

## Comment Reproduire l'Analyse

### Prérequis
```bash
# Installer les dépendances Python
pip install pandas openpyxl
```

### Étape 1 : Initialiser la base (si pas encore fait)
```bash
python "Exercice 1/scripts/init_db.py"
python "Exercice 1/scripts/load_data.py"
```

### Étape 2 : Intégrer les logs
```bash
python "Exercice 2/scripts/integrate_logs_to_db.py"
```
Ce script affiche automatiquement un **rapport de synthèse** dans la console : répartition par type d'opération, top 5 des utilisateurs actifs, et focus sur les logs du 14 août.
