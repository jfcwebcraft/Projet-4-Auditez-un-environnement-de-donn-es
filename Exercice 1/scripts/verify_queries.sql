-- ==============================================================================
-- EXERCICE 1 - REQUÊTES DE VÉRIFICATION ET D'AUDIT
-- Objectif : Valider les données chargées et prouver les chiffres clés.
-- Ces requêtes sont celles présentées à Hugo lors de la soutenance.
-- ==============================================================================


-- ============================================================
-- REQUÊTE 1 : CHIFFRE D'AFFAIRES TOTAL DU 14 AOÛT 2024
-- La date Excel 45518 correspond au 14 août 2024.
-- Résultat attendu : ~284 243,88 €
-- ============================================================
SELECT
    'CA Total 14 Août 2024' AS Indicateur,
    ROUND(SUM(p.prix), 2)   AS Valeur_EUR
FROM Fact_Ventes f
JOIN Dim_Produits p ON f.EAN = p.EAN
WHERE f.date_achat_excel = 45518;


-- ============================================================
-- REQUÊTE 2 : TOP 10 DES CLIENTS PAR CHIFFRE D'AFFAIRES
-- Identifie les meilleurs clients pour le programme de fidélité.
-- ============================================================
SELECT
    f.CUSTOMER_ID,
    ROUND(SUM(p.prix), 2) AS CA_Client_EUR
FROM Fact_Ventes f
JOIN Dim_Produits p ON f.EAN = p.EAN
GROUP BY f.CUSTOMER_ID
ORDER BY CA_Client_EUR DESC
LIMIT 10;


-- ============================================================
-- REQUÊTE 3 : PART DU CA PAR EMPLOYÉ (Avec Pourcentage)
-- Permet de contrôler l'activité de chaque caissier.
-- Utile pour détecter des comportements anormaux.
-- ============================================================
SELECT
    e.prenom,
    e.nom,
    ROUND(SUM(p.prix), 2)   AS CA_Employe_EUR,
    ROUND(SUM(p.prix) * 100.0 / (
        SELECT SUM(p2.prix) FROM Fact_Ventes f2 JOIN Dim_Produits p2 ON f2.EAN = p2.EAN
    ), 2)                   AS Pourcentage_CA
FROM Fact_Ventes f
JOIN Dim_Produits p  ON f.EAN = p.EAN
JOIN Dim_Employes e  ON f.id_employe = e.id_employe
GROUP BY e.id_employe
ORDER BY CA_Employe_EUR DESC;


-- ============================================================
-- REQUÊTE 4 : CA PAR RAYON DE PRODUIT
-- Permet de voir quels rayons génèrent le plus de revenus.
-- ============================================================
SELECT
    p.Rayon,
    COUNT(f.ID_BDD)         AS Nb_Articles_Vendus,
    ROUND(SUM(p.prix), 2)   AS CA_Rayon_EUR
FROM Fact_Ventes f
JOIN Dim_Produits p ON f.EAN = p.EAN
GROUP BY p.Rayon
ORDER BY CA_Rayon_EUR DESC;


-- ============================================================
-- REQUÊTE 5 : VÉRIFICATION D'INTÉGRITÉ - CLIENTS ORPHELINS
-- Détecte les ventes sans client reconnu (données incohérentes).
-- ============================================================
SELECT
    'Transactions sans client valide' AS Indicateur,
    COUNT(*)                          AS Nb_Lignes
FROM Fact_Ventes f
WHERE f.CUSTOMER_ID NOT IN (SELECT CUSTOMER_ID FROM Dim_Clients)
   OR f.CUSTOMER_ID IS NULL;
