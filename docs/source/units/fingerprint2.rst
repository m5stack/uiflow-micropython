Fingerprint2 Unit 
=================

.. sku: U203

.. include:: ../refs/unit.fingerprint2.ref

This library is the driver for Unit Fingerprint2.

Support the following products:

    |Unit Fingerprint2|

UiFlow2 Example
---------------

Enroll and recognize
^^^^^^^^^^^^^^^^^^^^

Open the |m5cores3_fp2_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to use a fingerprint recognition module to perform 
the complete process of fingerprint enrollment, identification, and deletion.

UiFlow2 Code Block:

    |m5cores3_fp2_basic_example.png|

Example output:

    None

Upload and download template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |m5cores3_fp2_template_upload_download_example.m5f2| project in UiFlow2.

This example demonstrates how to use a fingerprint recognition module to perform the complete process of fingerprint enrollment, identification, deletion, 
and template upload/download.(The upload and download functions enable cross-device fingerprint recognition — a fingerprint enrolled on one module can be verified on another.
The fingerprint template transfer method can be customized according to user requirements, such as via serial communication, network, or cloud synchronization.)

UiFlow2 Code Block:

    |m5cores3_fp2_template_upload_download_example.png|

Example output:

    None

Upload adn display fingerprint image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |m5cores3_fp2_upload_image_example.m5f2| project in UiFlow2.

This example demonstrates how to upload and display the fingerprint image.

UiFlow2 Code Block:

    |m5cores3_fp2_upload_image_example.png|

Example output:

    None
 
MicroPython Example
-------------------

Enroll and recognize
^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to use a fingerprint recognition module to perform 
the complete process of fingerprint enrollment, identification, and deletion.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/fingerprint2/m5cores3_fp2_basic_example.py
        :language: python
        :linenos:

Example output:

    None

Upload and download template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to use a fingerprint recognition module to perform the complete process of fingerprint enrollment, identification, deletion, 
and template upload/download.(The upload and download functions enable cross-device fingerprint recognition — a fingerprint enrolled on one module can be verified on another.
The fingerprint template transfer method can be customized according to user requirements, such as via serial communication, network, or cloud synchronization.)

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/fingerprint2/m5cores3_fp2_template_upload_download_example.py
        :language: python
        :linenos:

Example output:

    None

Upload adn display fingerprint image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to upload and display the fingerprint image.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/fingerprint2/m5cores3_fp2_upload_image_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

Fingerprint2Unit
^^^^^^^^^^^^^^^^

.. autoclass:: unit.fingerprint2.Fingerprint2Unit
    :members:
