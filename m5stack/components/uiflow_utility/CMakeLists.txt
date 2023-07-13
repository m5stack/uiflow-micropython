set(COMPONENT_ADD_INCLUDEDIRS
    .
)

file(GLOB SRCS
    *.c
)

set(COMPONENT_SRCS ${SRCS})
set(COMPONENT_REQUIRES nvs_flash)

register_component()
