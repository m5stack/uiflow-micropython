dl --- deep learning 
=====================================

.. include:: ../refs/advanced.dl.ref

.. note:: This module is only applicable to the CoreS3 Controller

.. module:: dl
   :synopsis: deep learning

Micropython Example 
--------------------------------

human face detect
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../examples/advanced/dl/cores3_example_human_face_detect.py
        :language: python
        :linenos:
        

pedestrain detect
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../examples/advanced/dl/cores3_example_pedestrian_detect.py
        :language: python
        :linenos:
 
human face recognition  
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../examples/advanced/dl/cores3_example_human_face_recognition.py
        :language: python
        :linenos:
 

UIFlow2.0 Example 
--------------------------------

human face detect
++++++++++++++++++++++++++++

    |human_face_detect_example.png|

.. only:: builder_html

    |cores3_example_human_face_detect.m5f2|

pedestrain detect
++++++++++++++++++++++++++++

    |pedestrian_detect_example.png|

.. only:: builder_html

    |cores3_example_pedestrian_detect.m5f2|

human face recognition  
++++++++++++++++++++++++++++

    |human_face_recognition_example.png|

.. only:: builder_html

    |cores3_example_human_face_recognition.m5f2|

Funtions
------------------------------

.. function:: dl.ObjectDetector(model) -> ObjectDetector

    Create an object detector instance.

    :param model: Load a detection model. Supported values:
      
    - ``dl.model.HUMAN_FACE_DETECT``: Human face detection.
    - ``dl.model.PEDESTRIAN_DETECT``: Pedestrian detection.

    Returns An ``ObjectDetector`` instance.

    UIFlow2.0

        |ObjectDetector.png|

    **Example**::

        detector = dl.ObjectDetector(dl.model.HUMAN_FACE_DETECT)
        detector = dl.ObjectDetector(dl.model.PEDESTRIAN_DETECT)

.. function:: dl.HumanFaceRecognizer() -> HumanFaceRecognizer

    Create a human face recognizer instance.

    Returns: A ``HumanFaceRecognizer`` instance.

    UIFlow2.0

        |HumanFaceRecognizer.png|

class ObjectDetector  
------------------------------
The ObjectDetector object is returned by `dl.ObjectDetector(model)`.

.. method:: ObjectDetector.infer(img: image.Image) -> DetectionResult

    Returns: A ``DetectionResult`` instance.

    UIFlow2.0

        |infer.png|

class HumanFaceRecognizer  
------------------------------
The HumanFaceRecognizer object is returned by `dl.HumanFaceRecognizer()`.

.. method:: HumanFaceRecognizer.recognize(img: image:Image, keypoint: tuple) -> RecognitionResult

    Face recognize

    - ``img`` imput image
    - ``keypoint`` face keypoint, ref: DetectionResult.keypoint()

    Returns an ``RecognitionResult`` object

    UIFlow2.0

        |recognize.png|

.. method:: HumanFaceRecognizer.clear_id() 

    clear id 

    UIFlow2.0

        |clear_id.png|


.. method:: HumanFaceRecognizer.enroll_id(img: image:Image, keypoint: tuple) -> bool

    enroll id 

    - ``img`` imput image
    - ``keypoint`` face keypoint, ref: DetectionResult.keypoint()

    UIFlow2.0

        |enroll_id.png|

.. method:: HumanFaceRecognizer.delete_id([id])

    delete id

    id is an optional parameter. If provided, it deletes the specified face information. By default, it deletes the most recently recorded id.

    UIFlow2.0

        |delete_id.png|

        |delete_last_id.png|

.. method:: HumanFaceRecognizer.enrolled_id_num() -> int

    get enrolled id num

    UIFlow2.0

        |enrolled_id_num.png| 

class DetectionResult -- DetectionResult object
-----------------------------------------------

The line object is returned by `ObjectDetector.infer()`.

.. method:: DetectionResult.bbox() -> tuple(x, y, w, h) 
    
    Get the bounding box of the object detection. 

    UIFlow2.0

        |get_bbox.png| 

.. method:: DetectionResult.x() -> int 

    The x-coordinate of the top-left corner of the bounding box.

    UIFlow2.0

        |get_x.png| 

.. method:: DetectionResult.y() -> int 

    The y-coordinate of the top-left corner of the bounding box.

    UIFlow2.0

        |get_y.png| 

.. method:: DetectionResult.w() -> int 

    The width of the bounding box.

    UIFlow2.0

        |get_w.png| 

.. method:: DetectionResult.h() -> int 

    The height of the bounding box.

    UIFlow2.0

        |get_h.png| 

.. method:: DetectionResult.category() -> int 

    The detected object's category.

    UIFlow2.0

        |get_category.png| 

.. method:: DetectionResult.keypoint() -> tuple

    Keypoint information (currently, only the face detection model outputs this data):

    - ``keypoint()[0], keypoint()[1]`` are the coordinates of the left eye.
    - ``keypoint()[2], keypoint()[3]`` are the coordinates of the left corner of the mouth.
    - ``keypoint()[4], keypoint()[5]`` are the coordinates of the nose.
    - ``keypoint()[6], keypoint()[7]`` are the coordinates of the right eye.
    - ``keypoint()[8], keypoint()[9]`` are the coordinates of the right corner of the mouth.

    UIFlow2.0

        |get_keypoint.png| 

class RecognitionResult -- RecognitionResult object
--------------------------------------------------- 

The ``RecognitionResult`` is returned by `HumanFaceRecognizer.recognize(img, keypoint)`.

.. method:: RecognitionResult.similarity() -> float
    
    Gets the face similarity, with a value closer to 1 indicating higher similarity.

    UIFlow2.0

        |similarity.png| 

.. method:: RecognitionResult.id() -> int

    Gets the face ID. A value greater than 0 indicates that the face recognition was successful.

    UIFlow2.0

        |id.png| 

 
