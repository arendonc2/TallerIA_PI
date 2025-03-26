import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images in the database from an images folder"

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images'

        if not os.path.exists(images_folder):
            self.stderr.write(f"Folder '{images_folder}' not found.")
            return

        update_count = 0

        for archivo in os.listdir(images_folder):
            nombre_archivo = os.path.splitext(archivo)[0]  # quita la extensión
            movie_title = nombre_archivo[2:]  # quita el "m_"
            ruta_completa = f'movie/images/{nombre_archivo}.png'
            # Busca película por título exacto
            movie = Movie.objects.filter(title=movie_title).first()
            if movie:
                movie.image = ruta_completa
                movie.save()
                update_count += 1
                self.stdout.write(f"Imagen actualizada para: {movie_title}")
            else:
                self.stderr.write(f"Película no encontrada: {movie_title}")

        self.stdout.write(self.style.SUCCESS(f"\n Imágenes actualizadas: {update_count}"))
