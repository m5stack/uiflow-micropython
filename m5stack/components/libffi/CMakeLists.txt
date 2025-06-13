idf_build_get_property(target IDF_TARGET)

if(target STREQUAL "esp32" OR target STREQUAL "esp32s3")
    set(srcs
        "libffi/src/prep_cif.c"
        "libffi/src/types.c"
        "libffi/src/xtensa/ffi.c"
        "libffi/src/xtensa/sysv.S"
    )
    set(include_dirs libffi/include libffi/include/xtensa)
elseif(target STREQUAL "esp32c3" OR target STREQUAL "esp32c6" OR target STREQUAL "esp32p4")
    set(srcs
        "libffi/src/prep_cif.c"
        "libffi/src/types.c"
        "libffi/src/riscv/ffi.cpp"
        "libffi/src/riscv/sysv.S"
    )
    set(include_dirs libffi/include libffi/include/riscv)
endif()

idf_component_register(SRCS "${srcs}"
                    INCLUDE_DIRS "${include_dirs}")
