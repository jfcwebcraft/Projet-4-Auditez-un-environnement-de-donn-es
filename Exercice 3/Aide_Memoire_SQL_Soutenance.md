# 📝 Aide-Mémoire SQL - Soutenance SuperSmartMarket

Ce document contient toutes les commandes prêtes à être copiées dans ton **SQL Shell** (`sql_shell.bat`) pour ta démonstration en direct.

---

## 🔍 1. Exploration (Découverte)
*Pour montrer au jury que tu maîtrises la structure de ta base.*

```sql
-- Voir toutes les tables
.tables

-- Voir les colonnes d'une table (ex: Produits)
.schema Dim_Produits

-- Voir les 5 premiers produits
SELECT Libelle_produit, Rayon, prix FROM Dim_Produits LIMIT 5;
```

---

## 🛡️ 2. Démonstration de la Résilience (Triggers)
*Pour prouver que ton système est auto-protecteur et auditable.*

### A. Test de Blocage (Prix Invalide)
*Cette requête DOIT échouer grâce au Trigger `validate_price_before_insert`.*
```sql
INSERT INTO Fact_Ventes (id_employe, EAN, ID_BDD, Quantite) 
VALUES ('EMP_TEST', 111, 'TEST_ERREUR', 1);
-- Résultat attendu : "❌ Erreur SQL : Prix invalide : insertion refusee"
```

### B. Test de Traçabilité (Audit Automatique)
*On insère une vente valide et on vérifie qu'elle a été loguée instantanément.*
```sql
-- 1. Insertion d'une vente valide
INSERT INTO Fact_Ventes (id_employe, EAN, ID_BDD, Quantite) 
VALUES ('EMP_SOLO', 123456, 'VENTE_OK', 2);

-- 2. Vérification immédiate dans les logs
SELECT * FROM Logs ORDER BY id_log DESC LIMIT 1;
-- Résultat attendu : Une ligne avec status 'INSERT_AUTO' et id_user 'EMP_SOLO'.
```

---

## 📊 3. Preuve de l'Audit (Delta CA)
*Pour expliquer au jury comment tu as trouvé les 9 057,29 € manquants.*

```sql
SELECT 
    CASE WHEN status = 'INSERT_AUTO' THEN 'Ventes Normales' ELSE 'Ventes Retardées' END as Groupe,
    COUNT(*) as Nb_Ventes, 
    SUM((SELECT prix FROM Dim_Produits WHERE EAN = l.id_produit)) * 5 as CA_Total
FROM Logs l
GROUP BY Groupe;
```

---

## 🔒 4. Conformité RGPD (Anonymisation)
*Pour montrer que les données sensibles des employés sont protégées.*

```sql
SELECT id_employe, prenom, nom, mail, hash_mdp 
FROM Dim_Employes 
LIMIT 3;
-- Résultat attendu : 'prenom' et 'nom' sont réels, mais 'mail' et 'hash_mdp' sont à 'None' ou masqués.
```

---

## 🧹 5. Nettoyage de la Démo
*Pour remettre la base à zéro si tu veux recommencer ton test.*
```sql
DELETE FROM Fact_Ventes WHERE id_employe IN ('EMP_SOLO', 'EMP_TEST');
DELETE FROM Logs WHERE id_user IN ('EMP_SOLO', 'EMP_TEST');
```
