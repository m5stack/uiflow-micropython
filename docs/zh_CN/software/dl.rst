:mod:`dl` ---  deep learning  
=====================================

.. include:: ../refs/software.dl.ref

.. note:: 当前模块只适用于 CoreS3 主机

.. module:: dl
   :synopsis: deep learning

Micropython 案例 
--------------------------------

人脸检测
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../examples/softwave/dl/cores3_example_human_face_detect.py
        :language: python
        :linenos:
 
行人检测
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../examples/softwave/dl/cores3_example_pedestrian_detect.py
        :language: python
        :linenos:
 

人脸识别
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../examples/softwave/dl/cores3_example_human_face_recognition.py
        :language: python
        :linenos:
 

UIFlow2.0 案例 
------------------------------

人脸检测 
++++++++++++++++++++++++++++

    |human_face_detect_example.png|

.. only:: builder_html

    |cores3_example_human_face_detect.m5f2|

行人检测
++++++++++++++++++++++++++++

    |pedestrian_detect_example.png|

.. only:: builder_html

    |cores3_example_pedestrian_detect.m5f2|

人脸识别
++++++++++++++++++++++++++++

    |human_face_recognition_example.png|

.. only:: builder_html

    |cores3_example_human_face_recognition.m5f2|

函数 
------------------------------

.. function:: dl.ObjectDetector(model) -> ObjectDetector

    创建一个目标检测器

    参数 ``model`` 仅接受以下值：
      
    - ``dl.model.HUMAN_FACE_DETECT`` 人脸检测
    - ``dl.model.PEDESTRIAN_DETECT`` 行人检测

    返回 ``ObjectDetector`` 对象.

    UIFlow2.0

      |ObjectDetector.png|

    **示例**::

        detector = dl.ObjectDetector(dl.model.HUMAN_FACE_DETECT)
        detector = dl.ObjectDetector(dl.model.PEDESTRIAN_DETECT)

.. function:: dl.HumanFaceRecognizer() -> HumanFaceRecognizer

    创建一个人脸识别器

    返回 ``HumanFaceRecognizer`` 对象.

     UIFlow2.0

      |HumanFaceRecognizer.png|

class ObjectDetector  
------------------------------
``ObjectDetector`` 对象由 dl.ObjectDetector(model) 返回

.. method:: ObjectDetector.infer(image:image.Image) -> DetectionResult

    返回一个 ``DetectionResult`` 实例.

    UIFlow2.0

        |infer.png|

class HumanFaceRecognizer  
------------------------------
``HumanFaceRecognizer`` 对象由 dl.HumanFaceRecognizer() 返回

.. method:: HumanFaceRecognizer.recognize(img: image:Image, keypoint: tuple) -> RecognitionResult

    人脸识别

    - ``img`` 输入图像 
    - ``keypoint`` 人脸关键点数据，详情参考 DetectionResult.keypoint() 解析 

    返回 ``RecognitionResult`` 对象。

    UIFlow2.0

        |recognize.png|


.. method:: HumanFaceRecognizer.clear_id() 

    清空所有 id

    UIFlow2.0

        |clear_id.png|


.. method:: HumanFaceRecognizer.enroll_id(img: image:Image, keypoint: tuple) -> bool

    录入人脸 id 

    - ``img`` 输入图像 
    - ``keypoint`` 人脸关键点数据，详情参考 DetectionResult.keypoint() 解析 

    UIFlow2.0

        |enroll_id.png|

.. method:: HumanFaceRecognizer.delete_id([id])

    删除人脸 id 

    - ``id`` 为可选参数，输入 ``id`` 为删除指定的人脸信息，默认为删除最近一次录入的 ``id``。

    UIFlow2.0

        |delete_id.png|

        |delete_last_id.png|

.. method:: HumanFaceRecognizer.enrolled_id_num() -> int

    返回已录入的 id 数

    UIFlow2.0

        |enrolled_id_num.png| 
      

class DetectionResult -- DetectionResult object
------------------------------
``DetectionResult`` 对象由 ObjectDetector.infer(img) 返回
 
.. method:: DetectionResult.bbox() -> tuple(x, y, w, h) 

    获取目标检测的边界框。

    UIFlow2.0

        |get_bbox.png| 

.. method:: DetectionResult.x() -> int 

    获取边界框的左上角坐标 x。

    UIFlow2.0

        |get_x.png| 

.. method:: DetectionResult.y() -> int 

    获取边界框的左上角坐标 y。

    UIFlow2.0

        |get_y.png| 

.. method:: DetectionResult.w() -> int 

    获取边界框的宽度。

    UIFlow2.0

        |get_w.png| 

.. method:: DetectionResult.h() -> int 

    获取边界框的高度。

    UIFlow2.0

        |get_h.png| 

.. method:: DetectionResult.category() -> int 

    检测到的目标类别。 

    UIFlow2.0

        |get_category.png| 

.. method:: DetectionResult.keypoint() -> tuple

    关键点信息(当前只有人脸检测模型输出包含此数据)

    - ``keypoint()[0], keypoint()[1]`` 为左眼坐标
    - ``keypoint()[2], keypoint()[3]`` 为嘴巴左角坐标
    - ``keypoint()[4], keypoint()[5]`` 为鼻子坐标
    - ``keypoint()[6], keypoint()[7]`` 为右眼坐标
    - ``keypoint()[8], keypoint()[9]`` 嘴巴右角

    UIFlow2.0

        |get_keypoint.png| 

 
class RecognitionResult -- RecognitionResult object
------------------------------
``DetectionResult`` 对象由 HumanFaceRecognizer.recognize(img, keypoint) 返回

.. method:: RecognitionResult.similarity() -> float

    获取人脸相似度，越接近1表示相似度越高。

    UIFlow2.0

        |similarity.png| 

.. method:: RecognitionResult.id() -> int

    获取人脸id，大于0表示人脸识别成功。

    UIFlow2.0

        |id.png| 

 
