from PIL import Image
from matplotlib import image
from matplotlib import pyplot


def a():
    # load the image
    image = Image.open('f1.jpg')
    # summarize some details about the image
    print(image.format)
    print(image.mode)
    print(image.size)
    # show the image
    image.show()


def b():
    # load image as pixel array
    data = image.imread('f1.jpg')
    # summarize shape of the pixel array
    print(data.dtype)
    print(data.shape)

    # display the array of pixels as an image
    pyplot.imshow(data)
    pyplot.show()

def c():
    # load the image
    image = Image.open('f1.jpg')
    # report the size of the image
    print(image.size)
    # create a thumbnail and preserve aspect ratio
    image.thumbnail((100, 100))
    # report the size of the thumbnail
    print(image.size)

if __name__ == "__main__":
    a()