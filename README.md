# Projet 4 - Auditez un environnement de données (SuperSmartMarket)

Ce projet porte sur l'audit technique et la sécurisation de l'environnement de données de SuperSmartMarket, suite à une anomalie de chiffre d'affaires constatée le 14 août 2024.

---

## 📂 Structure du Projet

### [Livrables/](./Livrables)
Contient les documents officiels pour la soutenance :
- **Rapport d'Audit Exhaustif** (MD)
- **Support de Présentation** (PDF/PPTX)
- **Fiche d'Auto-évaluation**
- **Dictionnaire de Données** (XLSX)

### 📂 [Exercice 1 : Architecture](./Exercice%201)
Modélisation et documentation :
- Scripts de création du schéma en étoile (Star Schema).
- Dictionnaire des données technique.

### 📂 [Exercice 2 : Enquête](./Exercice%202)
Identification de l'origine de l'écart :
- Scripts SQL d'analyse des 207 489 lignes de logs.
- Preuve mathématique du delta de **+9 057,29 €**.

### 📂 [Exercice 3 : Résilience](./Exercice%203)
Sécurisation du système :
- Implémentation des **Triggers d'Audit**.
- Mesures de conformité **RGPD** (Anonymisation/Hash).
- Scripts de démonstration du prototype SQLite.

---

## Utilisation du Prototype

1. **Base de données** : Le prototype final est stocké dans `supersmartmarket.db`.
2. **Scripts SQL** : Tu peux exécuter les scripts du dossier `Exercice 3` pour vérifier l'intégrité du système et la traçabilité des logs.

---

## Auteur
**Jean-François Chaussoy** - Candidat Data Engineering (2025-2026)
Mentoré par : Mr Arnol Namegni
