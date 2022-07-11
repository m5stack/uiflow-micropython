add_library(usermod_M5UNIFIED INTERFACE)

target_sources(usermod_M5UNIFIED INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/m5unified.c
)

target_include_directories(usermod_M5UNIFIED INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_compile_definitions(usermod_M5UNIFIED INTERFACE
    ESP_PLATFORM=1  # Very important
)

target_link_libraries(usermod INTERFACE usermod_M5UNIFIED)

set_source_files_properties(
    ${CMAKE_CURRENT_LIST_DIR}/m5unified.c
    PROPERTIES COMPILE_FLAGS
    "-Wno-discarded-qualifiers -Wno-implicit-int"
)
