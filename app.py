import streamlit as st
import pandas as pd

st.title(" Détection de Fraude 🚨")

# Upload d'un fichier 
uploaded_file = st.file_uploader("Importer un fichier CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Lire le fichier CSV
        df = pd.read_csv(uploaded_file, sep=None, engine="python")

        st.success(" Fichier chargé avec succès !")

        # Convertir les colonnes numériques en float
        numeric_cols = ["amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Vérifier les colonnes attendues
        expected_columns = [
            "step", "type", "amount", "nameOrig", "oldbalanceOrg", 
            "newbalanceOrig", "nameDest", "oldbalanceDest", 
            "newbalanceDest", "isFraud", "isFlaggedFraud"
        ]

        missing_cols = [col for col in expected_columns if col not in df.columns]
        if missing_cols:
            st.error(f" Colonnes manquantes dans le fichier : {missing_cols}")
        else:
            st.success(" Toutes les colonnes nécessaires sont présentes.")

            # Détection des Fraudes
            # Seuil calculé sur les données (95e percentile), après la conversion numérique
            seuil_montant = df["amount"].quantile(0.95)

            def detect_fraud(row):
                if row["type"] in ["TRANSFER", "CASH_OUT"] and row["oldbalanceOrg"] > 0 and row["amount"] == row["oldbalanceOrg"]:
                    return " COMPTE VIDÉ"
                elif row["amount"] > seuil_montant:
                    return " MONTANT ATYPIQUE"
                else:
                    return " OK"

            df["Fraude"] = df.apply(detect_fraud, axis=1)

            # Affichage des transactions et des fraudes détectées
            st.write("### 🔎 Aperçu des Transactions :")
            st.dataframe(df[["step", "type", "amount", "nameOrig", "nameDest", "Fraude"]].head(20))

            # Nombre de fraudes détectées
            fraude_count = df[df["Fraude"] != " OK"].shape[0]
            st.warning(f" Nombre de transactions suspectes : {fraude_count}")

            # Afficher uniquement les transactions frauduleuses
            if fraude_count > 0:
                st.write("### 🚨 Transactions Suspectes ")
                st.dataframe(df[df["Fraude"] != " OK"])

    except Exception as e:
        st.error(f" Erreur lors de la lecture du fichier : {e}")

else:
    st.warning("📂 Veuillez importer un fichier CSV (.csv).")
