let moviesData = [];
let commentsData = [];
let palavrasOfensivas;
let currentMovieIndex = 0;

const apiUrl = 'http://localhost:5000';

async function fetchMoviesData() {
    const response = await fetch(`${apiUrl}/api/movies`);
    const data = await response.json();
    moviesData = data.movies;
    commentsData = data.comments;
    
    return data;
}

// Inicialmente, obtenha todos os dados dos filmes
fetchMoviesData().then(movieData => {
    // Crie os cartões do carrossel
    const movieCarousel = document.getElementById('movie-carousel');
    const numMovies = movieData.movies.length;

    // Clone as primeiras e últimas imagens para criar o efeito circular
    movieData.movies.forEach((movie, index) => {
        // if (index === 0) {
        //     // Clone as últimas imagens no início do carrossel
        //     const cloneCard = document.createElement('div');
        //     cloneCard.className = 'movie-card';
        //     cloneCard.innerHTML = `<img src="${movieData.movies[numMovies - 1].image_url}" alt="${movieData.movies[numMovies - 1].title}">`;
        //     cloneCard.addEventListener('click', () => showMovie(numMovies + index));
        //     movieCarousel.appendChild(cloneCard);
        // }

        const movieCard = document.createElement('div');
        movieCard.className = 'movie-card';
        movieCard.innerHTML = `<img src="${movie.image_url}" alt="${movie.title}">`;
        movieCard.addEventListener('click', () => showMovie(index));
        movieCarousel.appendChild(movieCard);

        // if (index === numMovies - 1) {
        //     // Clone as primeiras imagens no final do carrossel
        //     const cloneCard = document.createElement('div');
        //     cloneCard.className = 'movie-card';
        //     cloneCard.innerHTML = `<img src="${movieData.movies[0].image_url}" alt="${movieData.movies[0].title}">`;
        //     cloneCard.addEventListener('click', () => showMovie(index - numMovies));
        //     movieCarousel.appendChild(cloneCard);
        // }
    });

    // Mostre os detalhes e os comentários para o primeiro filme
    showMovie(0);
});

function showMovie(index) {
    currentMovieIndex = index;
    const screenWidth = window.innerWidth;
    const movieWidth = 300;  // Substitua isso pela largura real da imagem do filme em pixels
    const spacing = 10;  // Ajuste o espaçamento conforme necessário

    // Calcula o offset para centralizar a imagem
    const offset = -(index * (movieWidth + spacing)) + (screenWidth - movieWidth) / 2;

    document.getElementById('movie-carousel').style.transform = `translateX(${offset}px)`;
    const cards = document.getElementById('movie-carousel').getElementsByClassName('movie-card');
    for (let index = 0; index < cards.length; index++) {
        cards[index].style.transform = 'scale(1)';
    }
    cards[index].style.transform = 'scale(1.1)';

    // Obtenha os dados do filme do cache
    const movieData = moviesData[index];
    const movieComments = commentsData.filter((commentData) => {return movieData.id === commentData.type_id;});

    if (movieData) {
        document.getElementById('movie-title').innerText = movieData.title;
        document.getElementById('movie-sinopse').innerText = movieData.sinopse;
        document.getElementById('movie-date').innerText = `Date: ${movieData.date}`;
        document.getElementById('movie-duration').innerText = `Duration: ${movieData.duration}`;
        document.getElementById('movie-classification').innerText = `Classification: ${movieData.classification}`;

        const commentsList = document.getElementById('comments-list');
        commentsList.innerHTML = '';
        movieComments.forEach(comment => {
            const li = document.createElement('li');
            li.textContent = comment.text;
            commentsList.appendChild(li);
        });
    }
}

// Funções para controlar a navegação
function nextMovie() {
    showMovie((currentMovieIndex < moviesData.length - 1) ? currentMovieIndex + 1 : 0);
}

function prevMovie() {
    showMovie((currentMovieIndex > 0) ? currentMovieIndex - 1 : moviesData.length - 1);
}

function addComment() {
    const commentInput = document.getElementById('comment-input');
    const commentText = commentInput.value;

    if (commentText.trim() !== '' && verificaComentario(commentText)) {

        const commentsList = document.getElementById('comments-list');
        const newComment = document.createElement('li');
        newComment.textContent = commentText;
        commentsList.appendChild(newComment);

        commentsData.push({
            type: 'movies',
            type_id: moviesData[currentMovieIndex]['id'],
            date: Date.now,
            text: commentText
        });

        commentInput.value = '';
    }
}

// Simula a leitura de palavras ofensivas de um arquivo
async function getPalavrasOfensivas() {
    try {
        // Substitua a URL abaixo pela localização real do seu arquivo de palavras ofensivas
        const response = await fetch('/resources/palavroes.txt');
        
        if (!response.ok) {
            throw new Error('Falha ao obter palavras ofensivas.');
        }

        const palavras = await response.text();
        palavrasOfensivas = new Set(palavras.split('\n').map(palavra => palavra.toLowerCase().trim()));
        // Separa as palavras com base em quebras de linha ou outros delimitadores
    } catch (error) {
        console.error(error);
        palavrasOfensivas = [];
    }
}

function verificaComentario(comentario) {
    comentario = removeNumerosComoLetras(comentario.trim());

    // Expressões regulares para dividir o comentário em palavras
    const tokens = comentario.toLowerCase().match(/\b\w+\b/g) || [];
    const lemas = tokens.map(token => token.toLowerCase()); // Aqui você poderia aplicar lematização se necessário

    for (const palavra of palavrasOfensivas) {
        if (tokens.includes(palavra) || comentario.includes(palavra) || lemas.includes(palavra)) {
            return false;
        }
    }
    return true;
}


function removeNumerosComoLetras(texto) {
    // Mapeamento de números para letras
    const mapeamento = {
        '0': 'o',
        '1': 'i',
        '!': 'i',
        '3': 'e',
        '4': 'a',
        '5': 's',
        '7': 't',
    };

    // Substitui os números pelos caracteres correspondentes
    for (const numero in mapeamento) {
        const letra = mapeamento[numero];
        const regex = new RegExp(numero, 'g');
        texto = texto.replace(regex, letra);
    }

    return texto;
}

getPalavrasOfensivas();