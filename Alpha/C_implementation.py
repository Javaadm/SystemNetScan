import numpy as np
import ctypes

def get_pass_corners(edged_image):
    lib = ctypes.cdll.LoadLibrary("./new_C_directory/get_pass_corners.so")
    fun = lib.mainF
    fun.restype = None
    fun.argtypes = [ctypes.c_int, ctypes.c_int,
                    np.ctypeslib.ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
                    np.ctypeslib.ndpointer(ctypes.c_int, flags="C_CONTIGUOUS")]
    height = np.shape(edged_image)[0]
    width = np.shape(edged_image)[1]
    edged_image = np.array(edged_image, np.int32)
    edged_image = edged_image.flatten()
    edged_image = np.ascontiguousarray(edged_image)
    # print(type(edged_image))
    result = np.array(np.empty(8), np.int32)
    result = np.ascontiguousarray(result)

    # print(height, width, edged_image[2])
    fun(height, width, edged_image, result)
    new_result = [x for x in result]
    print("C okay")
    return new_result
    # print(edged_image[1])
