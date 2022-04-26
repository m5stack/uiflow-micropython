add_library(usermod_M5UNIFIED INTERFACE)

target_sources(usermod_M5UNIFIED INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/m5unified.c
    ${CMAKE_CURRENT_LIST_DIR}/mpy_m5btn.cpp
    ${CMAKE_CURRENT_LIST_DIR}/mpy_m5gfx.cpp
    ${CMAKE_CURRENT_LIST_DIR}/mpy_m5spk.cpp
    ${CMAKE_CURRENT_LIST_DIR}/mpy_m5unified.cpp
)

target_include_directories(usermod_M5UNIFIED INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_compile_definitions(usermod_M5UNIFIED INTERFACE
    MODULE_M5UNIFIED_ENABLED=1
    ESP_PLATFORM=1  # Very important
)

target_link_libraries(usermod INTERFACE usermod_M5UNIFIED)

set_source_files_properties(
    ${CMAKE_CURRENT_LIST_DIR}/m5unified.c
    PROPERTIES COMPILE_FLAGS
    "-Wno-discarded-qualifiers -Wno-implicit-int"
)
