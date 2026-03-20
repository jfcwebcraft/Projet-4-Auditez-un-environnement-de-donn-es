# Dictionnaire des Données - SuperSmartMarket

Ce document répertorie les tables et colonnes identifiées dans l'extraction OLAP du 14 août 2024.
Il sert de référentiel de documentation pour l'équipe BI et tout auditeur extérieur.

---

## 1. Table de Faits : `Fact_Ventes` (Onglet source : "Vente Détail")

Contient les transactions commerciales à la maille la plus fine : une ligne par produit par ticket de caisse.

| Colonne | Type SQL | Description | Valeur Exemple | Contraintes / Anomalie |
| :--- | :--- | :--- | :--- | :--- |
| `ID_BDD` | TEXT | Identifiant unique technique de la ligne de vente. | `V-00001` | PK - Non null |
| `CUSTOMER_ID` | TEXT | Identifiant du client (Jointure avec `Dim_Clients`). | `CUST-0042` | FK → `Dim_Clients` |
| `id_employe` | TEXT | Identifiant de l'employé ayant encaissé la vente. | `EMP_abc123` | FK → `Dim_Employes` |
| `EAN` | INTEGER | Code barre EAN du produit (Jointure avec `Dim_Produits`). | `3017620425035` | FK → `Dim_Produits` |
| `date_achat_excel` | INTEGER | Date de la transaction au format sériel Excel (ex: 45518 = 14/08/2024). | `45518` | FK → `Dim_Calendrier.date_excel` |
| `ID_ticket` | TEXT | Identifiant du ticket de caisse. Regroupe plusieurs lignes `ID_BDD`. | `TKT-20240814-001` | Peut être null (vente anonyme) |

---

## 2. Table de Dimension : `Dim_Produits` (Onglet source : "Produits")

Contient le catalogue complet des produits vendus en magasin.

| Colonne | Type SQL | Description | Valeur Exemple | Contraintes / Anomalie |
| :--- | :--- | :--- | :--- | :--- |
| `EAN` | INTEGER | Code barre unique (European Article Number). | `3017620425035` | PK - Non null |
| `categorie` | TEXT | Catégorie parente du produit. | `Épicerie` | - |
| `Rayon` | TEXT | Rayon spécifique en magasin. | `Pâtes et riz` | - |
| `Libelle_produit` | TEXT | Nom descriptif du produit. | `Pâtes Panzani 500g` | - |
| `prix` | REAL | Prix unitaire TTC du produit en euros. | `1.79` | Doit être > 0 |

---

## 3. Table de Dimension : `Dim_Clients` (Onglet source : "Clients")

Contient les informations des clients membres du programme de fidélité.

| Colonne | Type SQL | Description | Valeur Exemple | Contraintes / Anomalie |
| :--- | :--- | :--- | :--- | :--- |
| `CUSTOMER_ID` | TEXT | Identifiant unique du client. | `CUST-0042` | PK - Non null |
| `date_inscription` | TEXT | Date d'adhésion au programme de fidélité. | `2022-05-15` | - |

> ⚠️ **Anomalie Source Détectée** : Dans le fichier Excel original, cette colonne est nommée `CUSTUMER_ID` (faute de frappe dans "CUSTOMER"). Le script ETL (`load_data.py`) corrige cette anomalie lors du chargement en renommant la colonne en `CUSTOMER_ID`.

---

## 4. Table de Dimension : `Dim_Employes` (Onglet source : "Employé")

Contient les informations du personnel habilité à réaliser des ventes.

| Colonne | Type SQL | Description | Valeur Exemple | Contraintes / Anomalie |
| :--- | :--- | :--- | :--- | :--- |
| `id_employe` | TEXT | Identifiant unique de l'employé (Hash SHA). | `e3b0c442...` | PK - Non null |
| `employe` | TEXT | Identifiant court / username de connexion. | `jmartin` | - |
| `prenom` | TEXT | Prénom de l'employé. | `Jean` | - |
| `nom` | TEXT | Nom de famille de l'employé. | `Martin` | - |
| `date_debut` | INTEGER | Date d'embauche au format sériel Excel. | `44562` | - |
| `hash_mdp` | TEXT | Hash du mot de passe (donnée sensible RGPD). | `$2b$12$...` | 🔐 Donnée sensible - Anonymisation obligatoire en reporting |
| `mail` | TEXT | Adresse email professionnelle de l'employé. | `j.martin@ssmarket.fr` | 🔐 Donnée sensible - Anonymisation obligatoire en reporting |

---

## 5. Table de Dimension : `Dim_Calendrier` (Onglet source : "Calendrier")

Référentiel temporel permettant toutes les analyses par période.

| Colonne | Type SQL | Description | Valeur Exemple | Contraintes / Anomalie |
| :--- | :--- | :--- | :--- | :--- |
| `date_excel` | INTEGER | Clé de date en format sériel Excel. Clé de jointure principale. | `45518` | PK - Non null |
| `annee` | INTEGER | Année civile. | `2024` | - |
| `mois` | INTEGER | Numéro du mois (1 à 12). | `8` | - |
| `jour_date` | TEXT | Date complète au format ISO. | `2024-08-14` | Renommée depuis "Jour" lors du chargement |
| `mois_nom` | TEXT | Nom du mois en français. | `Août` | - |
| `annee_mois` | INTEGER | Identifiant combiné mois/année pour regroupements. | `202408` | - |
| `jour_semaine` | INTEGER | Index du jour de la semaine (0=Lundi, 6=Dimanche). | `2` | - |
| `trimestre` | TEXT | Trimestre au format standard. | `Q3` | - |

---

## 6. Table de Traçabilité : `Logs` (Source : "../data/Logs.xlsx")

Contient l'historique de toutes les opérations réalisées sur les données transactionnelles.
C'est cette table qui permet d'expliquer le **delta de 9 057,29 €** sur le CA du 14 août 2024.

| Colonne | Type SQL | Description | Valeur Exemple | Contraintes / Anomalie |
| :--- | :--- | :--- | :--- | :--- |
| `id_log` | INTEGER | Identifiant auto-incrémenté du log. | `1` | PK - AUTOINCREMENT |
| `id_user` | TEXT | Identifiant de l'employé ayant réalisé l'opération. | `EMP_abc123` | FK → `Dim_Employes` |
| `date` | DATETIME | Horodatage précis de l'opération. | `2024-08-14 18:32:11` | Non null |
| `id_bdd` | TEXT | Référence à la ligne de vente concernée. | `V-00001` | FK → `Fact_Ventes.ID_BDD` |
| `id_produit` | INTEGER | Référence au produit concerné par l'opération. | `3017620425035` | FK → `Dim_Produits.EAN` |
| `status` | TEXT | Type d'opération réalisée. | `INSERT`, `UPDATE`, `DELETE` | Non null |

---

## Synthèse des Anomalies Détectées

| Anomalie | Localisation | Impact | Correction Appliquée |
| :--- | :--- | :--- | :--- |
| Faute de frappe `CUSTUMER_ID` | Onglet "Clients" du fichier Excel | Rupture de jointure avec `Fact_Ventes` | Renommage automatique dans `load_data.py` |
| Insertions tardives de tickets | Fichier `Logs.xlsx` | Delta de CA +9 057,29 € | Identification et documentation dans le rapport d'audit |
| Données sensibles non masquées | Table `Dim_Employes` | Risque RGPD | Anonymisation via `mesures_correctives.sql` |
| Absence de contraintes d'intégrité | BDD complète | Données "orphelines" possibles | Ajout de Foreign Keys et Triggers (Ex. 3) |
