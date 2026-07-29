add_library(uwb_driver STATIC
    ${CMAKE_CURRENT_LIST_DIR}/decadriver/deca_interface.c
    ${CMAKE_CURRENT_LIST_DIR}/decadriver/deca_compat.c
    ${CMAKE_CURRENT_LIST_DIR}/decadriver/deca_rsl.c
    ${CMAKE_CURRENT_LIST_DIR}/decadriver/dw3720/dw3720_device.c
    ${CMAKE_CURRENT_LIST_DIR}/decadriver/lib/qmath/src/qmath.c
)

target_include_directories(uwb_driver PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
    ${CMAKE_CURRENT_LIST_DIR}/decadriver
    ${CMAKE_CURRENT_LIST_DIR}/decadriver/dw3720
    ${CMAKE_CURRENT_LIST_DIR}/decadriver/lib/qmath/include
)

target_compile_definitions(uwb_driver PUBLIC
    CONFIG_DW3000_CHIP_DW3000=0
    CONFIG_DW3000_CHIP_DW3720=1
    CONFIG_DW3000_SPI_TRACE=0
)
target_compile_options(uwb_driver PRIVATE -ffunction-sections -fdata-sections)
add_library(module_uwb INTERFACE)
target_sources(module_uwb INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/py_uwb.c
    ${CMAKE_CURRENT_LIST_DIR}/uwb_port.c
)
target_include_directories(module_uwb INTERFACE ${CMAKE_CURRENT_LIST_DIR})
target_link_libraries(module_uwb INTERFACE uwb_driver)
target_link_libraries(usermod INTERFACE module_uwb)
