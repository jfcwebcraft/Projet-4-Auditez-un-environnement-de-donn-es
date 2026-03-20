-- ==============================================================================
-- PROJET 4 - SUPPORTS DE SOUTENANCE (RÉALIGNEMENT CANVA)
-- SCRIPT POUR LA SLIDE : "ANALYSE DES LOGS - VUE GLOBALE"
-- ==============================================================================

-- 1. PREUVE : LE CA N'A PAS ÉTÉ MANIPULÉ OU SUPPRIMÉ
-- (On cherche tout ce qui n'est PAS un INSERT sur les ventes)
SELECT 
    'Contrôle Fraude' AS "Action",
    status AS "Type_Operation",
    COUNT(*) AS "Nb_Operations"
FROM Logs 
WHERE id_bdd LIKE 'V-%' AND status != 'INSERT'
GROUP BY status;
-- RÉSULTAT : 0 résultat (Preuve qu'aucun ticket n'a été modifié/supprimé).


-- 2. PREUVE : VOLUME ÉLEVÉ D'ÉCRITURES (PISTE ASYNCHRONISME)
-- (On identifie les 206 885 insertions sur la table Fact_Ventes)
SELECT 
    'Anomalie Volume' AS "Observation",
    status AS "Technique",
    COUNT(*) AS "Impact_Logs"
FROM Logs 
WHERE id_bdd LIKE 'V-%' AND status = 'INSERT';
-- RÉSULTAT : INSERT | 206 885


-- 3. PREUVE : RISQUE DE PRIX SANS HISTORIQUE (CRITIQUE)
-- (On identifie les 575 modifications sur les produits)
SELECT 
    'Risque Prix' AS "Alerte",
    'UPDATE sur Dim_Produits' AS "Observation",
    COUNT(*) AS "Nb_Changements_Sans_SCD"
FROM Logs 
WHERE id_produit IS NOT NULL AND status = 'UPDATE';
-- RÉSULTAT : 575


-- 4. PREUVE : TEST DE JOINTURE VENTES <-> CLIENTS (QUALITÉ)
-- (Prouve le nettoyage de la base prototype)
SELECT 
    'Nettoyage BDD' AS "Test_Qualite",
    COUNT(*) AS "Nb_Ventes_Orphelines"
FROM Fact_Ventes v
LEFT JOIN Dim_Clients c ON v.CUSTOMER_ID = c.CUSTOMER_ID
WHERE c.CUSTOMER_ID IS NULL;
-- RÉSULTAT : 0


-- 5. COMPARAISON DATE COMMERCIALE VS DATE LOG (L'ÉLÉMENT CLÉ)
-- (Prouve que l'ordinateur enregistre après la vente réelle)
SELECT 
    'Comparaison Temporelle' AS "Analyse",
    v.date_achat_excel AS "Date_Commerciale",
    date(l.date) AS "Date_Log_Systeme",
    COUNT(DISTINCT v.ID_BDD) AS "Nb_Ventes_Impactees"
FROM Fact_Ventes v
JOIN Logs l ON v.ID_BDD = l.id_bdd
WHERE v.date_achat_excel = 45518 
GROUP BY "Date_Log_Systeme";
-- RÉSULTAT : 
-- 45518 | 2024-08-14 | 39 998
-- 45518 | 2024-08-15 | 1 379
