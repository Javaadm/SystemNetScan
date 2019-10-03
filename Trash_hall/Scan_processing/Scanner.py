from pdf2image import convert_from_path


pages = convert_from_path('pass.pdf', 500)
for n in list(range(len(pages))):
    pages[n].save('out' + str(n) + '.jpg', 'JPEG')
