from tools import image_tools
import cv2
import numpy as np

class QuickStream(image_tools.VirtualStream):
    def grabImage(self):
        try:
            image = np.load(self.np_images[self.count])
            self.count += 1
            return image
        except KeyError:
            return None


if __name__ == '__main__':
    folder_path = 'C:\\Users\\e_q\\Documents\\source_tree\\main_program\\gui\\Simulation_2019_7_17-20_17_10'
    stream = image_tools.VirtualStream(numpyFolder=folder_path)
    cascade_src = 'C:\\Users\\e_q\\Documents\\source_tree\\main_program\\car_detection\\cars.xml'
    car_cascade = cv2.CascadeClassifier(cascade_src)

    while True:
        img = stream.grabImage()
        if (type(img) == type(None)):
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cars = car_cascade.detectMultiScale(gray, 1.1, 2, 0)

        for (x, y, w, h) in cars:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imshow('video', img)

        if cv2.waitKey() == 27:
            break

    cv2.destroyAllWindows()
