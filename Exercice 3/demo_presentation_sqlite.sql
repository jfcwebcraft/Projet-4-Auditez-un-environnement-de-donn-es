-- ==============================================================================
-- PROJET 4 - AUDITEZ UN ENVIRONNEMENT DE DONNÉES
-- DOSSIER DE DÉMONSTRATION "EN DIRECT" (SQLITE)
-- À utiliser dans "DB Browser for SQLite" ou un outil similaire.
-- ==============================================================================

-- 🚀 PRÉPARATION DU TEST
-- On insère un employé et un client de test si besoin (sécurité IF NOT EXISTS)
INSERT OR IGNORE INTO Dim_Employes (id_employe, prenom, nom) VALUES ('EMP_DEMO', 'Jean', 'Francois');
INSERT OR IGNORE INTO Dim_Clients (CUSTOMER_ID) VALUES ('CUST_DEMO');
INSERT OR IGNORE INTO Dim_Produits (EAN, Libelle_produit, prix) VALUES (111, 'Article Test Valide', 10.00);
INSERT OR IGNORE INTO Dim_Produits (EAN, Libelle_produit, prix) VALUES (000, 'Article Test Erreur', 0.00);


-- 🛡️ TEST 1 : LE TRIGGER DE SÉCURITÉ (VALIDATION DE PRIX)
-- Tentative d'insérer un produit à 0 €
-- RÉSULTAT ATTENDU : Erreur bloquante "Erreur AUDIT : Tentative d'insertion..."
INSERT INTO Fact_Ventes (ID_BDD, CUSTOMER_ID, id_employe, EAN, date_achat_excel)
VALUES ('DEMO_ERR_1', 'CUST_DEMO', 'EMP_DEMO', 000, 45518);


-- ✅ TEST 2 : INSERTION VALIDE ET TRAÇABILITÉ AUTOMATIQUE
-- On insère une vente correcte
-- RÉSULTAT ATTENDU : Succès de l'insertion
INSERT INTO Fact_Ventes (ID_BDD, CUSTOMER_ID, id_employe, EAN, date_achat_excel, ID_ticket)
VALUES ('DEMO_OK_1', 'CUST_DEMO', 'EMP_DEMO', 111, 45518, 'TKT_DEMO_001');


-- 🔍 TEST 3 : VÉRIFICATION DU LOG AUTOMATIQUE (RÉSILIENCE)
-- On vérifie que le système a créé une preuve sans intervention humaine.
-- Note : Le nouveau statut est 'INSERT_AUTO' pour le distinguer des anciens logs.
SELECT * FROM Logs WHERE id_bdd = 'DEMO_OK_1';


-- 📊 TEST 4 : VÉRIFICATION DE LA CONFORMITÉ RGPD
-- On vérifie que les données sensibles de l'employé démo sont bien masquées.
SELECT id_employe, prenom, nom, mail, hash_mdp 
FROM Dim_Employes 
WHERE id_employe = 'EMP_DEMO';


-- 📉 TEST 5 : L'ENQUÊTE TECHNIQUE (Preuve finale du delta)
-- Cette requête isole précisément les 1 379 ventes tardives du 15 août.
SELECT 
    date(l.date) AS "Etape_Enregistrement", 
    COUNT(DISTINCT v.ID_BDD) AS "Volume_Ventes", 
    ROUND(SUM(p.prix)/5, 2) AS "Chiffre_Affaires_EUR"
FROM Fact_Ventes v 
JOIN Logs l ON v.ID_BDD = l.id_bdd 
JOIN Dim_Produits p ON v.EAN = p.EAN 
WHERE v.date_achat_excel = 45518 AND l.status = 'INSERT' 
GROUP BY 1;
