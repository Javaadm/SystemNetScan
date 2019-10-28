from Alpha.PassPage import PassPage
from Alpha.pass_blr import BlrPass
from Alpha.pass_ukr import UkrPass
from Alpha.Pass import Pass
from Alpha.C_implementation import get_pass_corners
from Alpha.Segment import Segment
from Alpha.PointVector import Point
from Alpha.C_implementation import get_pass_corners
from Alpha.Abstract_Documents.JsonWorker import JsonWorker
from PIL import Image
import requests
import json
import urllib
import os
import ctypes
import numpy
import math
import cv2 as cv


# passport = UkrPass("images/pass.pdf", "images/", deletion_key=False, analysis_key=True, is_debugging=True)
# print(passport.pass_info)
# passport.create_file()


