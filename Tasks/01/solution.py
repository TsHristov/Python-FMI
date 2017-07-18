from collections import defaultdict


def rotate_left(image):
    return list(zip(*image))[::-1]


def rotate_right(image):
    return list(zip(*image[::-1]))


def invert(image):
    return manipulate(image, invert=True)


def lighten(image, real_number):
    return manipulate(image, real_number, lighten=True)


def darken(image, real_number):
    return manipulate(image, real_number, darken=True)


def manipulate(image, real_number=None, invert=False, darken=False, lighten=False):
    new_image = []
    for pixels in image:
        modified_pixels = []
        for pixel in pixels:
            if darken:
                modified_pixels.append(tuple(map(lambda x: int(x - real_number * x), pixel)))
            elif lighten:
                modified_pixels.append(tuple(map(lambda x: int(x + real_number * (255-x)), pixel)))
            elif invert:
                modified_pixels.append(tuple(map(lambda x: 255-x, pixel)))
        new_image.append(modified_pixels)
    return new_image


def create_histogram(image):
    histogram = {
        'red':   defaultdict(int),
        'green': defaultdict(int),
        'blue':  defaultdict(int),
    }
    for pixels in image:
        for red, green, blue in pixels:
            histogram['red'][red]     += 1
            histogram['green'][green] += 1
            histogram['blue'][blue]   += 1
    return histogram
