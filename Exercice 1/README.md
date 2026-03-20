# Audit de l'Environnement de Données - Exercice 1

Ce dossier contient l'ensemble des travaux réalisés pour la première phase de l'audit de SuperSmartMarket. L'objectif principal était de comprendre l'architecture de données existante et de résoudre une incohérence majeure détectée sur le chiffre d'affaires du 14 août.

## 1. Analyse de la Demande
Hugo, responsable BI, a signalé une anomalie : le chiffre d'affaires du 14 août (initialement de 275 186,59 €) a été réévalué à 284 243,88 € deux jours plus tard, sans explication apparente.

### Objectifs de la mission :
- Documenter la base de données OLAP (inexistante jusqu'alors).
- Créer un modèle relationnel cohérent.
- Développer un prototype (POC) pour vérifier les chiffres et identifier la cause des écarts.

---

## 2. Solution Implémentée

### Documentation et Modélisation
- [Dictionnaire des données](Dictionnaire_des_donnees.md) : Inventaire complet des tables et colonnes identifiées dans l'extraction brute.
- [Schéma Relationnel](Schema_Relationnel.md) : Conception d'un modèle en étoile articulé autour de la table de faits `Ventes`.

### Développement du POC SQL
J'ai mis en place un environnement local basé sur **SQLite** pour auditer les données indépendamment des outils de reporting métier.
- **Scripts ETL (Python)** : Automatisation de la création de la base et du chargement des données.
- **Nettoyage des données** : Correction d'erreurs de saisie bloquantes (`CUSTUMER_ID`) et élimination des doublons sur les dimensions pour restaurer l'intégrité référentielle.
- **Validation Métier** : La génération d'un véritable "Top 10 Clients" via requête SQL a permis de prouver l'efficacité immédiate de cette nouvelle architecture en étoile.

### Audit des Chiffres
Suite à l'exécution de nos requêtes analytiques sur la base SQLite, nous avons pu valider de manière certaine :
- Le chiffre d'affaires total de la journée du 14 août est bien arrêté à **284 243,88 €**.
- Le delta mathématique observé relève d'écritures asynchrones : des opérations insérées tardivement viennent grossir le compte de la journée précédente.

---

## 3. Contenu Techniques du Dossier
- `scripts/` : Moteur de l'ETL local.
    - `init_db.py` : Création de la structure relationnelle.
    - `load_data.py` : Logique d'importation et de nettoyage.
    - `verify_queries.sql` : Requêtes d'audit utilisées pour la validation.
- `../supersmartmarket.db` : Base de données relationnelle résultante (Format SQLite).

---

**Statut : Terminé et Validé.**
