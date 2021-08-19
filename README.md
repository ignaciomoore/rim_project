# Tarea Examen de Recuperacin de Informacion Multimedia

Para este examen se uso Python 3 en Windows 10.

Se implemento un buscador de duplicaciones de audio para el dataset de la Tarea 2.
Se tomo como base la Tarea 2 del curso, el Anexo 4.1 y la memoria de Cristobal Muñoz que va adjunto en el repositorio.

Este proyecto se encuentra todo resumido en un jupyter notebook llamado evaluate.ipynb, pero se divide en tres partes:

## 1.- Extraer el audio de un video.

Para esto se necesita una herramineta llamada ffmpeg, la cual se llama mediante un comando, mas informacion en http://ffmpeg.org.
Tambien, se necesita definir el "Sample Rate" que usaran los audio, este valor sera el mismo para todos los audios que usara el programa, el archivo que hace esta separacion se llama audio_extractor.py.

## 2.- Generar descriptores de audio.

El archivo audio_descriptor_generator.py se encarga de generar los descriptores, hay tres variables que hay que definir antes de crear un descriptor:
    - El tamaño de la ventana, la cantidad de samples en un descriptor.
    - La dimension del descriptor, la cantidad de valores que tiene un descriptor.
    - El salto entre descriptores, la cantidad de saltos entre el inicio de cada ventana.

El tipo de descriptor que se usa para este proyecto es el MFCC, ya que es uno de los mas usados en el mercado y es muy bueno para encontrar similitudes entre descriptores.

## 3.- Buscar una secuencia repetida entre audios.

song_searcher.py y duplicate_searcher, entre otras, son los archivos de Python que se encargan de ver cuales descriptores tienen la menor distancia entre ellos, para esto se uso scipy.spatial.distance.cdist, una forma rapida de calcular la distancia entre cada par de descriptores y asi obtener los vecinos mas cercanos. Luego se aplica el algoritmo investigado por Cristobal Muñoz para ver que secuencias calzan y encontrar una duplicacion.


Los requerimientos del proyecto son los siguientes:

    jupyter==1.0.0
    librosa==0.8.1
    numpy==1.21.1
    scipy==1.7.0
    pandas==1.3.2
    prettytable==2.1.0

Y tambien tener instalado ffmpeg
