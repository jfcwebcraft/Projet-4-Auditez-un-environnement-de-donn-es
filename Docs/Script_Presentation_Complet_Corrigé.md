# Script de Soutenance - Audit de l'Environnement de Données (SuperSmartMarket)

Ce document contient ton **discours oral (Commentaire)** et le **visuel des slides**. Le ton a été volontairement rendu plus "humain" et direct, comme celui d'un technicien qui explique son enquête à son responsable (Hugo).

---

## Slide 1 : Titre et Entrée en matière

**CONTENU VISUEL**
- **Titre** : Audit & Résilience du Système de Données
- **Sous-titre** : Résolution de l'Écart de Chiffre d'Affaires du 14 Août
- **Jean-François Chaussoy** - Data Engineer

**COMMENTAIRE ORAL**
> "Bonjour à tous. On va faire le point aujourd'hui sur l'audit que j'ai mené suite à l'alerte d'Hugo. Pour rappel, tout est parti d'une incohérence assez gênante sur le chiffre d'affaires de la mi-août. L'idée de ma mission, ce n'était pas juste de retrouver cet argent, mais surtout de comprendre ce qui cloche dans notre architecture pour qu'on puisse enfin s'appuyer sur des données fiables et auditables."

---

## Slide 2 : La "Casse du Siècle" ? (Le Problème)

**CONTENU VISUEL**
- **L'énigme** :
    - CA extrait le 14/08 au soir : **275 186,59 €**
    - CA affiché le 16/08 au matin : **284 243,88 €**
- **Le Delta** : **+ 9 057,29 €**
- **Question** : D'où vient cet argent apparu "par magie" ?

**COMMENTAIRE ORAL**
> "Le point de départ, c'est ce chiffre. On a un écart de plus de 9 000 euros entre l'extraction qu'Hugo a faite le jour J et ce que Power BI affiche 48 heures plus tard. Forfocément, on se demande tout de suite s'il y a eu une erreur de calcul, des prix qu'on aurait changé par erreur, ou pire, une fraude. Mon enquête a consisté à remonter le fil de l'eau, des tickets de caisse jusqu'aux logs du serveur, pour trouver l'explication logique."

---

## Slide 3 : Diagnostic de l'Existant (Le Chaos et les Failles)

**CONTENU VISUEL**
*(Une capture d'un tableau Excel "foutoir")*
- **Fichiers Isolés** : Ventes, Clients, Produits (Pas de lien).
- **Le bug "CUSTUMER_ID"** : Faute de frappe bloquante sur l'identifiant client.
- **Le danger "Gommage"** : 575 prix écrasés sans historique (SCD0).

**COMMENTAIRE ORAL**
> "En mettant le nez dans les fichiers Excel d'origine, on a vite vu les failles. C'était le 'Far West' : des fichiers déconnectés, une faute de frappe sur 'CUSTOMER_ID' qui cassait presque toutes les jointures, et surtout, aucun historique de prix. Concrètement, si un employé changeait un prix à la main, l'ancienne valeur disparaissait à jamais. C'est le genre de fragilité qui peut fausser tout un chiffre d'affaires rétroactivement."

---

## Slide 4 : La Solution - Le Pipeline de Données

**CONTENU VISUEL**
- **Flux** : Sources Excel ➔ Pipeline Python ➔ **Prototype SQLITE** ➔ BI.
- **Force** : Automatisation du nettoyage et de l'intégrité.

**COMMENTAIRE ORAL**
> "Pour stabiliser tout ça, j'ai conçu un pipeline de données. On ne travaille plus sur Excel directement. On passe par un script de nettoyage qui injecte tout dans un prototype SQLite. C'est ce passage par une 'vraie' base de données qui nous permet de garantir que les données sont propres avant même qu'Hugo ne sorte son premier rapport."

---

## Slide 5 : Le Schéma en Étoile (Star Schema)

**CONTENU VISUEL**
- **Diagramme ERD** : (Ta table Fact_Ventes au centre des 4 dimensions).
- **Atout** : Vitesse analytique et simplicité pour Power BI.

**COMMENTAIRE ORAL**
> "Au cœur du prototype, j'ai choisi un modèle en étoile. Pourquoi ? Parce que pour faire du reporting, c'est ce qu'il y a de plus robuste. Ça évite les jointures trop complexes qui ralentissent le système. On a les faits (les ventes) au milieu et les dimensions autour. C'est ce qui m'a permis de sortir très vite des analyses comme le Top 10 des clients, ce qu'on ne pouvait pas faire proprement avant."

---

## Slide 6 : L'Enquête - La Vérité par les Logs

**CONTENU VISUEL**
- **Gros Chiffre** : **207 489** lignes de logs analysées.
- **Diagnostic** :
    - Zéro suppression suspecte (Pas de fraude).
    - Zéro modification de ticket.
- **Le coupable** : Un décalage temporel d'injection.

**COMMENTAIRE ORAL**
> "On est arrivé au cœur de l'enquête. J'ai scanné plus de 207 000 lignes de logs. Au début, on a cherché des fraudes ou des suppressions sauvages : on n'a rien trouvé de ce côté. Par contre, en croisant les dates d'insertions, tout est devenu clair. Le 14 août, on a bien nos 39 000 ventes initiales. Mais le lendemain, le 15, le système a fini d'injecter 1 379 ventes supplémentaires, antidatées au 14. Voilà nos 9 057 euros : ce sont juste des ventes arrivées en retard en base de données."

---

## Slide 7 : Mission 3 - Un Système "Actif" et Sécurisé

**CONTENU VISUEL**
- **Triggers d'Audit** : (Les 4 gardiens).
- **RGPD** : Anonymisation des emails employés et hash des mots de passe.

**COMMENTAIRE ORAL**
> "Pour que Hugo n'ait plus jamais ce genre de surprise, j'ai rendu la base de données 'intelligente'. J'ai posé des verrous, ce qu'on appelle des Triggers. Si un prix est aberrant ou si une vente est orpheline, le système la bloque. J'ai aussi profité de ce prototype pour blinder la partie RGPD : les emails et les mots de passe sont désormais masqués ou hachés. On est passé d'un fichier Excel fragile à un système pro."

---

## Slide 8 : Recommandations Finales (Architecture Cible)

**CONTENU VISUEL**
- **Diagramme Architecture Cible** (Celui d'Excalidraw).
- **Les 4 points clés** :
    1. **date_insertion** : Séparer date commerciale et date système.
    2. **Gestion SCD2** : Créer une table `historique_prix`.
    3. **Supervision** : Automatisé l'analyse des logs.
    4. **Alerting** : Alerte Power BI si variation > 10%.

**COMMENTAIRE ORAL**
> "En conclusion, voici ce que je recommande pour l'avenir. D'abord, il faut impérativement garder ce champ `date_insertion` technique pour toujours savoir quand une donnée est arrivée. Ensuite, on doit installer une table d'historique de prix pour ne plus jamais 'écraser' le passé. Enfin, on installe un système d'alerte automatique : si le CA bouge trop d'un coup, Hugo reçoit un mail. Avec ces quatre piliers, SuperSmartMarket sécurise son pipeline de données pour de bon."

---

## Slide 9 : Conclusion - Prêt pour la MEP

**COMMENTAIRE ORAL**
> "Voilà pour cet audit. Aujourd'hui, le prototype prouve qu'on peut avoir des chiffres justes au centime près, avec une traçabilité totale. Hugo a désormais toutes les clés en main pour passer en production sur un environnement sain. Je vous remercie de m'avoir écouté."
