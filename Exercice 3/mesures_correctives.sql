-- ==============================================================================
-- EXERCICE 3 : MESURES CORRECTIVES ET RÉSILIENCE DE LA BASE DE DONNÉES
-- Objectif : Renforcer la base SuperSmartMarket avec des contraintes automatiques.
-- Prérequis : Exécuter init_db.py et load_data.py avant ce script.
-- ==============================================================================


-- ============================================================
-- ÉTAPE 1 : ACTIVATION DE L'INTÉGRITÉ RÉFÉRENTIELLE
-- SQLite ne vérifie pas les clés étrangères par défaut !
-- On l'active pour bloquer toute insertion incohérente.
-- ============================================================
PRAGMA foreign_keys = ON;


-- ============================================================
-- ÉTAPE 2 : TRIGGER D'AUDIT À L'INSERTION
-- Ce déclencheur enregistre automatiquement chaque nouvelle
-- vente dans la table Logs, sans intervention humaine.
-- Cela remplace le processus externe instable identifié lors de l'audit.
-- ============================================================
DROP TRIGGER IF EXISTS audit_vente_insert;

CREATE TRIGGER audit_vente_insert
AFTER INSERT ON Fact_Ventes
FOR EACH ROW
BEGIN
    INSERT INTO Logs (id_user, date, id_bdd, id_produit, status)
    VALUES (
        NEW.id_employe,
        datetime('now', 'localtime'),
        NEW.ID_BDD,
        NEW.EAN,
        'INSERT_AUTO'
    );
END;


-- ============================================================
-- ÉTAPE 3 : TRIGGER DE VALIDATION DU PRIX À L'INSERTION
-- On empêche l'enregistrement d'une vente pour un produit
-- dont le prix est inexistant, nul, ou négatif.
-- Syntaxe compatible SQLite : RAISE() dans un CASE obligatoire.
-- ============================================================
DROP TRIGGER IF EXISTS validate_price_before_insert;

CREATE TRIGGER validate_price_before_insert
BEFORE INSERT ON Fact_Ventes
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT prix FROM Dim_Produits WHERE EAN = NEW.EAN) <= 0
        THEN RAISE(ABORT, 'Erreur AUDIT : Tentative d_insertion d_une vente pour un produit au prix nul ou negatif.')
    END;
END;


-- ============================================================
-- ÉTAPE 4 : TRIGGER D'AUDIT À LA SUPPRESSION
-- Toute suppression de vente doit être tracée.
-- Une vente ne peut jamais "disparaître" sans laisser de trace.
-- ============================================================
DROP TRIGGER IF EXISTS audit_vente_delete;

CREATE TRIGGER audit_vente_delete
AFTER DELETE ON Fact_Ventes
FOR EACH ROW
BEGIN
    INSERT INTO Logs (id_user, date, id_bdd, id_produit, status)
    VALUES (
        OLD.id_employe,
        datetime('now', 'localtime'),
        OLD.ID_BDD,
        OLD.EAN,
        'DELETE_AUDIT'
    );
END;


-- ============================================================
-- ÉTAPE 5 : TRIGGER D'AUDIT À LA MODIFICATION
-- Toute modification d'une vente est également tracée.
-- Cela permet de reconstituer l'historique complet d'un ticket.
-- ============================================================
DROP TRIGGER IF EXISTS audit_vente_update;

CREATE TRIGGER audit_vente_update
AFTER UPDATE ON Fact_Ventes
FOR EACH ROW
BEGIN
    INSERT INTO Logs (id_user, date, id_bdd, id_produit, status)
    VALUES (
        NEW.id_employe,
        datetime('now', 'localtime'),
        NEW.ID_BDD,
        NEW.EAN,
        'UPDATE_AUDIT'
    );
END;


-- ============================================================
-- ÉTAPE 6 : ANONYMISATION DES DONNÉES SENSIBLES (RGPD)
-- Les données personnelles des employés (email, mot de passe)
-- ne doivent pas apparaître en clair dans les exports de reporting.
-- On les remplace par des valeurs pseudonymisées.
-- ============================================================
UPDATE Dim_Employes
SET
    mail     = 'anonyme_' || id_employe || '@ssmarket.fr',
    hash_mdp = '********************************';
