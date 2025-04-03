ECG Module
============================

.. sku: M034

.. include:: ../refs/module.ecg.ref

This library is the driver for Module13.2 ECG, and the module communicates via UART.

Support the following products:

    |Module13.2 ECG|

UiFlow2 Example:
--------------------------

Heart Rate Monitoring Display
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |cores3_ecg_module_base_example.m5f2| project in UiFlow2.

This example program is used for real-time heart rate monitoring and ECG waveform display. During measurement, the device continuously plots the ECG (Electrocardiogram) waveform and automatically calculates and displays the heart rate data once the signal stabilizes.

**Electrode Placement Instructions**:
Please follow the guidelines below to correctly connect the ECG electrodes:

- ``Right Arm (RA)``: Place the right arm electrode on the right edge of the sternum, at the 2nd intercostal space along the midclavicular line, near the right shoulder.
- ``Left Arm (LA)``: Place the left arm electrode on the left edge of the sternum, at the 2nd intercostal space along the midclavicular line, near the left shoulder.
- ``Left Leg (LL)``: Place the left leg electrode above the iliac crest (hip bone) on the left lower abdomen, or on the lower left side of the abdomen.


**Measurement Precautions**:
To ensure stable and accurate ECG signals, please follow these precautions:

- ``Stay relaxed``: Avoid muscle tension to reduce signal interference.
- ``Remain still``: Minimize movement during measurement to obtain a stable ECG signal.


UiFlow2 Code Block:

    |cores3_ecg_module_base_example.png|

Example output:

    None
   
MicroPython Example:
--------------------------

Heart Rate Monitoring Display
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example program is used for real-time heart rate monitoring and ECG waveform display. During measurement, the device continuously plots the ECG (Electrocardiogram) waveform and automatically calculates and displays the heart rate data once the signal stabilizes.

**Electrode Placement Instructions**:
Please follow the guidelines below to correctly connect the ECG electrodes:

- ``Right Arm (RA)``: Place the right arm electrode on the right edge of the sternum, at the 2nd intercostal space along the midclavicular line, near the right shoulder.
- ``Left Arm (LA)``: Place the left arm electrode on the left edge of the sternum, at the 2nd intercostal space along the midclavicular line, near the left shoulder.
- ``Left Leg (LL)``: Place the left leg electrode above the iliac crest (hip bone) on the left lower abdomen, or on the lower left side of the abdomen.


**Measurement Precautions**:
To ensure stable and accurate ECG signals, please follow these precautions:

- ``Stay relaxed``: Avoid muscle tension to reduce signal interference.
- ``Remain still``: Minimize movement during measurement to obtain a stable ECG signal.


MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/ecg/cores3_ecg_module_base_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
--------------------------

ECGModule
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: module.ecg.ECGModule
    :members:
