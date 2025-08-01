from app import create_app, db

app = create_app()

# Ajout de ce bloc pour créer les tables si elles n'existent pas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Assure-toi que le port est spécifié si besoin
    app.run(debug=True, host='0.0.0.0', port=5000)