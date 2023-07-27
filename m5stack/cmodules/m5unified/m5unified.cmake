add_library(usermod_M5UNIFIED INTERFACE)

target_sources(usermod_M5UNIFIED INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/m5unified_als.c
    ${CMAKE_CURRENT_LIST_DIR}/m5unified_button.c
    ${CMAKE_CURRENT_LIST_DIR}/m5unified_gfx.c
    ${CMAKE_CURRENT_LIST_DIR}/m5unified_imu.c
    ${CMAKE_CURRENT_LIST_DIR}/m5unified_lvgl.c
    ${CMAKE_CURRENT_LIST_DIR}/m5unified_power.c
    ${CMAKE_CURRENT_LIST_DIR}/m5unified_speaker.c
    ${CMAKE_CURRENT_LIST_DIR}/m5unified_touch.c
    ${CMAKE_CURRENT_LIST_DIR}/m5unified_widgets.c
    ${CMAKE_CURRENT_LIST_DIR}/m5unified.c
)

target_include_directories(usermod_M5UNIFIED INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

if (BOARD_TYPE STREQUAL "stickcplus2")
    target_compile_definitions(usermod_M5UNIFIED INTERFACE TINY_FONT=1)
endif()

target_link_libraries(usermod INTERFACE usermod_M5UNIFIED)

set_source_files_properties(
    ${CMAKE_CURRENT_LIST_DIR}/m5unified.c
    PROPERTIES COMPILE_FLAGS
    "-Wno-discarded-qualifiers -Wno-implicit-int"
)
