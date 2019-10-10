#!/usr/bin/env python
# coding: utf-8


from PIL import Image, ImageDraw, ImageFont
import pytesseract
from PIL import Image
import json


def prepare(open_fname, name, crop=None, brightness_border = 180, scale=0):
    image = Image.open(open_fname).convert('RGB')
    if crop is not None:
        image = image.crop(crop)
        image.save(name)

    column = image
    gray = column.convert('L')
    blackwhite = gray.point(lambda x: 0 if x < brightness_border else 255, '1')
    newimg1 = Image.new('RGB', size=[x*(scale*2 + 1) for x in blackwhite.size], color='white')
    newimg1.paste(blackwhite, [x*scale for x in blackwhite.size])
    newimg1.save(name)


def show(image, crop, color="green", width=3):
    d = ImageDraw.Draw(image)
    d.rectangle(crop, outline=color, width=width)
    image.show()


def birth_date(open_fname, write_fname, brightness_border=180, scale=1):
    base = Image.open(open_fname).convert('RGB')
    image_crop=[x//2 for x in base.size]*2;
    image_crop[0]+=-1120
    image_crop[1]+=775
    image_crop[2]+=320
    image_crop[3]+=895
    #show(base, image_crop)
    prepare(open_fname, write_fname, image_crop, brightness_border=brightness_border, scale=scale)


def birth_place(open_fname, write_fname, brightness_border=180, scale=1):
    base = Image.open(open_fname).convert('RGB')
    image_crop=[x//2 for x in base.size]*2;
    #print(image_crop)
    image_crop[0]+=-30
    image_crop[1]+=860
    image_crop[2]+=1050
    image_crop[3]+=1060
    #print(image_crop)
    #show(base, image_crop)
    prepare(open_fname, write_fname, image_crop, brightness_border=brightness_border, scale=scale)


def personal_number(open_fname, write_fname, brightness_border=180, scale=1):
    base = Image.open(open_fname).convert('RGB')
    image_crop=[x//2 for x in base.size]*2;
    image_crop[0]+=370
    image_crop[1]+=760
    image_crop[2]+=1120
    image_crop[3]+=860
    prepare(open_fname, write_fname, image_crop, brightness_border=brightness_border, scale=scale)


def issuing_date(open_fname, write_fname, brightness_border=180, scale=1):
    base = Image.open(open_fname).convert('RGB')
    image_crop=[x//2 for x in base.size]*2;
    image_crop[0]+=-1010
    image_crop[1]+=1330
    image_crop[2]+=-470
    image_crop[3]+=1400
    prepare(open_fname, write_fname, image_crop, brightness_border=brightness_border, scale=scale)


def expiration_date(open_fname, write_fname, brightness_border=180, scale=1):
    base = Image.open(open_fname).convert('RGB')
    image_crop=[x//2 for x in base.size]*2;
    image_crop[0]+=350
    image_crop[1]+=1330
    image_crop[2]+=1150
    image_crop[3]+=1400
    prepare(open_fname, write_fname, image_crop, brightness_border=brightness_border, scale=scale)


def test(open_fname, main_path = ""):
    birth_date_path = main_path + "birth_date.jpg"
    birth_place_path = main_path + "birth_place.jpg"
    personal_number_path = main_path + "personal_number.jpg"
    issuing_date_path = main_path + "issuing_date.jpg"
    expiration_date_path = main_path + "expiration_date.jpg"
    birth_date(open_fname, birth_date_path)
    birth_place(open_fname, birth_place_path)
    personal_number(open_fname, personal_number_path)
    issuing_date(open_fname, issuing_date_path)
    expiration_date(open_fname, expiration_date_path)
    birth_date_value = pytesseract.image_to_string(Image.open(birth_date_path), lang='rus')
    birth_place_value = pytesseract.image_to_string(Image.open(birth_place_path), lang='rus')
    personal_number_value = pytesseract.image_to_string(Image.open(personal_number_path), lang='eng')
    issuing_date_value = pytesseract.image_to_string(Image.open(issuing_date_path), lang='rus')
    expiration_date_value = pytesseract.image_to_string(Image.open(expiration_date_path), lang='rus')


    ret = {"birth date": birth_date_value, "birth_place": birth_place_value, "personal_number": personal_number_value,
           "issuing_date": issuing_date_value, "expiration_date": expiration_date_value}
    return ret

def passport_number(open_fname, write_name, brightness_border=180, scale=1):
    base = Image.open(open_fname).convert('RGB')
    bs = [x for x in base.size]
    image_crop = bs*2
    image_crop[0] = (int)(bs[0]*0.7114)
    image_crop[1] = (int)(bs[1]*0.5647)
    image_crop[2] = (int)(bs[0]*0.9187)
    image_crop[3] = (int)(bs[1]*0.5906)
    prepare(open_fname, write_name, image_crop, brightness_border=brightness_border, scale=scale)


def citizenship(open_fname, write_name, brightness_border=180, scale=1):
    base = Image.open(open_fname).convert('RGB')
    bs = [x for x in base.size]
    image_crop = bs*2
    image_crop[0] = (int)(bs[0]*0.3170)
    image_crop[1] = (int)(bs[1]*0.669)
    image_crop[2] = (int)(bs[0]*0.6341)
    image_crop[3] = (int)(bs[1]*0.6886)
    prepare(open_fname, write_name, image_crop, brightness_border=brightness_border, scale=scale)


def birth_place2(open_fname, write_name, brightness_border=180, scale=1):
    base = Image.open(open_fname).convert('RGB')
    bs = [x for x in base.size]
    image_crop = bs*2
    image_crop[0] = (int)(bs[0] * 0.5041)
    image_crop[1] = (int)(bs[1] * 0.7404)
    image_crop[2] = (int)(bs[0] * 0.9146)
    image_crop[3] = (int)(bs[1] * 0.7609)
    prepare(open_fname, write_name, image_crop, brightness_border=brightness_border, scale=scale)


def test2(open_fname, main_path=""):
    passport_number_path = main_path + "passport_number.jpg"
    citizenship_path = main_path + "citizenship.jpg"
    birth_place2_path = main_path + "birth_place2.jpg"
    passport_number(open_fname, passport_number_path)
    citizenship(open_fname, citizenship_path)
    birth_place2(open_fname, birth_place2_path)
    passport_number_value = pytesseract.image_to_string(Image.open(passport_number_path), lang='eng')
    citizenship_value = pytesseract.image_to_string(Image.open(citizenship_path), lang='eng')
    birth_place2_value = pytesseract.image_to_string(Image.open(birth_place2_path), lang='eng')
    ret = {"passport_number": passport_number_value, "citizenship": citizenship_value,
           "birth_place2": birth_place2_value}
    return ret


def json_maker(prefix):
    open_fname = prefix + "final_pass15.jpg"
    path_to_json = prefix + "user_data.json"
    with open(path_to_json) as user_json:
        data = json.load(user_json)

    info_fields = test(open_fname, prefix)
    print(info_fields)
    for key in list(info_fields.keys()):
        data[key] = info_fields[key]

    open_fname2 = prefix + "final_pass16.jpg"
    info_fields2 = test2(open_fname2, prefix)
    for key in list(info_fields2.keys()):
        data[key] = info_fields2[key]

    with open(path_to_json, "w+") as user_json:
        json.dump(data, user_json)


prefix = "./images/"


openf = prefix + "full_fledged_pass.jpg"
print(test2(openf, prefix))

openf = prefix + "final_pass16.jpg"
print(test2(openf, prefix))
