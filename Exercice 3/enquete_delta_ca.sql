-- ==============================================================================
-- PROJET 4 - AUDITEZ UN ENVIRONNEMENT DE DONNÉES
-- DOSSIER DE PREUVES SQL (POUR CAPTURES D'ÉCRAN SOUTENANCE)
-- ==============================================================================

-- 🔍 PREUVE N°1 : HYPOTHÈSE DES PRIX (575 UPDATE)
-- On vérifie que les modifications de prix ont eu lieu le jour même (14/08)
SELECT 
    date(date) AS "Date_Log", 
    status, 
    COUNT(*) AS "Nb_Updates"
FROM Logs 
WHERE status = 'UPDATE' AND id_produit IS NOT NULL 
GROUP BY 1;
-- RÉSULTAT RÉEL : 2024-08-14 | UPDATE | 575


-- Note : Le facteur /5 compense la quintuple journalisation présente dans les logs sources (5 entrées par vente).
SELECT 
    date(l.date) AS "Jour_Enregistrement", 
    v.date_achat_excel AS "Date_Commerciale", 
    COUNT(DISTINCT v.ID_BDD) AS "Nb_Ventes_Reelles", 
    ROUND(SUM(p.prix)/5, 2) AS "CA_Net_Detecte"
FROM Fact_Ventes v 
JOIN Logs l ON v.ID_BDD = l.id_bdd 
JOIN Dim_Produits p ON v.EAN = p.EAN 
WHERE v.date_achat_excel = 45518 AND l.status = 'INSERT' 
GROUP BY 1;
-- RÉSULTAT RÉEL :
-- 2024-08-14 | 45518 | 39 998 | 275 186.59
-- 2024-08-15 | 45518 |  1 379 |   9 057.29


-- 🔍 PREUVE N°3 : VALIDATION DU TOTAL FINAL (POWER BI)
-- On confirme que le total en base est bien celui de Power BI
SELECT 
    v.date_achat_excel AS "Date_Excel", 
    COUNT(v.ID_BDD) AS "Total_Ventes", 
    ROUND(SUM(p.prix), 2) AS "Total_CA_PowerBI"
FROM Fact_Ventes v 
JOIN Dim_Produits p ON v.EAN = p.EAN 
WHERE v.date_achat_excel = 45518;
-- RÉSULTAT RÉEL : 45518 | 41 377 | 284 243.88
