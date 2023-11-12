from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import datetime

app = Flask(__name__)
CORS(app)

# Dados de exemplo
conn = mysql.connector.connect(
    host='localhost',
    database='site_consciencia_negra',
    user='root',
    password='root'
)

cursor = conn.cursor(dictionary=True)  # Use dictionary=True para obter resultados como dicionários

query = "SELECT * FROM movies"
cursor.execute(query)
    
movies = cursor.fetchall()

query = "SELECT * FROM comments WHERE type = 'movies'"
cursor.execute(query)

comments = cursor.fetchall()
        
cursor.close()
conn.close()

def serialize_timedelta(value):
    if isinstance(value, datetime.timedelta):
        return str(value)
    return value

# Rotas para filmes
@app.route('/api/movies', methods=['GET'])
def get_movies():
    # Converter datetime e timedelta para strings antes de enviar a resposta
    serialized_movies = [
        {key: serialize_timedelta(value) if isinstance(value, (datetime.datetime, datetime.timedelta)) else value for key, value in movie.items()} for movie in movies
    ]

    return jsonify({
        'movies': serialized_movies,
        'comments': comments
    })

if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/api/films/<int:film_id>', methods=['GET'])
# def get_film(film_id):
#     film = next((film for film in films if film['id'] == film_id), None)
#     if film:
#         return jsonify({'film': film})
#     return jsonify({'message': 'Filme não encontrado'}), 404

# @app.route('/api/films', methods=['POST'])
# def add_film():
#     data = request.get_json()
#     new_film = {
#         'id': len(films) + 1,
#         'title': data['title'],
#         'sinopse': data['sinopse'],
#         'date': data['date'],
#         'duration': data['duration'],
#         'classification': data['classification'],
#         'image_url': data['image_url'],
#     }
#     films.append(new_film)
#     return jsonify({'message': 'Filme adicionado com sucesso', 'film': new_film}), 201

# @app.route('/api/films/<int:film_id>', methods=['PUT'])
# def update_film(film_id):
#     film = next((film for film in films if film['id'] == film_id), None)
#     if film:
#         data = request.get_json()
#         film.update(data)
#         return jsonify({'message': 'Filme atualizado com sucesso', 'film': film})
#     return jsonify({'message': 'Filme não encontrado'}), 404

# @app.route('/api/films/<int:film_id>', methods=['DELETE'])
# def delete_film(film_id):
#     global films
#     films = [film for film in films if film['id'] != film_id]
#     return jsonify({'message': 'Filme excluído com sucesso'}), 200

# # Rotas para comentários
# @app.route('/api/comments', methods=['GET'])
# def get_comments():
#     return jsonify({'comments': comments})

# @app.route('/api/comments/<int:comment_id>', methods=['GET'])
# def get_comment(comment_id):
#     comment = next((comment for comment in comments if comment['id'] == comment_id), None)
#     if comment:
#         return jsonify({'comment': comment})
#     return jsonify({'message': 'Comentário não encontrado'}), 404

# @app.route('/api/comments', methods=['POST'])
# def add_comment():
#     data = request.get_json()
#     new_comment = {
#         'id': len(comments) + 1,
#         'type': data['type'],
#         'type_id': data['type_id'],
#         'text': data['text'],
#     }
#     comments.append(new_comment)
#     return jsonify({'message': 'Comentário adicionado com sucesso', 'comment': new_comment}), 201

# @app.route('/api/comments/<int:comment_id>', methods=['PUT'])
# def update_comment(comment_id):
#     comment = next((comment for comment in comments if comment['id'] == comment_id), None)
#     if comment:
#         data = request.get_json()
#         comment.update(data)
#         return jsonify({'message': 'Comentário atualizado com sucesso', 'comment': comment})
#     return jsonify({'message': 'Comentário não encontrado'}), 404

# @app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
# def delete_comment(comment_id):
#     global comments
#     comments = [comment for comment in comments if comment['id'] != comment_id]
#     return jsonify({'message': 'Comentário excluído com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)
