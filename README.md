# Tarea Examen de Recuperacin de Informacion Multimedia

Para este examen se uso Python 3 en Windows 10.

Se implemento un buscador de canciones en peliculas, pero tambien se puede aplicar a series, comerciales, videos y otras audios.
Se tomo como base la Tarea 2 del curso y el Anexo 4.1 que va adjunto en repositorio.

Este proyecto se divide en tres partes:

## 1.- Extraer el audio de un video.

Para esto se necesita una herramineta llamada ffmpeg, la cual se llama mediante un comando, mas informacion en http://ffmpeg.org.
Tambien, se necesita definir el "Sample Rate" que usaran los audio, este valor sera el mismo para todos los audios que usara el programa, el archivo que hace esta separacion se llama audio_extractor.py.

## 2.- Generar descriptores de audio.

El archivo audio_descriptor_generator.py se encarga de genearar los descriptores, hay tres variables que hay que definir antes de crear un descriptor:
    - El tamaño de la ventana, la cantidad de samples en un descriptor.
    - La dimension del descriptor, la cantidad de valores que tiene un descriptor.
    - El salto entre descriptores, la cantidad de saltos entre el inicio de cada ventana.

El tipo de descriptor que se usa para este proyecto es el MFCC, ya que es uno de los mas usados en el mercado y es muy bueno para encontrar similitudes entre descriptores.

## 3.- Buscar canciones en una pelicula.

song_searcher.py es el archivo de Python que se preocupa de ver cuales descriptores tienen la menor distancia entre ellos, para esto se uso scipy.spatial.distance.cdist, una forma rapida de calcular la distancia entre cada par de descriptores entre una cancion y una pelicula.

Usando una secuencia de descriptores con distancias pequeñas se puede encontarar una cancion en una pelicula.
