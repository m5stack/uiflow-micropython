# Create an INTERFACE library for our C module.
add_library(usermod_M5CAMERA INTERFACE)

# Add our source files to the lib
target_sources(usermod_M5CAMERA INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/m5camera.c
)

# Add the current directory as an include directory.
target_include_directories(usermod_M5CAMERA INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
    ${CMAKE_CURRENT_LIST_DIR}/../../components/esp32-camera/driver/include
    ${CMAKE_CURRENT_LIST_DIR}/../../components/esp32-camera/driver/private_include
    ${CMAKE_CURRENT_LIST_DIR}/../../components/esp32-camera/conversions/include
    ${CMAKE_CURRENT_LIST_DIR}/../../components/esp32-camera/conversions/private_include
    ${CMAKE_CURRENT_LIST_DIR}/../../components/esp32-camera/sensors/private_include
)

# Link our INTERFACE library to the usermod target.
target_link_libraries(usermod INTERFACE usermod_M5CAMERA)
