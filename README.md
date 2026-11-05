# 🏭 Gestion Fournisseurs & Prix Produits

**Application Streamlit** pour rechercher, comparer et choisir le meilleur fournisseur pour chaque produit photovoltaïque et industriel.

🌐 **Application en ligne :** [https://eqnovia-gestion-fournisseurs.streamlit.app/](https://eqnovia-gestion-fournisseurs.streamlit.app/)

---

## 📝 Description

Cette application permet de :
- ✅ Gérer une base de fournisseurs et de produits
- ✅ Importer des fichiers Excel pour enrichir la base
- ✅ Rechercher des produits par désignation, marque ou référence
- ✅ Comparer les prix entre différents fournisseurs
- ✅ Visualiser les meilleures offres avec tableau de prix
- ✅ Télécharger les résultats en CSV
- ✅ Graphiques d'évolution des prix

La base contient déjà des données de référence provenant de multiples fournisseurs (CLEANERGY, NEXANS, HUAWEI, JINKO SOLAR, etc.).

---

## 🚀 Démarrage rapide

### Prérequis

- Python 3.8 ou supérieur
- pip

### Installation locale

```bash
# Cloner le dépôt
git clone <votre-repo>
cd <dossier-du-projet>

# Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### Lancer l'application

```bash
streamlit run app.py
```

L'application ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`.

---

## 📦 Fonctionnalités

### Onglet "🏭 Liste des fournisseurs"
- Vue d'ensemble des fournisseurs avec métriques clés
- Cartes interactives par fournisseur
- Navigation vers les produits d'un fournisseur sélectionné

### Onglet "🔎 Recherche produit"
- Recherche textuelle (désignation, marque, référence)
- Filtres par poste et marque
- Identification de la meilleure offre
- Tableau comparatif avec mise en évidence du prix le plus bas
- Graphique d'évolution des prix par fournisseur
- Bouton de téléchargement CSV

### Onglet "📊 Comparateur multi-produits"
- Sélection multiple de produits à comparer
- Tableau pivot avec les prix minimum par fournisseur
- Identification du meilleur fournisseur par produit

---

## 🛠️ Technologies utilisées

<p align="left">
  <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" alt="Streamlit" height="50" style="margin-right: 15px;"/>
  <img src="https://pandas.pydata.org/static/img/pandas_white.svg" alt="Pandas" height="50" style="margin-right: 15px;"/>
  <img src="https://altair-viz.github.io/_static/altair-logo-light.png" alt="Altair" height="50" style="margin-right: 15px;"/>
  <img src="https://numpy.org/images/logo.svg" alt="NumPy" height="50" style="margin-right: 15px;"/>
  <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" height="50"/>
</p>

- **Streamlit** - Interface web interactive
- **Pandas** - Manipulation et traitement des données
- **Altair** - Visualisations graphiques
- **NumPy** - Calculs numériques
- **Python** - Langage principal

---

## 📁 Structure du projet

```text
.
├── app.py                  # Application Streamlit principale
├── requirements.txt        # Dépendances Python
└── README.md               # Cette documentation
```

*(Note : Les données de base sont intégrées directement dans le code `app.py` pour un déploiement facile sur Streamlit Cloud).*

---

## 🌐 Déploiement sur Streamlit Cloud

1. Poussez votre code sur un dépôt GitHub public.
2. Allez sur [share.streamlit.io](https://share.streamlit.io/).
3. Connectez votre compte GitHub.
4. Sélectionnez votre dépôt, la branche (`main`) et le fichier principal (`app.py`).
5. Cliquez sur **Deploy!**

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request
