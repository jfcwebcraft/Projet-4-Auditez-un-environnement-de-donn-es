# Questions Pièges Potentielles - Soutenance Projet 4

Voici une sélection de questions "pièges" ou d'approfondissement qu'un jury pourrait te poser pour tester la solidité de ton audit et de ton prototype.

---

## 🛠️ Thématique Technique (SQL & Modélisation)

### 1. "Pourquoi avoir choisi un modèle en Étoile plutôt qu'un modèle en Flocon ?"
*   **Réponse suggérée :** Le modèle en étoile est plus performant pour la Business Intelligence (BI) car il limite les jointures complexes. Dans notre cas, les dimensions ne sont pas assez complexes pour justifier une normalisation en "flocon" (qui ralentirait les rapports Power BI).

### 2. "Les Triggers ralentissent les performances de la base. N'auriez-vous pas pu faire ces contrôles côté application ?"
*   **Réponse suggérée :** C'est vrai, une base avec énormément de triggers peut ralentir. Cependant, pour SuperSmartMarket, la priorité était la **sécurité absolue de la donnée** (intégrité). En mettant le contrôle dans la BDD (Trigger), on s'assure qu'aucune vente invalide ne rentre, qu'elle vienne de l'application de caisse, d'un script import massif ou d'une correction manuelle. C'est une "ceinture de sécurité" ultime.

### 3. "Quelle est la différence entre OLTP et OLAP ? Votre MySQL est-il les deux ?"
*   **Réponse suggérée :** MySQL est ici utilisé comme un système **OLTP** (Online Transactional Processing) : il gère les transactions quotidiennes rapidement. Pour l'analyse décisionnelle (l'audit), on passe sur un modèle **OLAP** (Online Analytical Processing), comme ce que fait Power BI. Le modèle en étoile que j'ai créé fait le pont entre les deux.

### 4. "Comment votre base MySQL garantit-elle la fiabilité des données (Propriétés ACID) ?"
*   **Réponse suggérée :** MySQL (moteur InnoDB) respecte les propriétés **ACID** :
    *   **Atomicité** : Une vente est enregistrée en entier ou pas du tout.
    *   **Cohérence** : Les Triggers et contraintes empêchent les données aberrantes.
    *   **Isolation** : Deux ventes simultanées ne s'entrechoquent pas.
    *   **Durabilité** : Une fois validée, la vente est inscrite sur le disque (Docker volume).

---

## 🔍 Thématique Audit & Méthodologie

### 4. "Comment pouvez-vous être SÛR que le delta de 9 057,29 € n'est pas une fraude ?"
*   **Réponse suggérée :** L'audit des logs a montré que les tickets correspondent à des transactions réelles, cohérentes avec les stocks et les horaires. La découverte clé a été le timestamp d'insertion : les données ont été enregistrées en base APRÈS l'extraction BI du matin, mais datées du 14 août. C'est un problème de **synchro (Batch)** et non une manipulation volontaire de chiffres.

### 6. "Pourquoi utiliser Python pour l'audit au lieu de faire directement des requêtes SQL ?"
*   **Réponse suggérée :** Python permet de manipuler des fichiers volumineux plus souplement (Pandas) et d'automatiser le processus. Comme vu dans les cours, SQL est l'outil de stockage, mais Python est parfait pour le **Data Wrangling** (nettoyage) complexe avant d'importer dans un entrepôt de données.

### 7. "Auriez-vous pu utiliser des Window Functions (fonctions de fenêtrage) pour l'audit ?"
*   **Réponse suggérée :** Oui ! Par exemple, `LAG()` ou `LEAD()` auraient permis de comparer chaque vente avec la précédente pour détecter des doublons temporels ou des sauts suspects dans les `ID_ticket`, ce qui est très utile pour repérer des anomalies de caisse.

---

## 🛡️ Thématique Sécurité & RGPD

### 9. "Qui sont les acteurs clés de la donnée en entreprise et quel est votre rôle vis-à-vis d'eux ?"
*   **Réponse suggérée :** 
    *   Le **DPO** (Data Protection Officer) pour la conformité RGPD.
    *   Le **RSSI** (Sécurité Systèmes) pour la protection contre le vol.
    *   Le **CDO** (Chief Data Officer) pour la stratégie.
    *   Mon rôle en tant qu'auditeur est de fournir au **CDO** des données fiables et au **DPO** une garantie que les données sensibles sont protégées (anonymisation).

---

## 📊 Thématique Power BI & Dashboarding

### 10. "Quand utilisez-vous Power Query (M) plutôt que des mesures DAX ?"
*   **Réponse suggérée :** Power Query est utilisé pour le **nettoyage et la structuration** (filtrer les lignes, pivoter les colonnes). Le DAX est utilisé pour le **calcul dynamique** (comparer le CA de ce mois-ci par rapport au mois dernier). On nettoie d'abord (M), on calcule ensuite (DAX).

### 11. "Comment avez-vous géré la 'réconciliation des données' évoquée dans le cours ?"
*   **Réponse suggérée :** La réconciliation a été faite en créant des relations entre la table `Fact_Ventes` et les dimensions. En Power BI, j'ai vérifié que les directions des relations étaient correctes (un-à-plusieurs) pour éviter les erreurs d'agrégation.

---

## 👨‍💼 Questions Spécifiques d'Hugo (Jury)

### 12. "Quelles sont les tables concernées par les modifications apportées par vos Triggers ?"
*   **Réponse suggérée :** 
    *   Le trigger `validate_price_before_insert` surveille la table `Dim_Produits` pour bloquer les prix <= 0.
    *   Le trigger `audit_vente_insert` surveille `Fact_Ventes` et écrit automatiquement dans la table `Logs`. Ceci garantit que chaque modification importante est tracée sans intervention humaine.

### 13. "Qui a réalisé les actions loguées dans votre système ?"
*   **Réponse suggérée :** Les logs tracent les actions par `id_employe`. Cela permet d'identifier quelle caisse ou quel opérateur a déclenché l'opération. En production, on ajouterait aussi le `user_système` et l'adresse IP de la machine pour une traçabilité totale (Sécurité RSSI).

### 14. "Quels sont les risques d'automatiser (Triggers) l'insertion ou la suppression de données ?"
*   **Réponse suggérée :** 
    *   **Risque de blocage** : Un trigger mal codé peut bloquer tout le processus de vente (ex: un trigger qui plante empêche le ticket de caisse de s'enregistrer).
    *   **Performance** : Sur des millions de lignes, trop de triggers peuvent ralentir la base.
    *   **Maintenance** : La logique est "cachée" dans la base. Un nouveau développeur pourrait ne pas voir qu'un trigger modifie les données dans son dos.
    *   *Conclusion* : Il faut les utiliser avec parcimonie pour les règles critiques d'intégrité, et bien les documenter.
