#!/usr/bin/env python
# coding: utf-8

# In[221]:


from PIL import Image, ImageDraw, ImageFont
import pytesseract
from tesserocr import PyTessBaseAPI
from PIL import Image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


# In[222]:


def prepare(image, name, crop=None, brightness_border = 180, scale=0):
    if(crop!=None):
        image = image.crop(crop)
        image.save(name)
    bw_name = name[0:-4] + '_bw.jpg'
    column = image
    gray = column.convert('L')
    blackwhite = gray.point(lambda x: 0 if x < brightness_border else 255, '1')
    newimg1 = Image.new('RGB', size=[x*(scale*2 + 1) for x in blackwhite.size], color='white')
    newimg1.paste(blackwhite, [x*scale for x in blackwhite.size])
    newimg1.save(bw_name)
    return blackwhite

def show(image, crop, color="green", width=3):
    d = ImageDraw.Draw(image)
    d.rectangle(crop, outline=color, width=width)
    image.show()


# In[223]:


def birth_date(brightness_border=180, scale=1):
    base = Image.open('final_pass15.jpg').convert('RGB')

    birth_date_crop=[x//2 for x in base.size]*2;
    #print(birth_date_crop)
    birth_date_crop[0]+=-1120
    birth_date_crop[1]+=775
    birth_date_crop[2]+=320
    birth_date_crop[3]+=895
    #show(base, birth_date_crop)
    prepare(base, "birth_date.jpg", birth_date_crop, brightness_border=brightness_border, scale=scale)
    return "birth_date_bw.jpg"


# In[224]:


def birth_place(brightness_border=180, scale=1):
    base = Image.open('final_pass15.jpg').convert('RGB')

    birth_place_crop=[x//2 for x in base.size]*2;
    #print(birth_place_crop)
    birth_place_crop[0]+=-30
    birth_place_crop[1]+=860
    birth_place_crop[2]+=1050
    birth_place_crop[3]+=1060
    #print(birth_place_crop)
    #show(base, birth_place_crop)
    prepare(base, "birth_place.jpg", birth_place_crop, brightness_border=brightness_border, scale=scale)
    return "birth_place_bw.jpg"


# In[225]:


def personal_number(brightness_border=180, scale=1):
    base = Image.open('final_pass15.jpg').convert('RGB')

    personaln_crop=[x//2 for x in base.size]*2;
    #print(personaln_crop)
    personaln_crop[0]+=370
    personaln_crop[1]+=760
    personaln_crop[2]+=1120
    personaln_crop[3]+=860
    #print(personaln_crop)
    #show(base, personaln_crop)
    prepare(base, "personal_number.jpg", personaln_crop, brightness_border=brightness_border, scale=scale)
    return "personal_number_bw.jpg"


# In[226]:


def issuing_date(brightness_border=180, scale=1):
    base = Image.open('final_pass15.jpg').convert('RGB')

    personaln_crop=[x//2 for x in base.size]*2;
    #print(personaln_crop)
    personaln_crop[0]+=-1010
    personaln_crop[1]+=1330
    personaln_crop[2]+=-470
    personaln_crop[3]+=1400   
    #print(personaln_crop)
    #show(base, personaln_crop)
    prepare(base, "issuing_date.jpg", personaln_crop, brightness_border=brightness_border, scale=scale)
    return "issuing_date_bw.jpg"


# In[227]:


def expiration_date(brightness_border=180, scale=1):
    base = Image.open('final_pass15.jpg').convert('RGB')

    personaln_crop=[x//2 for x in base.size]*2;
    #print(personaln_crop)
    personaln_crop[0]+=350
    personaln_crop[1]+=1330
    personaln_crop[2]+=1150
    personaln_crop[3]+=1400  
    #print(personaln_crop)
    #show(base, personaln_crop)
    prepare(base, "expiration_date.jpg", personaln_crop, brightness_border=brightness_border, scale=scale)
    return "expiration_date_bw.jpg"


# In[215]:


base = Image.open('final_pass15.jpg').convert('RGB')
print([x//2 for x in base.size]*2)


# In[216]:

def test():
    image = Image.open(birth_date())
    birth_date = pytesseract.image_to_string(image, lang='rus')
    image = Image.open(issuing_date())
    issuing_date = pytesseract.image_to_string(image, lang='rus')
    image = Image.open(expiration_date())
    expiration_date = pytesseract.image_to_string(image, lang='rus')
    image = Image.open(birth_place())
    birth_place = pytesseract.image_to_string(image, lang='rus')
    print("birth date:", birth_date)
    print("birth_place:", birth_place)
    print("issuing_date:", issuing_date)
    print("expiration_date:", expiration_date)


# In[228]:


for brb in list(range(160, 200, 5)):
    print("brightness_border is ", brb)
    image_name = expiration_date(brightness_border=brb)
    img = Image.open(image_name)
    plt_img=mpimg.imread(image_name)
    imgplot = plt.imshow(plt_img)
    best2 = "21 05 1977"
    best3 = "11 09 2002"
    best4 = "21 05 2022"
    best = best4
    print("rel:", best)
    plt.show()
    img.load()
    with PyTessBaseAPI() as api:
        api.SetImageFile(image_name)
        text = api.GetUTF8Text()[:-1]
        print("bad:", text, "  ", text == best)
    text1 = pytesseract.image_to_string(img, lang='eng')
    print("eng:", text1, "  ", text1 == best)
    text2 = pytesseract.image_to_string(img, lang='rus')
    print("rus:", text2, "  ", text2 == best)
    text3 = pytesseract.image_to_string(img, lang='bel')
    print("bel:", text3, "  ", text3 == best)
    text4 = pytesseract.image_to_string(img, lang='osd')
    print("osd:", text4, "  ", text4 == best)
    
    


# In[ ]:




