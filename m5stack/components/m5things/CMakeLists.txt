idf_component_register(
    SRCS
        "m5things.c"
        "crypto.c"
    INCLUDE_DIRS
        "include"
    REQUIRES
        json
        nvs_flash
        freertos
        main
        uiflow_utility
)

set_property(TARGET ${COMPONENT_LIB} APPEND PROPERTY LINK_INTERFACE_MULTIPLICITY 3)

# idf_component_register(
#                     INCLUDE_DIRS "include"
#                     REQUIRES nvs_flash main)
# target_link_libraries(${COMPONENT_TARGET} INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}/libm5things.a")
target_compile_definitions(${COMPONENT_LIB} PRIVATE BOARD_ID=${BOARD_ID})