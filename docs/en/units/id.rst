ID Unit
=======

.. include:: ../refs/unit.id.ref

The ``ID Unit`` is a crypto coprocessor with hardware-based secure key storage, integrated with ATECC608B hardware cryptographic chip, using I2C communication interface. The chip has a built-in 10Kb EEPROM for storing keys, certificates, data, consumption records and security configurations.

Support the following products:

    |IDUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import IDUnit


    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    id_0 = IDUnit(i2c0)
    print(id_0.get_sha256_hash('Hello M5', 1))
    print(id_0.get_generate_key(0, False))
    print(id_0.randrange(500, 1000, 5))

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |cores3_id_example.m5f2|


class IDUnit
------------

Constructors
------------

.. class:: IDUnit(i2c)

    Create a IDUnit object

    :param object i2c: the I2C object.
    
    UIFLOW2:

        |init.png|


Methods
-------

.. method:: IDUnit.get_revision_number() -> int

    Returns the ATECC608B revision number. A revision number refers to a version identifier that indicates a specific 
    iteration or update of the hardware design. The revision number helps distinguish between different versions of the same chip model.

    - Return: ``int``:  hexdecimal

    UIFLOW2:

        |get_revision_number.png|


.. method:: IDUnit.get_serial_number() -> str

    Returns the ATECC serial number.

    9-byte serial number is structured as follows:

        First 4 Bytes: These bytes are the first part of the serial number, which includes a fixed pattern and a portion that is unique to the device.
        Next 2 Bytes: These bytes are reserved and typically set to 0x00 or other reserved values.
        Last 3 Bytes: These bytes are the final part of the serial number and are unique to the device.

    - Return: ``string``  

    UIFLOW2:

        |get_serial_number.png|


.. method:: IDUnit.randint(min, max) -> int

    Returns the random number(4 byte). generate true random numbers using its hardware-based random number generator(RNG). 
    This RNG is often used in secure applications where high-quality randomness is needed, such as in key generation.

    :param int min: 0 ~ 4294967295.
    :param int max: 0 ~ 4294967295. 

    - Return: ``int``:  0 ~ 4294967295

    UIFLOW2:

        |randint.png|


.. method:: IDUnit.random() -> float

    Returns a random floating point number in the range [0.0 ~ 1.0].

    - Return: ``float``:  0.0 ~ 1.0

    UIFLOW2:

        |random.png|


.. method:: IDUnit.randrange(min, max, step) -> int

    The first form returns a random integer from the range(0, max). 
    The second form returns a random integer from the range (min, max, step) in steps of step. 
    For instance, calling randrange(1, 10, 2) will return odd numbers between 1 and 9 inclusive.

    :param int min: 0 ~ 4294967295.
    :param int max: 0 ~ 4294967295. 
    :param int step: 0 ~ 4294967295. 

    - Return: ``int``:   0 ~ 4294967295

    UIFLOW2:

        |randrange_max.png|
        |randrange.png|


.. method:: IDUnit.uniform(min, max) -> float

    Return a random floating point number N such that min <= N <= max for min <= max, and max <= N <= min for max < min.

    :param float min:
    :param float max:

    - Return: ``float``: 

    UIFLOW2:

        |uniform.png|


.. method:: IDUnit.get_generate_key(slot_num, private_key) -> bytearray

    Returns the generates a private or public key. A private key is a confidential piece of data that is used in 
    cryptography to perform various functions. A public key is a cryptographic key that is paired with a private 
    key in public-key cryptography.

    :param int slot_num: 0 ~ 4
    :param bool private_key: True or False

    - Return: ``bytearray``: 

    UIFLOW2:

        |get_generate_key.png|


.. method:: IDUnit.get_ecdsa_sign(slot, message) -> bytearray 

    Returns the ECDSA signatures. ECDSA is widely used in digital signatures 
    for ensuring the authenticity and integrity of messages and documents.

    :param int slot: 0 ~ 4
    :param message: ``string`` or ``list`` or ``bytearray``

    - Return: ``bytearray``: 

    UIFLOW2:

        |get_ecdsa_sign.png|


.. method:: IDUnit.get_verify_ecdsa_sign(message, sign, key) -> bool

    Returns the verify ecsda signature status. A signature verification in the Elliptic Curve Digital Signature Algorithm (ECDSA) 
    is the process of checking whether a given digital signature is valid and was indeed generated by the holder of the corresponding 
    private key or public key. This process ensures that the message or data.

    :param message: ``string`` or ``list`` or ``bytearray``
    :param sign: ``bytearray``
    :param key: ``bytearray``

    - Return: ``bool``: True or False

    UIFLOW2:

        |get_verify_ecdsa_sign.png|


.. method:: IDUnit.get_sha256_hash(message, format) -> str

    Get the generate the SHA-256 hash value. SHA-256 (Secure Hash Algorithm 256-bit) is a cryptographic hash 
    function that produces a fixed-size, 256-bit (32-byte) hash value, regardless of the size of the input data.

    :param message: ``string``
    :param format: 0: hexdecimal, 1: base64

    - Return: ``string``: 

    UIFLOW2:

        |get_sha256_hash.png|


.. method:: IDUnit.set_certificate_signing_request(slot_num, private_key, country, state_prov, city, org, org_unit, file_path) -> None

    A Certificate Signing Request (CSR) is a block of encoded text that is sent to a Certificate Authority (CA) when you apply for 
    an SSL/TLS certificate. It contains information that the CA uses to create your certificate, including your public key and some 
    information about your organization. 

    :param int slot_num: 0 ~ 4
    :param bool private_key: True or False
    :param str country: country name example: China
    :param str state_prov: states or province name
    :param str city: city name
    :param str org: organization or company name
    :param str org_unit: organization or company unit name
    :param str file_path: Store the file to flash or SD

    UIFLOW2:

        |set_certificate_signing_request.png|

.. method:: IDUnit.aes_ecb_encrypt(position, data) -> bytearray

    Performs AES-ECB mode encryption on data. The AES key is stored in slot 9 of the chip.

    :param int position: Position for encryption operation (used after left shift by 6)
    :param bytearray data: Data to be encrypted, must be 16 bytes

    - Return: ``bytearray``: Returns 16 bytes of encrypted data


.. method:: IDUnit.aes_ecb_decrypt(position, data) -> bytearray

    Performs AES-ECB mode decryption on data. The AES key is stored in slot 9 of the chip.

    :param int position: Position for decryption operation (used after left shift by 6)
    :param bytearray data: Data to be decrypted, must be 16 bytes

    - Return: ``bytearray``: Returns 16 bytes of decrypted data


.. method:: IDUnit.aes_gfm_encrypt(data) -> bytearray

    Performs Galois Field Multiplication (GFM) encryption operation in AES-GCM mode.

    :param bytearray data: Data to be encrypted, must be 16 bytes

    - Return: ``bytearray``: Returns 16 bytes of encrypted data

.. method:: IDUnit.ecdh_stored_key(slot_num, mode, external_public_key=None) -> bytearray

    Performs an ECDH key exchange operation using stored keys.

    :param int slot_num: The key slot number
    :param int mode: ECDH operation mode
    :param bytearray external_public_key: External public key, must be 64 bytes. If not provided, a new public key will be generated

    - Return: ``bytearray``: Returns 32 bytes shared secret when mode is 0x0C or 0x08;