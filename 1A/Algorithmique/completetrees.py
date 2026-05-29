import numpy as np
import pandas as pd

# Paramètres du vecteur aléatoire
mu = np.array([0, 0])  # Moyenne
Sigma = np.array([[1, 0.7],  # Matrice de covariance
                  [0.7, 1]])

# Générer 200 vecteurs gaussiens
n = 200
data = np.random.multivariate_normal(mu, Sigma, size=n)

# Convertir en DataFrame
df = pd.DataFrame(data, columns=["X1", "X2"])

# Sauvegarder la version originale en CSV
df.to_csv("vecteurs_gaussiens.csv", index=False)

# Lire le fichier CSV
df = pd.read_csv("vecteurs_gaussiens.csv")

# Multiplier chaque élément par 10^20
df_int = df.copy()
df_int["X1"] = df["X1"] * (10**20)
df_int["X2"] = df["X2"] * (10**20)

# Convertir en entiers
df_int["X1"] = df_int["X1"].astype(np.int64)
df_int["X2"] = df_int["X2"].astype(np.int64)

# Afficher le contenu
print("Contenu du fichier CSV (original) :")
print(df.head())

print("\nContenu après multiplication par 10^20 :")
print(df_int.head())

# Sauvegarder la version avec entiers
df_int.to_csv("vecteurs_gaussiens_entiers.csv", index=False)
print("\nFichier CSV avec entiers généré : vecteurs_gaussiens_entiers.csv")


