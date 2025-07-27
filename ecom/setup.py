#!/usr/bin/env python3
"""
Script de configuration automatique pour le projet ECOMMERCE
"""

import os
import sys
import subprocess
import json

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Terminé")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de {description}")
        print(f"Erreur: {e.stderr}")
        return False

def create_env_file():
    """Crée le fichier .env avec les configurations par défaut"""
    env_content = """# Configuration Django
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuration Base de données
DATABASE_NAME=ferme-d
DATABASE_USER=root
DATABASE_PASSWORD=
DATABASE_HOST=localhost
DATABASE_PORT=3306

# Configuration Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Configuration Médias
MEDIA_URL=/media/
STATIC_URL=/static/
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ Fichier .env créé")

def create_package_json():
    """Crée le package.json pour le frontend"""
    package_json = {
        "name": "ecommerce-frontend",
        "version": "1.0.0",
        "description": "Frontend React pour la plateforme e-commerce",
        "main": "index.js",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.8.0",
            "axios": "^1.3.0",
            "react-scripts": "5.0.1"
        },
        "devDependencies": {
            "tailwindcss": "^3.2.0",
            "autoprefixer": "^10.4.0",
            "postcss": "^8.4.0"
        },
        "browserslist": {
            "production": [
                ">0.2%",
                "not dead",
                "not op_mini all"
            ],
            "development": [
                "last 1 chrome version",
                "last 1 firefox version",
                "last 1 safari version"
            ]
        }
    }
    
    os.makedirs('frontend', exist_ok=True)
    with open('frontend/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)
    print("✅ Package.json créé pour le frontend")

def main():
    """Fonction principale de configuration"""
    print("🚀 Configuration du projet ECOMMERCE")
    print("=" * 50)
    
    # Vérifier si on est dans le bon répertoire
    if not os.path.exists('manage.py'):
        print("❌ Erreur: manage.py non trouvé. Assurez-vous d'être dans le répertoire du projet.")
        sys.exit(1)
    
    # Créer le fichier .env
    if not os.path.exists('.env'):
        create_env_file()
    
    # Créer les répertoires nécessaires
    directories = ['media', 'static', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Répertoire {directory} créé")
    
    # Installer les dépendances Python
    if run_command('pip install -r requirements.txt', 'Installation des dépendances Python'):
        print("✅ Dépendances Python installées")
    
    # Créer et appliquer les migrations
    run_command('python manage.py makemigrations', 'Création des migrations')
    run_command('python manage.py migrate', 'Application des migrations')
    
    # Créer le superutilisateur (optionnel)
    print("\n📝 Création du superutilisateur (optionnel)")
    create_superuser = input("Voulez-vous créer un superutilisateur maintenant? (y/N): ")
    if create_superuser.lower() == 'y':
        os.system('python manage.py createsuperuser')
    
    # Configuration du frontend
    create_package_json()
    
    print("\n🎉 Configuration terminée!")
    print("\n📋 Prochaines étapes:")
    print("1. Configurez votre base de données MySQL 'ferme-d'")
    print("2. Lancez le serveur: python manage.py runserver")
    print("3. Accédez à l'admin: http://127.0.0.1:8000/admin/")
    print("4. Pour le frontend: cd frontend && npm install && npm start")
    print("\n📖 Consultez le README.md pour plus d'informations")

if __name__ == '__main__':
    main()