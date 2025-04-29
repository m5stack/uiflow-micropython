dl --- deep learning
====================

.. include:: ../refs/advanced.dl.ref

.. note:: This module is only applicable to the CoreS3 Controller

.. module:: dl
   :synopsis: deep learning


UiFlow2 Example
---------------

human face detect
+++++++++++++++++

Open the |cores3_example_human_face_detect.m5f2| project in UiFlow2.

This example uses a face detection algorithm to detect faces in real time from
the camera feed. When a face is detected, a bounding box is drawn on the screen
to mark the face's position, providing an intuitive visualization of the
detection results.

UiFlow2 Code Block:

    |human_face_detect_example.png|

Example output:

    None


pedestrain detect
+++++++++++++++++

Open the |cores3_example_pedestrian_detect.m5f2| project in UiFlow2.

This example uses a pedestrian detection algorithm to detect pedestrian targets
in real time from the camera feed. When a pedestrian is detected, a bounding box
is drawn on the screen to highlight the pedestrian's position, providing an
intuitive demonstration of the detection results.

UiFlow2 Code Block:

    |pedestrian_detect_example.png|

Example output:

    None

human face recognition
++++++++++++++++++++++

Open the |cores3_example_human_face_recognition.m5f2| project in UiFlow2.

To run this example, you will need the `CoreS3 <https://docs.m5stack.com/en/core/CoreS3>`_ 
and the `Unit Dual Button <https://docs.m5stack.com/en/unit/dual_button>`_.

This example uses a face recognition algorithm to detect faces in real time from
the camera feed.

By pressing different buttons, you can either enroll new face data or perform
face recognition. The detected faces and recognition results are displayed on
the screen with bounding boxes.

UiFlow2 Code Block:

    |human_face_recognition_example.png|

Example output:

    None


Micropython Example
-------------------

human face detect
+++++++++++++++++


MicroPython Code Block:

    .. literalinclude:: ../../../examples/advanced/dl/cores3_example_human_face_detect.py
        :language: python
        :linenos:

Example output:

    None

pedestrain detect
+++++++++++++++++

MicroPython Code Block:

    .. literalinclude:: ../../../examples/advanced/dl/cores3_example_pedestrian_detect.py
        :language: python
        :linenos:

Example output:

    None


human face recognition
++++++++++++++++++++++

MicroPython Code Block:

    .. literalinclude:: ../../../examples/advanced/dl/cores3_example_human_face_recognition.py
        :language: python
        :linenos:

Example output:

    None


Funtions
--------

.. function:: dl.ObjectDetector(model) -> ObjectDetector

    Create an object detector instance.

    :param model: Load a detection model. Supported values:

    - ``dl.model.HUMAN_FACE_DETECT``: Human face detection.
    - ``dl.model.PEDESTRIAN_DETECT``: Pedestrian detection.

    Returns An ``ObjectDetector`` instance.

    UiFlow2 Code Block:

        |ObjectDetector.png|

    **Example**::

        detector = dl.ObjectDetector(dl.model.HUMAN_FACE_DETECT)
        detector = dl.ObjectDetector(dl.model.PEDESTRIAN_DETECT)

.. function:: dl.HumanFaceRecognizer() -> HumanFaceRecognizer

    Create a human face recognizer instance.

    Returns: A ``HumanFaceRecognizer`` instance.

    UiFlow2 Code Block:

        |HumanFaceRecognizer.png|


class ObjectDetector
--------------------

The ObjectDetector object is returned by `dl.ObjectDetector(model)`.

.. method:: ObjectDetector.infer(img: image.Image) -> DetectionResult

    Returns: A ``DetectionResult`` instance.

    UiFlow2 Code Block:

        |infer.png|


class HumanFaceRecognizer
-------------------------

The HumanFaceRecognizer object is returned by `dl.HumanFaceRecognizer()`.

.. method:: HumanFaceRecognizer.recognize(img: image:Image, keypoint: tuple) -> RecognitionResult

    Face recognize

    - ``img`` imput image
    - ``keypoint`` face keypoint, ref: DetectionResult.keypoint()

    Returns an ``RecognitionResult`` object

    UiFlow2 Code Block:

        |recognize.png|

.. method:: HumanFaceRecognizer.clear_id()

    clear id

    UiFlow2 Code Block:

        |clear_id.png|

.. method:: HumanFaceRecognizer.enroll_id(img: image:Image, keypoint: tuple) -> bool

    enroll id

    - ``img`` imput image
    - ``keypoint`` face keypoint, ref: DetectionResult.keypoint()

    UiFlow2 Code Block:

        |enroll_id.png|

.. method:: HumanFaceRecognizer.delete_id([id])

    delete id

    id is an optional parameter. If provided, it deletes the specified face information. By default, it deletes the most recently recorded id.

    UiFlow2 Code Block:

        |delete_id.png|

        |delete_last_id.png|

.. method:: HumanFaceRecognizer.enrolled_id_num() -> int

    get enrolled id num

    UiFlow2 Code Block:

        |enrolled_id_num.png|


class DetectionResult -- DetectionResult object
-----------------------------------------------

The line object is returned by `ObjectDetector.infer()`.

.. method:: DetectionResult.bbox() -> tuple(x, y, w, h)

    Get the bounding box of the object detection.

    UiFlow2 Code Block:

        |get_bbox.png|

.. method:: DetectionResult.x() -> int

    The x-coordinate of the top-left corner of the bounding box.

    UiFlow2 Code Block:

        |get_x.png|

.. method:: DetectionResult.y() -> int

    The y-coordinate of the top-left corner of the bounding box.

    UiFlow2 Code Block:

        |get_y.png|

.. method:: DetectionResult.w() -> int

    The width of the bounding box.

    UiFlow2 Code Block:

        |get_w.png|

.. method:: DetectionResult.h() -> int

    The height of the bounding box.

    UiFlow2 Code Block:

        |get_h.png|

.. method:: DetectionResult.category() -> int

    The detected object's category.

    UiFlow2 Code Block:

        |get_category.png|

.. method:: DetectionResult.keypoint() -> tuple

    Keypoint information (currently, only the face detection model outputs this data):

    - ``keypoint()[0], keypoint()[1]`` are the coordinates of the left eye.
    - ``keypoint()[2], keypoint()[3]`` are the coordinates of the left corner of the mouth.
    - ``keypoint()[4], keypoint()[5]`` are the coordinates of the nose.
    - ``keypoint()[6], keypoint()[7]`` are the coordinates of the right eye.
    - ``keypoint()[8], keypoint()[9]`` are the coordinates of the right corner of the mouth.

    UiFlow2 Code Block:

        |get_keypoint.png|


class RecognitionResult -- RecognitionResult object
---------------------------------------------------

The ``RecognitionResult`` is returned by `HumanFaceRecognizer.recognize(img, keypoint)`.

.. method:: RecognitionResult.similarity() -> float

    Gets the face similarity, with a value closer to 1 indicating higher similarity.

    UiFlow2 Code Block:

        |similarity.png|

.. method:: RecognitionResult.id() -> int

    Gets the face ID. A value greater than 0 indicates that the face recognition was successful.

    UiFlow2 Code Block:

        |id.png|
