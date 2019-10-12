from Alpha.PassPage import PassPage
from Alpha.pass_blr import BlrPass
from Alpha.Pass import Pass
from PIL import Image
import os

passport = BlrPass("images/pass.pdf", "images/")

for n in range(len(passport.pages)):
    passport.pages[n].get_image().save("images/invoker_out" + str(n) + ".jpg")



