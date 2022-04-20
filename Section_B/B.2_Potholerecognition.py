import cv2
import numpy as np


# This will be used to resize our frame if the need arises.
def rescale(image, scale):
    w = int(image.shape[1] * scale)
    h = int(image.shape[0] * scale)

    return cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)


# Ok I'll be frank here. I just had to submit something, so i did everything I possibly could in a last ditch attempt to detect something.
# I greyscaled the image, put some threshholds, washed out noise, drew contours, and then dumped a lot of the contours on some criteria.
# I dumped the BIG contours coz they were roads, the tiny ones because they were noise.
# I looked at the tiny sliver of pixels right above the detected region and checked if they were having some colouration,
# to filter out the cylinders, as opposed to the road which would be blackish for the potholes
# The code is by no means perfect, and It's probably the best strategy to just train a classifier for anything better.

def runthecode(name):
    # Getting the video feed, and initiating our classifier.
    videofeed = cv2.VideoCapture(name + "_test_pothole.mp4")
    # pothole_data = cv2.CascadeClassifier('pothole_data.xml')

    while True:

        # Getting the video's frames and breaking out once we run out of frames.
        isTrue, frame_og = videofeed.read()
        if not isTrue:
            break

        frame = cv2.cvtColor(frame_og, cv2.COLOR_BGR2GRAY)
        ret, frame = cv2.threshold(frame, 200, 250, cv2.THRESH_TOZERO)

        kernel = np.ones(5)
        frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)

        contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        frame = cv2.drawContours(frame, contours, -1, (0, 255, 255), 3)

        for contour in contours:
            (x, y, width, height) = cv2.boundingRect(contour)

            s = s2 = 0
            for i in range(x):
                try:
                    s += int(frame[y][i])
                    if s != 0:
                        break
                except:
                    s += sum(frame[y][i])
                    if s != 0:
                        break

            for i in range(x + width, len(frame[0])):
                try:
                    s2 += int(frame[y][i])
                    if s2 != 0:
                        break

                except:
                    s2 += sum(frame[y][i])
                    if s2 != 0:
                        break

            flag = 0
            delta = width / 10
            for i in range(y - 1, y):
                for j in range(int(x + width / 2 - delta), int(x + width / 2 + delta)):
                    if sum(frame_og[i][j]) > 250:
                        flag = 1
                        break
                if flag == 1:
                    break
            if flag == 1:
                continue

            if s == 0 or s2 == 0:
                continue

            upperbound = 150
            lowerbound = 10

            if height > upperbound or height < lowerbound or width > upperbound or width < lowerbound:
                continue

            frame = cv2.rectangle(frame_og, (x, y), (x + width, y + height), (255, 255, 0), 2)

        # Showing the video to the user.
        cv2.imshow("Bleh", frame_og)
        cv2.waitKey(1)

    videofeed.release()
    cv2.destroyAllWindows()


runthecode("bolt")
runthecode("virat")
