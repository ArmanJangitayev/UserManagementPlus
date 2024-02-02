from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def compress_image(uploaded_image):
    image = Image.open(uploaded_image)
    image = image.convert('RGB')

    output_io_stream = BytesIO()
    image_temproary_resized = image.resize((1020, 573))
    image_temproary_resized.save(output_io_stream, format='JPEG', quality=60)
    output_io_stream.seek(0)
    uploaded_image = InMemoryUploadedFile(output_io_stream, 'ImageField', "%s.jpg" % uploaded_image.name.split('.')[0],
                                         'image/jpeg', sys.getsizeof(output_io_stream), None)
    return uploaded_image
