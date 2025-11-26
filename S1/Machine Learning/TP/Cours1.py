import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn as sk

data = pd.read_csv("employees.csv", index_col=0)
print(data.shape)
print(data.head())
print(data.describe())
print(data.dtypes)

if 'Salary' in data.columns:
    salary_col = data.pop('Salary')
    data['Salary'] = salary_col
print("\nData Types after moving Salary column:")
print(data.dtypes)

data = data.replace(['-', 'na'], np.nan)
print("Data head after replacing non-standard NaNs:")
print(data.head())

data = data.replace(['-', 'na'], np.nan)

data['Gender'] = data['Gender'].fillna('Male')
print("\nData head after filling NaNs:")
print(data.head())
print("\nNull values count per column:")
print(data.isnull().sum())


if 'Start Date' in data.columns:
    data_copy = data.copy()
    data_copy['Start Date'] = pd.to_datetime(data_copy['Start Date'], errors='coerce')
    today = pd.Timestamp('today')
    data_copy['Years_Service'] = (today - data_copy['Start Date']).dt.days / 365.25
    data_copy['Years_Service'] = pd.to_numeric(data_copy['Years_Service'], errors='coerce')
    print(data_copy[['Start Date', 'Years_Service']].head())


Q1 = data.quantile(0.25, numeric_only=True)
Q3 = data.quantile(0.75, numeric_only=True)
IQR = Q3 - Q1
print("Q1 \n",Q1)
print("Q3 \n",Q3)
print("IQR \n",IQR)
print("\n")
data.boxplot()
plt.title("Boxplot for Numerical Columns")
plt.show()

print(data.describe())


plt.figure(figsize=(8,5))
sns.histplot(data['Salary'].dropna(), bins=20, kde=True, color='blue', edgecolor='black')
plt.title("Histogramme et densité des salaires")
plt.xlabel("Salaire")
plt.ylabel("Fréquence / Densité")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


data['Bonus_Category'] = pd.cut(data['Bonus %'], bins=[0, 7, 14, 20], labels=['Low Bonus', 'Medium Bonus', 'High Bonus'])

plt.figure(figsize=(10, 6))
sns.histplot(
    data=data.dropna(subset=['Salary', 'Bonus_Category']),
    x='Salary',
    hue='Bonus_Category',
    multiple='stack',
    bins=20,
    kde=True,
    palette='viridis',
    edgecolor='black'
)
plt.title("Distribution des Salaires par Catégorie de Bonus (%)", fontsize=14)
plt.xlabel("Salaire")
plt.ylabel("Fréquence / Densité")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

########
########

plt.figure(figsize=(10, 6))
sns.scatterplot(
    x='Salary',
    y='Bonus %',
    hue='Gender',
    data=data.dropna(subset=['Salary', 'Bonus %', 'Gender']),
    palette={'Male': 'blue', 'Female': 'red'},
    edgecolor='black',
    alpha=0.7
)

plt.title('Relation entre le Salaire et le Bonus (%) par Genre', fontsize=14)
plt.xlabel('Salaire', fontsize=12)
plt.ylabel('Bonus (%)', fontsize=12)
plt.legend(title='Genre (Gender)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

#######


sns.histplot(x='Gender', hue='Gender', data=data, kde=True, palette=['green', 'purple'], multiple='dodge', bins=30)
plt.title("Comparaison de la Distribution des Salaires par Genre", fontsize=14)
plt.xlabel("Gender")
plt.ylabel("Fréquence / Densité")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


######

plt.figure(figsize=(10, 5))
sns.histplot(
    data=data.dropna(subset=['Salary', 'Senior Management']),
    x='Salary',
    hue='Senior Management',
    multiple='dodge',
    bins=30,
    kde=True,
    palette={True: 'darkgreen', False: 'red'},
    edgecolor='black'
)
plt.title("Distribution des Salaires par Senior Management", fontsize=16)
plt.xlabel("Salaire", fontsize=12)
plt.ylabel("Fréquence / Densité", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


#####

plt.figure(figsize=(12, 7))
sns.histplot(
    data=data.dropna(subset=['Salary', 'Team']),
    x='Salary',
    hue='Team',
    multiple='stack',
    bins=30,
    kde=True,
    palette='tab20',
    edgecolor='black'
)
plt.title("Distribution des Salaires par (Team)", fontsize=16)
plt.xlabel("Salaire", fontsize=12)
plt.ylabel("Fréquence / Densité", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


#######
plt.figure(figsize=(12, 7))
sns.histplot(
    data=data.dropna(subset=['Team', 'Team']),
    x='Team',
    hue='Team',
    multiple='stack',
    bins=30,
    kde=True,
    palette='tab20',
    edgecolor='black'
)
plt.title("Distribution des Salaires par (Team)", fontsize=16)
plt.xlabel("Team", fontsize=12)
plt.ylabel("Fréquence / Densité", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
#######



plt.figure(figsize=(8, 5))
plt.hist(data_copy['Years_Service'].dropna(), bins=20, color='skyblue', edgecolor='black')
plt.title("Histogramme de l'ancienneté (Years of Service)")
plt.xlabel("Années de service")
plt.ylabel("Nombre d'employés")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(data=data_copy, x='Years_Service', y='Salary', color='dodgerblue', s=70, edgecolor='black', alpha=0.8)
plt.title("Relation entre l'Ancienneté et le Salaire")
plt.xlabel("Années de service")
plt.ylabel("Salaire")
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()


plt.figure(figsize=(8,5))
plt.hist(data_copy['Years_Service'], bins=20, weights=data_copy['Salary'], color='skyblue', edgecolor='black', alpha=0.8)
plt.title("Histogramme de l'Ancienneté pondéré par le Salaire")
plt.xlabel("Années de service")
plt.ylabel("Salaire total")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()