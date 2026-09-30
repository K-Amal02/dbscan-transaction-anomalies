# Détection d'anomalies par DBSCAN sur des transactions bancaires

Application de **DBSCAN** à la détection de transactions atypiques, accompagnée d'une petite application **Streamlit** de détection par règles.

## Contenu du dépôt

```
├── Tp_DBSCAN.ipynb              # Notebook : DBSCAN + graphique des k plus proches voisins
├── app.py                       # Application Streamlit (détection par règles)
├── data/transactions_fixed.csv  # Sous-échantillon de la base de données PaySim
├── requirements.txt
└── README.md
```

## Données

- Sous-échantillon du jeu de données **PaySim** ([Kaggle : ealaxi/paysim1](https://www.kaggle.com/datasets/ealaxi/paysim1)).
- 699 transactions, dont **2 frauduleuses** (`isFraud = 1`).

## Méthodes

### 1. DBSCAN (notebook)
- Variables : `amount` et `oldbalanceOrg`, standardisées (`StandardScaler`).
- Paramètres : `eps = 0.5`, `min_samples = 5`. `eps` est justifié par le graphique des k plus proches voisins (le coude de la courbe se situe autour de 0,3 à 0,6).
- Les points du cluster `-1` (bruit) sont considérés comme anomalies : **14 anomalies**.

### 2. Application Streamlit (règles)
- **Compte vidé** : `TRANSFER` ou `CASH_OUT` dont le montant est égal à l'ancien solde de l'émetteur.
- **Montant atypique** : montant supérieur au 95e percentile.

## Résultats et limites

| Approche | Alertes | Fraudes retrouvées (sur 2) |
|---|---|---|
| DBSCAN (`amount`, `oldbalanceOrg`) | 14 | 0 |
| Règle « compte vidé » | 2 | 2 |
| Règle « montant > P95 » | 35 | 0 |

- **DBSCAN détecte l'atypique, pas le frauduleux** : ses 14 anomalies (gros montants, soldes à 0) ne contiennent aucune des 2 fraudes, qui portent sur de petits montants.
- La règle « compte vidé » a été formulée en observant ces 2 mêmes fraudes (schéma connu de PaySim) : elle est plausible mais **non validée**.
- Les variables de soldes (`oldbalanceOrg`, etc.) ne sont pas fiables pour détecter la fraude dans PaySim.
- Avec des étiquettes, une approche supervisée serait plus adaptée ; DBSCAN sert ici à illustrer la détection d'anomalies par densité.

## Lancer le projet

```bash
pip install -r requirements.txt

# Notebook
jupyter notebook Tp_DBSCAN.ipynb

# Application Streamlit
streamlit run app.py      # puis importer data/transactions_fixed.csv
```