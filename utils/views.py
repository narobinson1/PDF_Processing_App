from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import os
import re
from pypdf import PdfReader, PdfWriter, Transformation

def theme_creator(theme_str: str) -> dict:
    """Takes either 'true' or 'false' - true and false booleans from 'checked' attribute of theme checkbox, javascript boolean is stringified when passed as value of form input
    
    Returns: dict with theming classes
    """
    theme = {}
    if theme_str == 'true':
        theme['text'] = 'dark-text'
        theme['header'] = 'dark-header'
        theme['component'] = 'dark-component'
        theme['main_section'] = 'dark-main-section'
        theme['upload_section'] = 'dark-upload-section'
        theme['dropzone_section'] = 'dark-dropzone-section'
        theme['dropzone_text'] = 'dark-dropzone-text'
        theme['checked'] = 'checked'
    elif theme_str == 'false':
        theme['text'] = 'light-text'
        theme['header'] = 'light-header'
        theme['component'] = 'light-component'
        theme['main_section'] = 'light-main-section'
        theme['upload_section'] = 'light-upload-section'
        theme['dropzone_section'] = 'light-dropzone-section'
        theme['dropzone_text'] = 'light-dropzone-text'
        theme['checked'] = ''
    
    return theme
        
def index(request):
#    theme_bool = request.POST['theme-input']
    message = {}
    theme = theme_creator('true')
    message['welcome'] = "welcome"
    message['theme'] = theme
    
    return render(request, "utils/interface.html", message)

def returnText(request):
    files_dictionary = request.FILES
    file_wrapper = files_dictionary['text']
    message = {}
    if file_wrapper.multiple_chunks:
        raw_file = file_wrapper.file
        reader = PdfReader(raw_file)
        page = reader.pages[0]
        text = page.extract_text()
        message['text'] = text
#        text = []
#        for chunk in file:
#            text.append(chunk)
    else:
        text = file.size
        message['text'] = text
        
    theme_bool = request.POST['theme-input']
    theme = theme_creator(theme_bool)
    message['theme'] = theme
    return render(request, "utils/interface.html", message)
    
def returnMetadata(request):
    files_dictionary = request.FILES
    message = {}
    if 'author' in files_dictionary.keys():
        file_wrapper = files_dictionary['author']
        raw_file = file_wrapper.file
        reader = PdfReader(raw_file)
        meta = reader.metadata
        if hasattr(meta, 'author') and meta.author is not None:
            message['author'] = meta.author
        else:
            message['author'] = "No author"
    if 'date' in files_dictionary.keys():
        file_wrapper = files_dictionary['date']
        raw_file = file_wrapper.file
        reader = PdfReader(raw_file)
        meta = reader.metadata
        if hasattr(meta, 'creation_date') and meta.author is not None:
            message['date'] = meta.creation_date
        else:
            message['date'] = "No date"
    if 'device' in files_dictionary.keys():
        file_wrapper = files_dictionary['device']
        raw_file = file_wrapper.file
        reader = PdfReader(raw_file)
        meta = reader.metadata
        if hasattr(meta, 'creator') and meta.creator is not None:
            message['device'] = meta.creator
        else:
            message['device'] = "No device"

    theme_bool = request.POST['theme-input']
    theme = theme_creator(theme_bool)
        
    message['theme'] = theme
    return render(request, "utils/interface.html", message)

def returnContent(request):
    files_dictionary = request.FILES
    message = {}
    if 'text' in files_dictionary.keys():
        file_wrapper = files_dictionary['text']
        raw_file = file_wrapper.file
        reader = PdfReader(raw_file)
        page = reader.pages[0]
        text = page.extract_text()
        if text:
            message['text'] = text
        else:
            message['text'] = "No text"
    if 'images' in files_dictionary.keys():
        file_wrapper = files_dictionary['images']
        raw_file = file_wrapper.file
        reader = PdfReader(raw_file)
        page = reader.pages[0]
        image_count = len(page.images)
        if image_count > 0:
            message['images'] = image_count
        else:
            message['images'] = "No images"
    if 'attachments' in files_dictionary.keys():
        file_wrapper = files_dictionary['attachments']
        raw_file = file_wrapper.file
        reader = PdfReader(raw_file)
        attachments = reader.attachments
        if len(attachments) > 0:
            message['attachments'] = attachments
        else:
            message['attachments'] = "No attachments"
            
    theme_bool = request.POST['theme-input']
    theme = theme_creator(theme_bool)
    message['theme'] = theme
    return render(request, "utils/interface.html", message)
    
def returnTransformation(request):
    files_dictionary = request.FILES
    if 'merged' in files_dictionary.keys():
        files_list = files_dictionary.getlist('merged')
        file_tuples = []
        for file in files_list:
            rgx = re.compile('[\d]+')
            order = rgx.match(file.name)
            if not order:
                mergedMessage = "Invalid filename formatting"
                response = render(request, "utils/interface.html", {"merged": mergedMessage})
                return response
            file_tuple = (order, file)
            file_tuples.append(file_tuple)
        merger = PdfWriter()
        for file_tuple in file_tuples:
            merger.append(file_tuple[1])
        with open("merged.pdf", "wb") as f:
            merger.write(f)
        with open("merged.pdf", "rb") as f:
            response = HttpResponse(
                f.read(),
                headers={
                    "Content-Type": "application/pdf",
                    "Content-Disposition": 'attachment; filename="merged.pdf"'
                }
            )
        os.remove("merged.pdf")
    if 'rotated' in files_dictionary.keys():
        rotation_degree = int(request.POST['rotation_degree'])
        files_dictionary = request.FILES
        files_list = files_dictionary.getlist('rotated')
        writer = PdfWriter()
        for file in files_list:
            reader = PdfReader(file)
            for page in reader.pages:
                page.rotate(rotation_degree)
                writer.add_page(page)
        with open("rotated.pdf", "wb") as f:
            writer.write(f)
        with open("rotated.pdf", "rb") as f:
            response = HttpResponse(
                f.read(),
                headers={
                    "Content-Type": "application/pdf",
                    "Content-Disposition": 'attachment; filename="rotated.pdf"'
                }
            )
        os.remove("rotated.pdf")
    
    return response
    
def returnSecurity(request):
    files_dictionary = request.FILES
    if 'AES-encrypt' in files_dictionary.keys():
        encryption_type = request.POST['AES-algorithm']
        password = request.POST['password-input']
        files_dictionary = request.FILES
        file_wrapper = files_dictionary['AES-encrypt']
        raw_file = file_wrapper.file
        reader = PdfReader(raw_file)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password, algorithm=encryption_type)
        with open("encrypted.pdf", "wb") as f:
            writer.write(f)
        with open("encrypted.pdf", "rb") as f:
            response = HttpResponse(
                f.read(),
                headers={
                    "Content-Type": "application/pdf",
                    "Content-Disposition": 'attachment; filename="encrypted.pdf"'
                }
            )
    if 'AES-decrypt' in files_dictionary.keys():
        encryption_algorithm = request.POST['AES-algorithm']
        password = request.POST['password-input']
        files_dictionary = request.FILES
        file_wrapper = files_dictionary['AES-decrypt']
        raw_file = file_wrapper.file
        reader = PdfReader(raw_file)
        writer = PdfWriter()
        if reader.is_encrypted:
            reader.decrypt(password)
        for page in reader.pages:
            writer.add_page(page)
        with open("decrypted.pdf", "wb") as f:
            writer.write(f)
        with open("decrypted.pdf", "rb") as f:
            response = HttpResponse(
                f.read(),
                headers={
                    "Content-Type": "application/pdf",
                    "Content-Disposition": 'attachment; filename="decrypted.pdf"'
                }
            )
    
    return response
    

#def returnStamped(request):
#    files_dictionary = request.FILES
#    files_list = files_dictionary.getlist('stamped')
#    file_tuples = []
#    stamp_page = []
#    for file in file_list:
#        for page in file.pages:
#            rgx = re.compile('[\d]')
#            base = rgx.match(file.name)
#            if not base:
#                mergedMessage = "Invalid filename formatting"
#                response = render(request, "utils/interface.html", {"mergedMessage": mergedMessage})
#                return response
#            file_tuple = (order, file)
#            file_tuples.append(file_tuple)
#    sorted_files = sorted(file_tuples, key=lambda x:x[0])
#    pages_lists = [list(x[1].pages) for x in file_tuples]
#    pages_watermarked = [
#    pages_zip = list(zip(pages_lists[0], pages_lists[1]))
#    transformation = Transformation().rotate(rotation_degree).translate(tx=horizontal_translation, ty=vertical_translation)
#    base_merged = [x[0].merge_page(x[1].add_transformation(transformation)) for x in pages_zip]
#    writer = PdfWriter()
#    for page in base_merged:
#        writer.add_page(page[0])
#
#
#    with open("plainmerge.pdf", "wb") as f:
#        writer.write(f)
#    with open("plainmerge.pdf", "rb") as f:
#        response = HttpResponse(
#            f.read(),
#            headers={
#                "Content-Type": "application/pdf",
#                "Content-Disposition": 'attachment; filename="plainmerge.pdf"'
#            }
#        )
#    os.remove("plainmerge.pdf")
#    return response
