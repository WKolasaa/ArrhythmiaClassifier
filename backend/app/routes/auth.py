from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from app.utils.jwt import generate_token

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    """
        Register a new user
        ---
        tags:
          - Auth
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - email
                - password
                - role
              properties:
                email:
                  type: string
                password:
                  type: string
                role:
                  type: string
                  enum: [doctor, admin]
        responses:
          201:
            description: User registered successfully
          400:
            description: Bad input
          409:
            description: User already exists
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON"}), 400

        required_fields = {"email", "password", "role"}
        if not required_fields.issubset(data):
            return jsonify({"error": "Missing fields"}), 400

        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already exists"}), 409

        user = User(email=data["email"], role=data["role"])
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@bp.route('/login', methods=['POST'])
def login():
    """
        User login and token generation
        ---
        tags:
          - Auth
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  example: test@example.com
                password:
                  type: string
                  example: yourpassword123
        responses:
          200:
            description: Login successful
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Login successful
                token:
                  type: string
                  example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
                user:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    email:
                      type: string
                      example: test@example.com
                    role:
                      type: string
                      example: doctor
          400:
            description: Bad request or missing fields
          401:
            description: Invalid credentials
    """
    data = request.get_json()

    if not data or not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'Missing fields'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = generate_token(user)

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role
        }
    }), 200
