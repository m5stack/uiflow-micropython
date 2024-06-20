include("manifest.py")  # noqa: F821

freeze("$(MPY_LIB_DIR)/python-ecosys/urequests", "urequests.py")  # noqa: F821

freeze("$(MPY_LIB_DIR)/micropython/upysh", "upysh.py")  # noqa: F821
freeze("$(MPY_LIB_DIR)/micropython/umqtt.simple", "umqtt/simple.py")  # noqa: F821
freeze("$(MPY_LIB_DIR)/micropython/umqtt.robust", "umqtt/robust.py")  # noqa: F821
