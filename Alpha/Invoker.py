from Alpha.PassPage import PassPage
from Alpha.pass_blr import BlrPass
from Alpha.pass_ukr import UkrPass
from Alpha.Pass import Pass
from PIL import Image
import requests
import json
import urllib
import os
import ctypes
from Alpha.C_implementation import get_pass_corners
from Alpha.Segment import Segment
from Alpha.PointVector import Point
from Alpha.C_implementation import get_pass_corners
from PIL import Image
import numpy
import math
import os
import cv2 as cv

import numpy

passport = UkrPass("images/pass.pdf", "images/", deletion_key=False, analysis_key=True, is_debugging=True)
print(passport.pass_info)
# passport.create_file()

# for i in range(10):
#     print(i, " started")
#     arr = numpy.ones((5000- i * 50, 4000 + i * 50), numpy.int32)
#     print(get_pass_corners(arr))
