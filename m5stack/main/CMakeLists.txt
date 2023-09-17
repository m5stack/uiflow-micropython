# LVGL support
if(BUILD_WITH_LVGL)
    message(STATUS "Build with LVGL enable...")
    include(${PROJECT_DIR}/main/CMakeListsLvgl.cmake)
else()
    include(${PROJECT_DIR}/main/CMakeListsDefault.cmake)
endif()
