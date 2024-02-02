from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .helpers import compress_image


# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

def handle_uploaded_file(f, filename):
    if filename.endswith('.jpg'):
        print('compressing image')
        f = compress_image(f)
    with open("media/files/" + filename, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"], form.cleaned_data['title'])
            return redirect('home_page')

    else:
        form = UploadFileForm()
    return render(request, "files.html", {"form": form})

# from django.core.exceptions import ValidationError
# from django.core.files.images import get_image_dimensions
#
#
# def validate_image(file):
#    # Проверка, является ли файл изображением
#    try:
#        width, height = get_image_dimensions(file)
#        if width < 100 or height < 100:
#            raise ValidationError("Image dimensions are too small (at least 100x100 pixels required).")
#    except Exception as e:
#        raise ValidationError("Invalid image file.")
