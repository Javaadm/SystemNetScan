from Alpha.Pass import PassPage
from Alpha.pass_blr import BlrPass
from PIL import Image
import os

passport = BlrPass("images/pass.pdf")

for n in range(passport.pages):
    passport.pages[n].image.save("images/out" + str(n) + ".jpg")


