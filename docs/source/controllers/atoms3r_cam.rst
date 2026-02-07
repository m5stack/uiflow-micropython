AtomS3R-CAM
==============

.. sku: C126-CAM

.. include:: ../refs/controllers.atoms3r_cam.ref

Support the following products:

    |AtomS3R-CAM|


MicroPython Example:
--------------------------

Video Streaming
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example implements a real-time video streaming server, with integrated QR code recognition.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/atoms3r_cam/video_streaming.py
        :language: python
        :linenos:

Example output:

    None


**How to Use**

1. Configure Wi-Fi settings.

.. figure:: ./../../_static/controllers/atoms3r_cam/configure.png
   :width: 800
   :align: center

1. Copy the example code into the editor.

.. figure:: ./../../_static/controllers/atoms3r_cam/copy_paste_example_code.png
   :width: 800
   :align: center

3. Run the program, After uploading, the console will print the local IP address assigned to the device.

.. figure:: ./../../_static/controllers/atoms3r_cam/connect.png
   :width: 800
   :align: center

.. figure:: ./../../_static/controllers/atoms3r_cam/run.png
   :width: 800
   :align: center

5. Open the video stream in your browser

On any device connected to the same Wi-Fi network, open a browser and visit: http://<device-ip>:8080/,
Replace `<device-ip>` with the actual IP address printed in the console.

.. figure:: ./../../_static/controllers/atoms3r_cam/browser.png
   :width: 800
   :align: center


