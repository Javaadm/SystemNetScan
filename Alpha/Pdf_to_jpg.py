from pdf2image import convert_from_path


def pdf_to_images(path_to_pdf, path_for_images=""):
    pages = convert_from_path(path_to_pdf, 500)
    for n in list(range(len(pages))):
        pages[n].save(path_for_images + 'out' + str(n) + '.jpg', 'JPEG')
