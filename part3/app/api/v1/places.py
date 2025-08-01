from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

# NOUVEAUX IMPORTS NÉCESSAIRES POUR LA CORRECTION
from app.models.place import Place
from app import db

api = Namespace('places', description='Place operations')

# --- Les modèles (api.model) restent les mêmes ---

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        try:
            current_user_id = get_jwt_identity()
            data = api.payload

            # --- DÉBUT DE LA CORRECTION ---
            # On crée l'objet Place nous-mêmes pour être sûr que owner_id est bien utilisé.
            new_place = Place(
                title=data.get('title'),
                description=data.get('description'),
                price=data.get('price'),
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                owner_id=current_user_id  # On assigne directement l'ID de l'utilisateur du token
            )

            # On sauvegarde directement dans la base de données
            db.session.add(new_place)
            db.session.commit()
            # --- FIN DE LA CORRECTION ---

            return new_place.to_dict(), 201
        except Exception as e:
            db.session.rollback() # Important en cas d'erreur
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

# --- Le reste du fichier (PlaceResource pour GET/PUT) reste identique ---

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'unauthorized - not the owner')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user_id = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        if not is_admin and place.owner_id != current_user_id:
            return {'error':'unauthorized - you can only modify your own places'}, 403
        try:
            updated_place = facade.update_place(place_id, api.payload)
            return updated_place.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
