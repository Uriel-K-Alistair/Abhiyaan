from PIL import Image
from numpy import asarray, array, sqrt
from matplotlib import pyplot

imagenames = ["4Junc.png", "Curve.png", "scenario.png", "Straight.png", "TJunc.png"]
# These are the files we need to work with. I will iterate through these in the following for loop.

for name in imagenames:

    # Opening the image
    img = Image.open(name)

    # Finding the center. This is where I assume the car exists. I haven't bothered with the extra distance.
    # Considering the bonus distance is just a matter of redefining the center so the code is still valid.
    centerx = img.size[0] // 2
    centery = img.size[1] // 2

    # This is the list of angles I will be plotting
    X = list(range(360))
    # This will contain the distances that we need.
    distances = []

    for angle in range(360):
        # I'm taking the original image and simply rotating by some angle so that
        # I can just look vertically above the center to find the closest black pixel.
        rotated_img = img.rotate(angle)
        megalist = asarray(rotated_img)

        # Here, I start at the center and move upward, looking for non-white pixels
        # which have all 4 RGB and aplha values as 255.

        for i in range(centery, -1, -1):
            if sum(megalist[i][centerx]) != 255 * 4:
                distances.append(centery - i)
                break
        else:
            distances.append(centery)
            # If it's just an open end, I assume the distance to be till the edge of the image.

    # Now I am normalising the distances:

    mean = sum(distances) / 360
    ssd = 0
    for i in distances:
        ssd += (i - mean) ** 2

    s = sqrt(ssd / 360)
    for i in range(360):
        distances[i] = (distances[i] - mean) / s

    # And Finally I plot the required graph.

    pyplot.scatter(X, distances, c="green")
    pyplot.xlabel("Angle")
    pyplot.ylabel("Normalised Distance")
    pyplot.title(name)
    pyplot.show()
