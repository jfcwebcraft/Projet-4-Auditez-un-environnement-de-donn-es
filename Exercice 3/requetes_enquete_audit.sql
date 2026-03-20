-- ==============================================================================
-- PROJET 4 - DOSSIER D'ENQUÊTE TECHNIQUE (SQLITE)
-- Ces requêtes permettent de prouver l'origine de l'écart de 9 057,29 €
-- ==============================================================================

-- 1. CALCUL DU CHIFFRE D'AFFAIRES "INITIAL" (Ce qu'Hugo voyait le matin)
-- On simule l'état de la base le 14/08 soir en excluant les ventes logguées le 15/08.
SELECT 
    'CA Initial (Matin)' AS Etape,
    COUNT(DISTINCT v.ID_BDD) AS Nb_Ventes,
    ROUND(SUM(p.prix), 2) AS Total_EUR
FROM Fact_Ventes v
JOIN Dim_Produits p ON v.EAN = p.EAN
WHERE v.date_achat_excel = 45518
AND v.ID_BDD NOT IN (
    -- On exclut les ventes qui n'ont été enregistrées (logguées) que le 15 août
    SELECT id_bdd FROM Logs WHERE date(date) = '2024-08-15'
);
-- RÉSULTAT : 39 998 ventes | 275 186.59 €


-- 2. IDENTIFICATION DE L'ANOMALIE (L'impact des insertions tardives)
-- On isole les ventes du 14/08 enregistrées techniquement le 15/08.
SELECT 
    'Impact des Logs (Ecart)' AS Etape,
    COUNT(DISTINCT v.ID_BDD) AS Nb_Ventes,
    -- Le facteur /5 compense la quintuple journalisation des logs sources
    ROUND(SUM(p.prix)/5, 2) AS Total_EUR
FROM Logs l
JOIN Fact_Ventes v ON l.id_bdd = v.ID_BDD
JOIN Dim_Produits p ON v.EAN = p.EAN
WHERE date(l.date) = '2024-08-15' AND v.date_achat_excel = 45518;
-- RÉSULTAT : 1 379 ventes | 9 057.29 €


-- 3. CALCUL DU CHIFFRE D'AFFAIRES "FINAL" (Après Audit)
-- C'est la somme totale stabilisée pour la journée du 14 août (Code 45518).
SELECT 
    'CA Final (Power BI)' AS Etape,
    COUNT(v.ID_BDD) AS Nb_Ventes,
    ROUND(SUM(p.prix), 2) AS Total_EUR
FROM Fact_Ventes v
JOIN Dim_Produits p ON v.EAN = p.EAN
WHERE v.date_achat_excel = 45518;
-- RÉSULTAT : 41 377 ventes | 284 243.88 €


-- 4. ÉCHANTILLON DES TRANSACTIONS LOGGUÉES TARDIVEMENT
SELECT 
    v.ID_ticket,
    l.date AS Date_Enregistrement_Systeme,
    l.status AS Action_Audit,
    p.Libelle_produit,
    p.prix AS Montant_EUR
FROM Logs l
JOIN Fact_Ventes v ON l.id_bdd = v.ID_BDD
JOIN Dim_Produits p ON v.EAN = p.EAN
WHERE date(l.date) = '2024-08-15'
LIMIT 10;