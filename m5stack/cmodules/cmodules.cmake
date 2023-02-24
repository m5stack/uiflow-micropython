# add m5unified module
include(${CMAKE_CURRENT_LIST_DIR}/m5unified/m5unified.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/m5things/m5things.cmake)

if(M5_CAMERA_MODULE_ENABLE)
    # add m5camera module
    include(${CMAKE_CURRENT_LIST_DIR}/m5camera/m5camera.cmake)
endif()