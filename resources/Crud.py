from flask import Flask, jsonify, request
from flask_cors import CORS
import bcrypt
import mysql.connector

app = Flask(__name__)
CORS(app)

# Configuração da conexão com o banco de dados (substitua pelos seus próprios valores)
db_config = {
    'host': 'localhost',
    'database': 'site_consciencia_negra',
    'user': 'root',
    'password': 'root'
}

def get_database_connection():
    return mysql.connector.connect(**db_config)

def serialize_movie(movie):
    return {
        'id': movie['id'],
        'title': movie['title'],
        'sinopse': movie['sinopse'],
        'date': movie['date'],
        'duration': str(movie['duration']),  # Convertendo timedelta para string
        'classification': movie['classification'],
        'image_url': movie['image_url']
    }

# Auth #

# Register
@app.route('/auth/register', methods=['POST'])
def register():
    name = request.form.get('name')
    password = request.form.get('password')

    try:
        with get_database_connection() as conn, conn.cursor() as cursor:
            # Gera um salt aleatório
            salt = bcrypt.gensalt()
            
            # Gera o hash da senha utilizando o salt
            hashed_senha = bcrypt.hashpw(password.encode('utf-8'), salt)

            query = "SELECT name FROM users WHERE name = %s"
            cursor.execute(query, (name,))
            existing_user = cursor.fetchone()
            if existing_user:
                return jsonify({"message": "Nome de usuário já cadastrado"}), 409

            query = "INSERT INTO users (name, password, salt) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, hashed_senha, salt))
            conn.commit()

        return jsonify({"message": "Cadastro bem-sucedido"})

    except mysql.connector.Error as e:
        return jsonify({"message": "Cadastro mal-sucedido"}), 500

# Login
@app.route('/auth/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')

    try:
        with get_database_connection() as conn, conn.cursor() as cursor:
            query = "SELECT * FROM users WHERE name = %s"
            cursor.execute(query, (name,))
            user = cursor.fetchone()

        if user:
            stored_hashed_password = user[2]  # Índice correspondente à coluna 'password' na tabela

            # Verifica se as senhas coincidem
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                # Login bem-sucedido
                return jsonify({"message": "Login bem-sucedido"})

        # Login falhou
        return jsonify({"message": "Nome de usuário ou senha incorretos"}), 401

    except mysql.connector.Error as e:
        return jsonify({"message": f"Erro ao processar login. Erro: {e}"}), 500

# Movies #

# Index
@app.route('/api/movies', methods=['GET'])
def get_movies():
    try:
        with get_database_connection() as conn, conn.cursor(dictionary=True) as cursor:
            query_movies = "SELECT * FROM movies"
            cursor.execute(query_movies)
            movies = cursor.fetchall()

        # Converter datetime e timedelta para strings antes de enviar a resposta
        serialized_movies = [serialize_movie(movie) for movie in movies]

        return jsonify({'movies': serialized_movies})

    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao obter filmes"}), 500

# Create
@app.route('/api/movies', methods=['POST'])
def add_movie():
    try:
        with get_database_connection() as conn, conn.cursor() as cursor:
            data = request.get_json()
            new_movie = {
                'title': data['title'],
                'sinopse': data['sinopse'],
                'date': data['date'],
                'duration': data['duration'],
                'classification': data['classification'],
                'image_url': data['image_url'],
            }

            # Adicione lógica para inserir no banco de dados
            query = "INSERT INTO movies (title, sinopse, date, duration, classification, image_url) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (
                new_movie['title'],
                new_movie['sinopse'],
                new_movie['date'],
                new_movie['duration'],
                new_movie['classification'],
                new_movie['image_url']
            ))

            conn.commit()

            return jsonify({'message': 'Filme adicionado com sucesso', 'movie': new_movie}), 201

    except mysql.connector.Error as e:
        return jsonify({'message': f'Erro ao adicionar filme. Erro: {e}'}), 500
    
#Get By Id
@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        query = "SELECT * FROM movies WHERE id = %s"
        cursor.execute(query, (movie_id,))
        movie = cursor.fetchone()

    if movie:
        return jsonify({'movie': serialize_movie(movie)})
    
    return jsonify({'message': 'Filme não encontrado'}), 404

# Get By Name
@app.route('/api/movies/<str:movie_name>', methods=['GET'])
def get_movie(movie_name):
    with get_database_connection() as conn, conn.cursor() as cursor:
        query = "SELECT * FROM movies WHERE name = %s"
        cursor.execute(query, (movie_name,))
        movie = cursor.fetchone()

    if movie:
        return jsonify({'movie': serialize_movie(movie)})
    
    return jsonify({'message': 'moviee não encontrado'}), 404

# Update By Id
@app.route('/api/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        try:
            title = request.json.get('title')
            sinopse = request.json.get('sinopse')
            date = request.json.get('date')
            duration = request.json.get('duration')
            classification = request.json.get('classification')
            image_url = request.json.get('image_url')

            # Check if all fields are filled
            if title and sinopse and date and duration and classification and image_url:
                query = 'UPDATE movies SET title=%s, sinopse=%s, date=%s, duration=%s, classification=%s, image_url=%s WHERE id=%s'
                cursor.execute(query, (title, sinopse, date, duration, classification, image_url, movie_id))
                return jsonify({'message': 'Filme atualizado com sucesso'}), 200
        
            return jsonify({'message': 'Todos os campos precisam ser preenchidos!'})
        
        except mysql.connector.Error as e:
            return jsonify({'message': 'Erro ao atualizar o filme'}), 500

# Delete By Id
@app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        try:
            query = "DELETE FROM movies WHERE id = %s"
            cursor.execute(query, (movie_id,))
            conn.commit()

            return jsonify({'message': 'Filme deletado com sucesso'})
        
        except mysql.connector.Error as e:
            return jsonify({'message': 'Erro ao deletar o filme'}), 500

# Comments #

# Index
@app.route('/api/comments', methods=['GET'])
def get_comments():
    try:
        with get_database_connection() as conn, conn.cursor(dictionary=True) as cursor:
            query_comments = "SELECT * FROM comments"
            cursor.execute(query_comments)
            comments = cursor.fetchall()

        return jsonify({'comments': comments})

    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao obter comentários"}), 500

# Create
@app.route('/api/comments', methods=['POST'])
def add_comment():
    try:
        with get_database_connection() as conn, conn.cursor() as cursor:
            data = request.get_json()
            new_comment = {
                'user_id': data['user_id'],
                'type_id': data['type_id'],
                'type': data['type'],
                'text': data['text'],
                'date': data['date']
            }

            # Adicione lógica para inserir no banco de dados
            query = "INSERT INTO comments (user_id, type_id, type, text, date) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (
                new_comment['user_id'],
                new_comment['type_id'],
                new_comment['type'],
                new_comment['text'],
                new_comment['date']
            ))

            conn.commit()

            return jsonify({'message': 'Comentado sucesso', 'comment': new_comment}), 201

    except mysql.connector.Error as e:
        return jsonify({'message': f'Erro ao adicionar filme. Erro: {e}'}), 500
    
#Get By User_Id
@app.route('/api/comments/<int:user_id>', methods=['GET'])
def get_comments_by_user_id(user_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        query = "SELECT * FROM comments WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        comments = cursor.fetchall()

    if comments:
        return jsonify({'comments': comments})
    
    return jsonify({'message': 'Comentários não encontrados'}), 404

#Get By User_Name
@app.route('/api/comments/<str:user_name>', methods=['GET'])
def get_comments_by_user_name(user_name):
    with get_database_connection() as conn, conn.cursor() as cursor:
        query = "SELECT * FROM users WHERE name = %s"
        cursor.execute(query, (user_name,))
        user = cursor.fetchall()

        if user:
            user_id = user[0]['id']
            query = "SELECT * FROM comments WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            comments = cursor.fetchall()

    if comments:
        return jsonify({'comments': comments})
    
    return jsonify({'message': 'Comentários não encontrados'}), 404

# Get By Type_Id
@app.route('/api/comments/<str:type>/<int:type_id>', methods=['GET'])
def get_comments_by_type_id(type, type_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        query = "SELECT * FROM comments WHERE type = %s AND type_id = %s"
        cursor.execute(query, (type, type_id))
        comments = cursor.fetchone()

    if comments:
        return jsonify({'comments': comments})
    
    return jsonify({'message': 'Comentários não encontrados'}), 404

# Get By Type
@app.route('/api/comments/<str:type>', methods=['GET'])
def get_comments_by_type(type):
    with get_database_connection() as conn, conn.cursor() as cursor:
        query = "SELECT * FROM comments WHERE type = %s"
        cursor.execute(query, (type,))
        comments = cursor.fetchone()

    if comments:
        return jsonify({'comments': comments})
    
    return jsonify({'message': 'Comentários não encontrados'}), 404

# Update By Id
@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        try:
            user_id = request.json.get('user_id')
            type_id = request.json.get('type_id')
            type = request.json.get('type')
            text = request.json.get('text')
            date = request.json.get('date')

            # Check if all fields are filled
            if user_id and type_id and type and text and date:
                query = 'UPDATE comments SET user_id=%s, type_id=%s, type=%s, text=%s, date=%s= WHERE id=%s'
                cursor.execute(query, (user_id, type_id, type, text, date, comment_id))
                return jsonify({'message': 'Comentário atualizado com sucesso'}), 200
        
            return jsonify({'message': 'Todos os campos precisam ser preenchidos!'})
        
        except mysql.connector.Error as e:
            return jsonify({'message': 'Erro ao atualizar o comentário'}), 500
    
# Delete By Id
@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        try:
            query = "DELETE FROM comments WHERE id = %s"
            cursor.execute(query, (comment_id,))
            conn.commit()

            return jsonify({'message': 'Comentário deletado com sucesso'})
        
        except mysql.connector.Error as e:
            return jsonify({'message': 'Erro ao deletar o comentário'}), 500
        
# Delete By User_id
@app.route('/api/comments/<int:user_id>', methods=['DELETE'])
def delete_comment_by_user_id(user_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        try:
            query = "DELETE FROM comments WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            conn.commit()

            return jsonify({'message': 'Comentários deletado com sucesso'})
        
        except mysql.connector.Error as e:
            return jsonify({'message': 'Erro ao deletar os comentários'}), 500
        
# Delete By Type
@app.route('/api/comments/<str:type>', methods=['DELETE'])
def delete_comment(type):
    with get_database_connection() as conn, conn.cursor() as cursor:
        try:
            query = "DELETE FROM comments WHERE type = %s"
            cursor.execute(query, (type,))
            conn.commit()

            return jsonify({'message': 'Comentários deletados com sucesso'})
        
        except mysql.connector.Error as e:
            return jsonify({'message': 'Erro ao deletar os comentários'}), 500
        
# Delete By Type_Id
@app.route('/api/comments/<str:type>/<int:type_id>', methods=['DELETE'])
def delete_comment(type, type_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        try:
            query = "DELETE FROM comments WHERE type = %s AND type_id = %s"
            cursor.execute(query, (type, type_id))
            conn.commit()

            return jsonify({'message': 'Comentário deletado com sucesso'})
        
        except mysql.connector.Error as e:
            return jsonify({'message': 'Erro ao deletar o comentário'}), 500

# Events #

# Index
@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        with get_database_connection() as conn, conn.cursor(dictionary=True) as cursor:
            query_events = "SELECT * FROM events"
            cursor.execute(query_events)
            events = cursor.fetchall()

        return jsonify({'events': events})

    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao obter eventos"}), 500

# Create
@app.route('/api/events', methods=['POST'])
def add_event():
    try:
        with get_database_connection() as conn, conn.cursor() as cursor:
            data = request.get_json()
            new_event = {
                'title': data['title'],
                'description': data['description'],
                'date': data['date'],
                'local': data['local']
            }

            # Adicione lógica para inserir no banco de dados
            query = "INSERT INTO events (title, description, date, local) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (
                new_event['title'],
                new_event['description'],
                new_event['date'],
                new_event['local']
            ))

            conn.commit()

            return jsonify({'message': 'Evento adicionado com sucesso', 'event': new_event}), 201

    except mysql.connector.Error as e:
        return jsonify({'message': f'Erro ao adicionar evento'}), 500
    
#Get By Id
@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        query = "SELECT * FROM events WHERE id = %s"
        cursor.execute(query, (event_id,))
        event = cursor.fetchone()

    if event:
        return jsonify({'event': event})
    
    return jsonify({'message': 'Evento não encontrado'}), 404

# Get By Name
@app.route('/api/events/<str:event_name>', methods=['GET'])
def get_event(event_name):
    with get_database_connection() as conn, conn.cursor() as cursor:
        query = "SELECT * FROM events WHERE name = %s"
        cursor.execute(query, (event_name,))
        event = cursor.fetchone()

    if event:
        return jsonify({'event': event})
    
    return jsonify({'message': 'Evento não encontrado'}), 404

# Get By Date
@app.route('/api/events/<str:date>', methods=['GET'])
def get_event(date):
    with get_database_connection() as conn, conn.cursor() as cursor:
        query = "SELECT * FROM events WHERE date = %s"
        cursor.execute(query, (date,))
        events = cursor.fetchall()

    if events:
        return jsonify({'event': events})
    
    return jsonify({'message': 'Evento não encontrado'}), 404

# Get By Local
@app.route('/api/events/<str:local>', methods=['GET'])
def get_event(local):
    with get_database_connection() as conn, conn.cursor() as cursor:
        query = "SELECT * FROM events WHERE local = %s"
        cursor.execute(query, (local,))
        events = cursor.fetchall()

    if events:
        return jsonify({'event': events})
    
    return jsonify({'message': 'Evento não encontrado'}), 404

# Get By Date And Local
@app.route('/api/events/<str:date>/<str:local>', methods=['GET'])
def get_event(date, local):
    with get_database_connection() as conn, conn.cursor() as cursor:
        query = "SELECT * FROM events WHERE date = %s AND local = %s"
        cursor.execute(query, (date, local))
        events = cursor.fetchall()

    if events:
        return jsonify({'events': events})
    
    return jsonify({'message': 'Evento não encontrado'}), 404

# Update By Id
@app.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        try:
            title = request.json.get('title')
            description = request.json.get('description')
            date = request.json.get('date')
            local = request.json.get('local')

            # Check if all fields are filled
            if title and description and date and local:
                query = 'UPDATE events SET title=%s, description=%s, date=%s, local=%s WHERE id=%s'
                cursor.execute(query, (title, description, date, local, event_id))
                return jsonify({'message': 'Evento atualizado com sucesso'}), 200
        
            return jsonify({'message': 'Todos os campos precisam ser preenchidos!'})
        
        except mysql.connector.Error as e:
            return jsonify({'message': 'Erro ao atualizar o evento'}), 500

# Delete By Id
@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        try:
            query = "DELETE FROM events WHERE id = %s"
            cursor.execute(query, (event_id,))
            conn.commit()

            return jsonify({'message': 'Evento deletado com sucesso'})
        
        except mysql.connector.Error as e:
            return jsonify({'message': 'Erro ao deletar o evento'}), 500

# Photos #

# Index
@app.route('/api/photos', methods=['GET'])
def get_photos():
    try:
        with get_database_connection() as conn, conn.cursor(dictionary=True) as cursor:
            query_photos = "SELECT * FROM photos"
            cursor.execute(query_photos)
            photos = cursor.fetchall()

        return jsonify({'photos': photos})

    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao obter fotos"}), 500

# Create
@app.route('/api/photos', methods=['POST'])
def add_photo():
    try:
        with get_database_connection() as conn, conn.cursor() as cursor:
            data = request.get_json()
            new_photo = {
                'image_url': data['image_url'],
                'caption': data['caption'],
                'date': data['date'],
            }

            # Adicione lógica para inserir no banco de dados
            query = "INSERT INTO photos (image_url, caption, date) VALUES (%s, %s, %s)"
            cursor.execute(query, (
                new_photo['image_url'],
                new_photo['caption'],
                new_photo['date'],
            ))

            conn.commit()

            return jsonify({'message': 'Foto adicionada com sucesso', 'photo': new_photo}), 201

    except mysql.connector.Error as e:
        return jsonify({'message': 'Erro ao adicionar foto'}), 500
    
#Get By Id
@app.route('/api/photos/<int:photo_id>', methods=['GET'])
def get_photo(photo_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        query = "SELECT * FROM photos WHERE id = %s"
        cursor.execute(query, (photo_id,))
        photo = cursor.fetchone()

    if photo:
        return jsonify({'photo': photo})
    
    return jsonify({'message': 'Foto não encontrado'}), 404

# Get By Date
@app.route('/api/photos/<str:date>', methods=['GET'])
def get_photo(date):
    with get_database_connection() as conn, conn.cursor() as cursor:
        query = "SELECT * FROM photos WHERE date = %s"
        cursor.execute(query, (date,))
        photos = cursor.fetchall()

    if photos:
        return jsonify({'photo': photos})
    
    return jsonify({'message': 'photoo não encontrado'}), 404

# Update By Id
@app.route('/api/photos/<int:photo_id>', methods=['PUT'])
def update_photo(photo_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        try:
            image_url = request.json.get('image_url')
            caption = request.json.get('caption')
            date = request.json.get('date')

            # Check if all fields are filled
            if image_url and caption and date:
                query = 'UPDATE photos SET image_url=%s, caption=%s, date=%s WHERE id=%s'
                cursor.execute(query, (image_url, caption, date, photo_id))
                return jsonify({'message': 'photoo atualizado com sucesso'}), 200
        
            return jsonify({'message': 'Todos os campos precisam ser preenchidos!'})
        
        except mysql.connector.Error as e:
            return jsonify({'message': 'Erro ao atualizar o photoo'}), 500

# Delete By Id
@app.route('/api/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    with get_database_connection() as conn, conn.cursor() as cursor:
        try:
            query = "DELETE FROM photos WHERE id = %s"
            cursor.execute(query, (photo_id,))
            conn.commit()

            return jsonify({'message': 'photoo deletado com sucesso'})
        
        except mysql.connector.Error as e:
            return jsonify({'message': 'Erro ao deletar o photoo'}), 500


if __name__ == '__main__':
    app.run(debug=True)