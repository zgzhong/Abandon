"""
人脸检测算法
"""

import dlib
from skimage import io

class DetectionResult(object):
    def __init__(self, image, faces):
        self._image = image
        self._faces = faces

    def __len__(self):
        return self._faces.__len__()

    def display(self):
        window = dlib.image_window()

        window.clear_overlay()
        window.set_image(self._image)
        window.add_overlay(self._faces)
        window.wait_until_closed()



class FaceDetection(object):

    @staticmethod
    def get_faces_dlib(image):
        """Find all face in the image. Using dlib face detector

        Parameters
        ----------
        image: numpy.ndarray
            must be channel last

        Returns
        -------
        face_array: DetectionResult
            face list represented by ndarray
        """
        detector = dlib.get_frontal_face_detector()
        # The 2 in the second argument indicates that we should upsample the image 2 time
        # this will make everything bigger and allow us to detect more faces
        results = detector(image, 2)

        return DetectionResult(image, results)



img = io.imread('/home/zgzhong/Desktop/stars.jpg')

ret = FaceDetection.get_faces_dlib(img)
ret.display()