from PassPage import PassPage
from pass_blr import BlrPass
from pass_ukr import UkrPass
from Pass import Pass
from C_implementation import get_pass_corners
from Segment import Segment
from PointVector import Point
from C_implementation import get_pass_corners
from Abstract_Documents.AbstractDocument import AbstractDocument
from Abstract_Documents.JsonWorker import JsonWorker
from BucketWorker import bucketWorker
from PIL import Image
import requests
import json
import urllib
import os
import ctypes
import numpy
import math
import cv2 as cv

# js = JsonWorker(["first", "second"], "Data/jopa.json", new_path=True)
# fields = {"Devil": "may", "Cry": True}
# js.replace_current_directory(fields)
# js.working_directory = fields
# js.save_json()
# bw = bucketWorker("ltd-krp")
# bw.download_file("images/jopa.png", "documents/847723c20d040ad90c3e917a3a6aeec9.png")
# passport = UkrPass("images/pass.pdf", "images/", deletion_key=False, analysis_key=True, is_debugging=True)
# print(passport.pass_info)
# passport.create_file()



passport = AbstractDocument("images/pass.pdf", "images/", ["passport", "ukr", "0"], "Data/work_data.json", deletion_key=
                            False, analysis_key=False, is_debugging=True)
print(passport.get_text())

# img = Image.open("./images/jopa.jpg")
# img.thumbnail((128,128), Image.ANTIALIAS)
# img.save("./images/jopa2.jpg", "JPEG")
