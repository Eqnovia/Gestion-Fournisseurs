# 🏭 Gestion Fournisseurs & Prix Produits

**Application Streamlit** pour rechercher, comparer et choisir le meilleur fournisseur pour chaque produit photovoltaïque et industriel.

![Streamlit](https://static.streamlit.io/examples/streamlit_logo_white.svg)

---

## 📝 Description

Cette application permet de :
- ✅ Gérer une base de fournisseurs et de produits
- ✅ Importer des fichiers Excel pour enrichir la base
- ✅ Rechercher des produits par designation, marque ou référence
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

### Installation

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

## 📦 Fonnalités

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

- **Streamlit** - Interface web interactive
- **Pandas** - Manipulation et traitement des données
- **Altair** - Visualisations graphiques
- **NumPy** - Calculs numériques

---

## 📁 Structure du projet

```
.
├── app.py              # Application Streamlit principale
├── Data Fournisseur.xlsx # Base de données initiale
├── requirements.txt    # Dépendances Python
└── README.md         # Cette documentation
```

---

## 📊 Aperçu

<p align="center">
  <img src="https://static.streamlit.io/examples/streamlit_logo_white.svg" alt="Streamlit Logo" width="200">
</p>

**Application de gestion de fournisseurs** - Comparez les prix, recherchez des produits et prenez des décisions d'achat éclairées.

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.