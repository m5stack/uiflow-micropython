add_library(usermod_M5THING INTERFACE)

target_sources(usermod_M5THING INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/modm5things.c
)

target_include_directories(usermod_M5THING INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(usermod INTERFACE usermod_M5THING)
