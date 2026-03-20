# Auto-évaluation : Auditez un environnement de données - Data Engineer

| Étape | Indicateur de réussite | Notes (Commentaires pour le mentor) |
| :--- | :--- | :--- |
| **Mission 1** | Le dictionnaire des données est complet | Tous les champs (incluant la table Logs) sont documentés dans `Exercice 1/Dictionnaire_des_donnees.md`. |
| | Le schéma relationnel est conforme | Modèle en étoile (Star Schema) implémenté, centré sur `Fact_Ventes`. |
| | Clés étrangères et primaires détectées | Identifiées pour chaque dimension (EAN, CUSTOMER_ID, etc.) et activées en base. |
| | Système SGBD installé | SQLite utilisé pour sa portabilité et sa facilité d'audit. |
| | Données insérées dans la base | Automatisé via `load_data.py`. |
| | Types correspondent | Mapping vérifié entre Excel (Real/Integer) et SQLite (REAL/INTEGER). |
| | Bonnes pratiques SQL respectées | Utilisation de jointures explicites, alias lisibles et modèles normalisés. |
| | Qualité des données extraites vérifiée | Détection d'une erreur de nommage source (`CUSTUMER_ID`) et de l'instabilité du CA. |
| | Support de présentation rempli | Notes de présentation prêtes dans `Exercice 3/notes_presentation.md`. |
| **Mission 2** | Logs intégrés dans la base | Table `Logs` créée et alimentée via `integrate_logs_to_db.py`. |
| | Format des données analysé | Identification des types d'opérations (INSERT/DELETE) responsables du delta. |
| | Template complété | Rapport d'audit `audit_rapport.md` créé pour documenter les logs. |
| | Table des logs ajoutée au dictionnaire | Table documentée avec ses champs (id_user, date, status, etc.). |
| | Tests SQL effectués sur les logs | Calcul d'impact financier réalisé, confirmant le delta de 9 057,29 €. |
| | Données correspondent à l'écart de CA | Corrélation exacte établie entre les insertions de logs et l'augmentation du CA. |
| **Mission 3** | Cours et ressources revus | Concepts ACID et Triggers intégrés dans la solution finale. |
| | Veille et recherche réalisée | Solutions techniques (Triggers de validation) et humaines (Cut-off BI) proposées. |
| | Analyse ajoutée aux templates | Rapport exhaustif et notes de présentation finalisés. |
| | Documents sourcés | Références aux principes ACID et MDM (Master Data Management). |
| | Document d'audit complet | `rapport_audit_complet.md` couvre l'exhaustivité des missions. |
| | Recommandations émises | Préconisations sur la résilience et la gouvernance des données. |
| | Recommandations fonctionnelles | Triggers opérationnels dans le prototype SQL. |
| | Prototype ajouté au support | Planifié pour les livrables de présentation. |
