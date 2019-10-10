from PIL import Image
import math
import cv2 as cv


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

def fill_around(image, diag, ux, uy):
    canvas = Image.new("RGB", (diag, diag), "white")
    canvas.paste(image, (diag // 2 - uy, diag // 2 - ux))
    return canvas
    # canvas.save("pass_on_centre.jpg")


def get_center(coords):
    ux = sum(coords[1:4:2]) // 2
    uy = sum(coords[0:3:2]) // 2
    print(ux, ' ', uy)
    ux = sum(coords[5:8:2]) // 2
    uy = sum(coords[4:7:2]) // 2
    print(ux, ' ', uy)
    ux = sum(coords[1::2]) // 4
    uy = sum(coords[0::2]) // 4
    print(ux, ' ', uy)
    return ux, uy


def find_rotate_angle(x0, y0, x1, y1, x2, y2):
    if (((x0 - x1) ** 2 + (y0 - y1) ** 2) > ((x0 - x2) ** 2 + (y0 - y2) ** 2)):
        return -(math.atan2(x0 - x2, y0 - y2))
    else:
        return -(math.atan2(x0 - x1, y0 - y1))


def ort_rotate(rotate_angle, image):
    rotate_angle = rotate_angle * 180 / math.pi
    image = image.rotate(rotate_angle)
    return image


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin[0], origin[1]
    px, py = point[0], point[1]

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return [qx, qy]


def new_points(coords, diag, ux, uy):
    coords2 = coords[:]
    for i in range(4):
        coords2[i * 2] += diag // 2 - uy
        coords2[i * 2 + 1] += diag // 2 - ux
    return coords2


def rotated_points(coords2, diag, angle):
    coords3 = coords2[:]
    for i in range(4):
        q = rotate([diag // 2, diag // 2], [coords3[i * 2], coords3[i * 2 + 1]], angle)
        coords3[i * 2] = int(q[0])
        coords3[i * 2 + 1] = int(q[1])
    return coords3


imageName = './images/out15'
img = Image.open(imageName + '.jpg').convert('L')
img.save(imageName + '_grayscale.jpg')
img = cv.imread(imageName + '_grayscale.jpg',0)
edges = cv.Canny(img,7, 14)
cv.imwrite(imageName + "_edges.jpg", edges)
cv = Image.open(imageName + "_edges.jpg")

with open("C_directory/image.txt", "w") as f:
    a = edges.tolist()
    f.write(str(len(a)) + ' ' + str(len(a[0])))
    for i in a:
        for j in i:
            f.write(' ' + str(j))



##
## There must be cpp code for finding the passport angle points.
##
##


coords = []
with open("C_directory/coordinates_4p.txt", "r+") as file:
    arr = file.readline().split(' ')
    coords = [int(x) for x in (arr)]
print(coords[:-4])

ux, uy = get_center(coords)

diag = int(math.sqrt((coords[0] - coords[2])**2 + (coords[1] - coords[3])**2))
angle = find_rotate_angle(coords[0], coords[1], coords[2], coords[3], coords[4], coords[5])
print(angle)
image = ort_rotate(angle,fill_around(Image.open(imageName + ".jpg"), diag,
            ux, uy))

image.save(imageName + "_rotated.jpg")

print(coords)
coords2 = new_points(coords, diag, ux, uy)
print(coords)
print(coords2)

coords3 = rotated_points(coords2, diag, angle)
print(coords2)
print(coords3)

x = coords3[0::2]
y = coords3[1::2]
print(x, y)

x.sort()
y.sort()
print(x, y)

frame = [(x[0] + x[1])//2, (y[0] + y[1])//2, (x[2] + x[3])//2, (y[2] + y[3])//2]
print(frame)

ready_image = Image.open(imageName + '_rotated.jpg')
prepare(ready_image, imageName + "_ready.jpg", frame)

