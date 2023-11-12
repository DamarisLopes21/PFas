<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
header("Access-Control-Allow-Credentials: true");
header("Content-Type: application/json");

$servername = "localhost:3306";
$username = "root";
$password = "root";
$dbname = "site_consciencia_negra";

// Criar conexão
$conn = new mysqli($servername, $username, $password, $dbname);

// Verificar conexão
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

    // Ler filmes
    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
        $movies = array();
        $comments = array();
        $result = $conn->query("SELECT * FROM films");
        while ($row = $result->fetch_assoc()) {
            $movies[] = $row;
        }

        $result = $conn->query("SELECT * FROM comments where type = 'films'");

        while ($row = $result->fetch_assoc()) {
            $comments[] = $row;
        }

        $responseData = array('movies' => $movies, 'comments' => $comments);
        echo json_encode($responseData);
    }

    // Criar filme
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $data = json_decode(file_get_contents("php://input"), true);

        $title = $data['title'];
        $sinopse = $data['sinopse'];
        $image_url = $data['image_url'];

        $stmt = $conn->prepare("INSERT INTO films (title, sinopse, image_url) VALUES (?, ?, ?)");
        $stmt->bind_param("sss", $title, $sinopse, $image_url);

        if ($stmt->execute()) {
            echo json_encode(array('message' => 'Movie created successfully'));
        } else {
            echo json_encode(array('message' => 'Error creating movie'));
        }
    }

    // Atualizar filme
    if ($_SERVER['REQUEST_METHOD'] === 'PUT') {
        $data = json_decode(file_get_contents("php://input"), true);
        $movieId = $data['id'];
        $title = $data['title'];
        $sinopse = $data['sinopse'];
        $image_url = $data['image_url'];

        $stmt = $conn->prepare("UPDATE films SET title=?, sinopse=?, image_url=? WHERE id=?");
        $stmt->bind_param("sssi", $title, $sinopse, $image_url, $movieId);

        if ($stmt->execute()) {
            echo json_encode(array('message' => 'Movie updated successfully'));
        } else {
            echo json_encode(array('message' => 'Error updating movie'));
        }
    }

    // Excluir filme
    if ($_SERVER['REQUEST_METHOD'] === 'DELETE') {
        $data = json_decode(file_get_contents("php://input"), true);
        $movieId = $data['id'];

        $stmt = $conn->prepare("DELETE FROM films WHERE id=?");
        $stmt->bind_param("i", $movieId);

        if ($stmt->execute()) {
            echo json_encode(array('message' => 'Movie deleted successfully'));
        } else {
            echo json_encode(array('message' => 'Error deleting movie'));
        }
    }

$conn->close();
?>
