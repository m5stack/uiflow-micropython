# LVGL support
if(BUILD_WITH_LVGL)
    message(STATUS "Build with LVGL enable...")
    include(${PROJECT_DIR}/CMakeListsLvgl.cmake)
else()
    include(${PROJECT_DIR}/CMakeListsDefault.cmake)
endif()
