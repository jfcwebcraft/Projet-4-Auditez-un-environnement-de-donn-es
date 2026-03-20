# Données pour Visuels Power BI - Audit SuperSmartMarket

Voici les indicateurs et requêtes à utiliser pour créer vos tableaux de bord visuels.

---

## 1. Indicateurs Clés (KPIs)
- **CA Total (Audité)** : 284 243,88 €
- **Nombre de Transactions** : Total des lignes dans `Fact_Ventes` pour le 14/08.
- **Delta Financier** : +9 057,29 € (à afficher en 'Alerte' ou 'Variance').
- **Ventes Rétroactives** : 1 379 transactions (insérées le 15 août mais datées du 14).
- **Nombre de Produits différents** : Compte unique des EAN vendus.

---

## 2. Visuels Recommandés

### A. Évolution du CA (Graphique en barres ou Waterfall)
- **Objectif** : Montrer le passage de 275k à 284k.
- **Données** :
    - Valeur 1 : CA Initial (275 186,59 €)
    - Valeur 2 : Impact des 1 379 ventes rétroactives (9 057,29 €)
    - Total : CA Final (284 243,88 €)

### B. Top 5 Catégories de Produits (Camembert / Treemap)
- **Requête SQL pour Power BI** :
    ```sql
    SELECT p.categorie, SUM(p.prix) as CA_Categorie
    FROM Fact_Ventes f
    JOIN Dim_Produits p ON f.EAN = p.EAN
    GROUP BY p.categorie
    ORDER BY CA_Categorie DESC
    LIMIT 5;
    ```

### C. Répartition des Actions de Logs (Anneau)
- **Objectif** : Montrer le volume d'Insert/Delete/Update.
- **Données** :
    ```sql
    SELECT status, COUNT(*) as Volume
    FROM Logs
    GROUP BY status;
    ```

### D. CA par Rayon (Histogramme Groupé)
- **Requête SQL** :
    ```sql
    SELECT p.Rayon, SUM(p.prix) as CA_Rayon
    FROM Fact_Ventes f
    JOIN Dim_Produits p ON f.EAN = p.EAN
    GROUP BY p.Rayon;
    ```

---

## 3. Données de "Qualité" (Cartes de score)
- **Modifications de Prix (Alerte rouge)** : 575 prix écrasés en base de données sans aucune trace ou historique.
- **Taux de correspondance Clients** : (Nombre de ventes avec CUSTOMER_ID valide / Total ventes).
- **Anomalies de prix négatifs** : Nombre de produits avec prix <= 0 (devrait être 0 après application des triggers).

---

## 4. Astuce Power BI
Pour intégrer ces données, utilisez le connecteur **SQLite** ou exportez vos tables finalisées en **CSV** depuis la base de données SQLite pour les charger directement dans Power BI Desktop.
