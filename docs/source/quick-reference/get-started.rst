###########
Get Started
###########

.. include:: ../refs/qr.get-started.ref

***********
Preparation
***********

Driver Installation
===================

Click the link below to download the driver that matches the operating system.
There are currently two driver chip versions (CP210X/CH9102). Please download
the corresponding driver compressed package according to the version you are
using. After decompressing the compressed package, select the installation
package corresponding to the number of operating systems to install.

If you are not sure of the USB chip used by your device, you can install both
drivers at the same time.

.. warning::

    During the installation process of CH9102_VCP_SER_MacOS v1.7, an error may
    occur, but the installation is actually completed, just ignore it.

========================= ======================= =========================
Driver name               Applicable driver chip   Download link
========================= ======================= =========================
CP210x_VCP_Windows        CP2104                  |CP210x_VCP_Windows|_
------------------------- ----------------------- -------------------------
CP210x_VCP_MacOS          CP2104                  |CP210x_VCP_MacOS|_
------------------------- ----------------------- -------------------------
CP210x_VCP_Linux          CP2104                  |CP210x_VCP_Linux|_
------------------------- ----------------------- -------------------------
CH9102_VCP_SER_Windows    CH9102                  |CH9102_VCP_SER_Windows|_
------------------------- ----------------------- -------------------------
CH9102_VCP_SER_MacOS v1.7 CH9102                  |CH9102_VCP_MacOS_v1.7|_
========================= ======================= =========================

M5Burner
========

Please click the button below to download the corresponding M5Burner firmware
burning tool according to your operating system. Open the application after
decompression.

================ =============================
Software         Link
================ =============================
M5Burner_Windows |M5Burner-v3-beta-win-x64|_
---------------- -----------------------------
M5Burner_MacOS   |M5Burner-v3-beta-mac-x64|_
---------------- -----------------------------
M5Burner_Linux   |M5Burner-v3-beta-linux-x64|_
================ =============================

********************
Installation UIFLOW2
********************

Login M5Burner
==============

Before using UIFlow2, you need to log in to your M5Stack account first.
If you don't have an account yet, please register an account first.

|login-m5burner.gif|

Firmware Burning
================

Before burning firmware, first put the host into download mode. Each device has
different ways of entering download mode. For details, please refer to the
corresponding host product documentation.

Before burning, M5Burner will bind your host and M5Stack account.
After binding, you can use your host in UIFlow2.

|burn-firmware.gif|

*******************
Start using UIFLOW2
*******************

Login UIFlow2
=============

Log in to https://uiflow2.m5stack.com/

|login-uiflow2.gif|
