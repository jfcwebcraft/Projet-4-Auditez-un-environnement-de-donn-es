# Tutoriel : Visualiser l'Audit dans Power BI

Ce tutoriel vous guide pour importer les données de votre prototype **MySQL (Docker)** vers Power BI Desktop.

---

## Étape 1 : Préparer la base de données
Nous utilisons une base de données **SQLite** (`supersmartmarket.db`) pour garantir la cohérence avec le diaporama de soutenance.

1.  **Lancez le script d'initialisation** :
    - Ouvrez un terminal dans le dossier du projet.
    - Tapez : `python "Exercice 3/init_sqlite_demo.py"`
2.  Le fichier **`supersmartmarket.db`** sera généré à la racine du dossier Exercice 3.

---

## Étape 2 : Importer dans Power BI
1.  Ouvrez **Power BI Desktop**.
2.  Cliquez sur **Obtenir les données** > **Plus...**.
3.  Cherchez **"SQLite"** ou utilisez le connecteur **ODBC** si vous avez installé le driver SQLite.
4.  **Alternative simple** : Vous pouvez aussi importer les fichiers CSV déjà présents dans le dossier `Exercice 3/csv/`. C'est la méthode la plus rapide.
    - Allez dans `Obtenir les données` > `Texte/CSV`.
    - Chargez `Fact_Ventes.csv`, `Dim_Produits.csv`, `Dim_Clients.csv`, `Logs.csv` et `Dim_Employes.csv`.

---

## Étape 3 : Nettoyage (Power Query)

> [!IMPORTANT]
> **En cas d'erreurs "Error" dans les cellules lors du changement de type :**
> Si Power BI affiche des erreurs, c'est que votre ordinateur attend une **virgule** alors que le fichier peut avoir des **points** (ou inversement).
> 1.  Faites un clic droit sur l'en-tête de la colonne (ex: `prix`).
> 2.  Sélectionnez **Modifier le type** > **En utilisant les paramètres régionaux...**.
> 3.  **Type de données** : Nombre décimal.
> 4.  **Paramètres régionaux** : Anglais (États-Unis).
> 5.  Validez. Cela "forcera" Power BI à lire les points comme des décimales sans erreur.

1.  **Vérifiez les types** :
    - `prix` dans la table Produits doit être en **Nombre décimal**.
    - `date_achat_excel` dans Ventes doit être en **Nombre entier**.
2.  Cliquez sur **Fermer et appliquer**.

---

## Étape 4 : Reproduire les Graphiques d'Audit

### 📈 1. Graphique en CASCADE (Audit du CA)
*   **Données** : Utilisez le bouton **"Entrer des données"** pour créer une table `Données_Cascade` :
    - Ligne 1 : `CA Initial (Matin)` | `275186,59`
    - Ligne 2 : `Impact Logs` | `9057,29`
*   **Visuel** : Sélectionnez **Waterfall chart** (icône escalier).
    - **Catégorie** : Champ `État`
    - **Axe Y** : Champ `Montant`

### 🏆 2. Top 10 CLIENTS (Histogramme)
*   **Visuel** : Sélectionnez **Histogramme groupé** (Barres bleues verticales).
*   **Champs** :
    - **Axe X** : `CUSTOMER_ID` (Table Clients)
    - **Axe Y** : `prix` (Table Produits)
*   **Filtre Top 10** :
    - Dans le volet **Filtres**, cliquez sur `CUSTOMER_ID`.
    - Type de filtre : **N premiers**.
    - Afficher les éléments : **10**.
    - Par valeur : Glissez le champ `prix`.
    - Cliquez sur **Appliquer le filtre**.

### 🍕 3. Analyse des LOGS (Graphique en Anneau)
*   **Visuel** : Sélectionnez **Graphique en anneau** (Donut chart).
*   **Champs** :
    - **Légende** : `status` (Table Logs).
    - **Valeurs** : `status` (Power BI fera un "Nombre de status" automatiquement).

### 🗺️ 4. Répartition par CATÉGORIE (Treemap)
*   **Visuel** : Sélectionnez **Treemap** (Icône avec des carrés de tailles variées).
*   **Champs** :
    - **Catégorie** : `categorie` (Table Produits).
    - **Valeurs** : `prix` (Table Produits).

---

## Étape 5 : Rappel sur les Relations (L'onglet Modèle)
Pour que les graphiques 2, 3 et 4 fonctionnent, vous devez impérativement tracer ces lignes dans l'onglet **Modèle** :
- `EAN` (Produits) ↔ `EAN` (Ventes)
- `CUSTOMER_ID` (Clients) ↔ `CUSTOMER_ID` (Ventes)
- `id_employe` (Employes) ↔ `id_employe` (Ventes)
- `ID_BDD` (Ventes) ↔ `id_bdd` (Logs)

---

## Étape 6 : Publication & Remise
Enregistrez votre travail sous le nom officiel : **`Chaussoy_Jean_Francois_2_dashboard_temporel_022026.pbix`**.
