document.addEventListener('DOMContentLoaded', function () {
    // Obtén el contenedor de la lista de canciones
    const songListContainer = document.getElementById('cancionSeleccionada');
    // Obtén el elemento de audio
    const audioElement = document.getElementById('player');
    // Obtén la imagen de la canción
    const songImage = document.getElementById('songImage');
    // Almacena el estado de reproducción
    let isPlaying = false;
    // Función para pausar o reanudar la canción al hacer clic en la imagen
    function togglePlayPause() {
        if (isPlaying) {
            audioElement.pause();
        } else {
            audioElement.play();
        }
        isPlaying = !isPlaying;
    }

    // Agrega un evento de clic a la imagen para pausar o reanudar la canción
    songImage.addEventListener('click', togglePlayPause);

    // Agrega un evento de clic derecho al contenedor de la lista
    songListContainer.addEventListener('contextmenu', function (event) {
        // Detén el comportamiento predeterminado del menú contextual
        event.preventDefault();

        // Verifica si el clic derecho fue en un elemento de la lista
        const songItem = event.target.closest('li');
        if (songItem) {
            // Almacena la canción seleccionada para su posterior descarga
            const songName = songItem.textContent;

            // Realiza la solicitud de descarga al backend (cambió a GET)
            window.location.href = `/downloadSong/${encodeURIComponent(songName)}`;
        }
    });
    // Muestra el contenedor-info al cargar la página
    const containerInfo = document.querySelector('.container-info');
    containerInfo.style.display = 'block';

    // Oculta el contenedor-info después de 1 minuto
    setTimeout(function () {
        containerInfo.style.display = 'none';
    }, 30000); // 60000 milisegundos = 1 minuto
});

// Este archivo está intencionalmente en blanco
const cancionSeleccionada = document.getElementById('cancionSeleccionada');
const player = document.getElementById('player');
const audioSource = document.getElementById('audioSource');
const songImage = document.getElementById('songImage');
const downloadMessage = document.getElementById('downloadMessage');
const nombreCancion = document.getElementById('nombreCancion');

// ... (tu código existente)

// Variable para almacenar todas las canciones
const songListItems = document.querySelectorAll('#cancionSeleccionada li');

// Evento clic en la lista de canciones
cancionSeleccionada.addEventListener('click', async function (event) {
    // Obtiene el texto dentro del elemento clickeado (el nombre de la canción)
    const selectedSong = event.target.textContent;

    // Verifica si la opción seleccionada no es "none"
    if (selectedSong) {
        const songUrl = `/music/${encodeURIComponent(selectedSong)}.mp3`;
        const imageUrl = `/static/img/${encodeURIComponent(selectedSong)}.jpg`;


        try {
            // Carga la canción y la imagen
            await Promise.all([
                loadAudio(songUrl),
                loadImage(imageUrl)
            ]);

            // Ambos han cargado correctamente, ahora podemos reproducir la canción
            player.load();
            player.play();
            songImage.style.display = "block"; // Muestra el elemento songImage
            nombreCancion.textContent = selectedSong;

            // Agregar el evento 'ended' al reproductor de audio
            player.addEventListener('ended', function () {
                // Cuando la canción actual haya terminado, elige una canción aleatoria
                const randomIndex = Math.floor(Math.random() * songListItems.length);
                const randomSong = songListItems[randomIndex];

                // Configura la URL del reproductor de audio con la nueva canción aleatoria
                const randomSongName = randomSong.textContent;
                const randomSongUrl = `/music/${randomSongName}.mp3`;
                const randomImageUrl = `/static/img/${randomSongName}.jpg`;

                // Carga la nueva canción y la imagen aleatoria
                Promise.all([
                    loadAudio(randomSongUrl),
                    loadImage(randomImageUrl)
                ]).then(() => {
                    // Reproduce la nueva canción aleatoria
                    player.load();
                    player.play();
                    nombreCancion.textContent = randomSongName;
                }).catch(error => {
                    console.error('Error al cargar la canción o la imagen:', error);
                });
            });
        } catch (error) {
            console.error('Error al cargar la canción o la imagen:', error);
        }
    } else {
        // Si la opción seleccionada es "none", oculta la imagen del logo
        songImage.src = "";
        location.reload(); // Recarga la página
    }
});


// Función para cargar la canción
async function loadAudio(url) {
    return new Promise((resolve, reject) => {
        audioSource.src = url;
        player.load();
        player.oncanplaythrough = resolve;
        player.onerror = reject;
    });
}

// Función para cargar la imagen
async function loadImage(url) {
    return new Promise((resolve, reject) => {
        songImage.src = url;
        songImage.onload = resolve;
        songImage.onerror = reject;
    });
}

// Función para descargar una canción
async function downloadSong() {
    try {
        const urlInput = document.getElementById('urlInput');
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: urlInput.value
            })
        });

        const data = await response.json();
        downloadMessage.textContent = `Descarga exitosa. Título: ${data.message}, se autorefrescará en 3 segundos.`;

        // Actualizar la lista de canciones recargando la página después de la descarga exitosa
        setTimeout(function () {
            location.reload();
        }, 3000);
    } catch (error) {
        console.error('Error al descargar la canción:', error);
        downloadMessage.textContent = 'Error al descargar la canción.';
    }


}

const searchInput = document.getElementById('searchInput');

// Array para almacenar todas las canciones (sin filtros)
const allSongs = Array.from(cancionSeleccionada.children);

// Escucha los cambios en la barra de búsqueda
searchInput.addEventListener('input', function () {
    const searchTerm = searchInput.value.toLowerCase();
    // Filtra las canciones según el término de búsqueda
    const filteredSongs = allSongs.filter(song => song.textContent.toLowerCase().includes(searchTerm));
    // Muestra solo las canciones filtradas
    allSongs.forEach(song => song.style.display = filteredSongs.includes(song) ? 'block' : 'none');
});