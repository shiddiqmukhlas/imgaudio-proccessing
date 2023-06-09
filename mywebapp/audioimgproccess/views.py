from django.shortcuts import render
from PIL import Image
from pydub import AudioSegment
import tempfile
import os
from django.http import HttpResponse, FileResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

def home(request):
    return render(request, 'home.html')

def resize_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        image = Image.open(image_file)

        # Mendapatkan nilai lebar dan tinggi yang diinput oleh pengguna
        width = request.POST.get('width', 500)
        height = request.POST.get('height', 500)

        # Mengubah nilai lebar dan tinggi menjadi integer
        try:
            width = int(width)
            height = int(height)
        except ValueError:
            width = 500
            height = 500

        resized_image = image.resize((width, height))

        # Buat file sementara dengan menggunakan modul tempfile.NamedTemporaryFile
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_path = temp_file.name
            resized_image.save(temp_path)

            # Buat objek FileResponse untuk mengirim file sebagai respons
            file_response = FileResponse(open(temp_path, 'rb'), as_attachment=True, filename='resized_image.jpg')

        return file_response

    return render(request, 'resize_image.html')


def compress_audio(request):
    if request.method == 'POST' and request.FILES['audio']:
        audio_file = request.FILES['audio']

        # Membuat direktori tempat file audio sementara akan disimpan
        temp_dir = tempfile.mkdtemp()

        # Menyimpan file audio sementara dalam direktori temp
        temp_path = os.path.join(temp_dir, audio_file.name)
        with open(temp_path, 'wb') as file:
            for chunk in audio_file.chunks():
                file.write(chunk)

        # Melakukan kompresi audio
        compressed_audio_path = os.path.join(temp_dir, 'compressed_audio.mp3')
        audio = AudioSegment.from_file(temp_path)
        audio.export(compressed_audio_path, format='mp3', bitrate='64k')

        # Menghapus file audio sementara setelah kompresi
        os.remove(temp_path)

        # Mengirimkan file audio yang telah dicompress sebagai respons langsung
        return FileResponse(open(compressed_audio_path, 'rb'), as_attachment=True, filename='compressed_audio.mp3')

    return render(request, 'compress_audio.html')
