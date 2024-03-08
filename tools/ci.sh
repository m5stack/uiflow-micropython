#!/bin/bash

#######################################################################################
#  Original file: https://github.com/micropython/micropython/blob/master/tools/ci.sh  #
#######################################################################################

if which nproc > /dev/null; then
    MAKEOPTS="-j$(nproc)"
else
    MAKEOPTS="-j$(sysctl -n hw.ncpu)"
fi

########################################################################################
# code formatting

function ci_code_formatting_setup {
    sudo apt-add-repository --yes --update ppa:pybricks/ppa
    sudo apt-get install uncrustify
    pip3 install black
    uncrustify --version
    black --version
}

function ci_code_formatting_run {
    tools/codeformat.py -v
}

########################################################################################
# commit formatting

function ci_commit_formatting_run {
    git remote add upstream https://github.com/micropython/micropython.git
    git fetch --depth=100 upstream  master
    # For a PR, upstream/master..HEAD ends with a merge commit into master, exlude that one.
    tools/verifygitlog.py -v upstream/master..HEAD --no-merges
}

########################################################################################
# code size

function ci_code_size_setup {
    sudo apt-get update
    sudo apt-get install gcc-multilib
    gcc --version
    ci_gcc_arm_setup
}

function ci_code_size_build {
    # starts off at either the ref/pull/N/merge FETCH_HEAD, or the current branch HEAD
    git checkout -b pull_request # save the current location
    git remote add upstream https://github.com/micropython/micropython.git
    git fetch --depth=100 upstream master
    # build reference, save to size0
    # ignore any errors with this build, in case master is failing
    git checkout `git merge-base --fork-point upstream/master pull_request`
    git show -s
    tools/metrics.py clean bm
    tools/metrics.py build bm | tee ~/size0 || true
    # build PR/branch, save to size1
    git checkout pull_request
    git log upstream/master..HEAD
    tools/metrics.py clean bm
    tools/metrics.py build bm | tee ~/size1
}

########################################################################################
# ports/esp32

function ci_esp32_setup_helper {
    git clone https://github.com/m5stack/esp-idf.git
    git -C esp-idf checkout $1
    git -C esp-idf submodule update --init \
        components/bt/host/nimble/nimble \
        components/esp_wifi \
        components/esptool_py/esptool \
        components/lwip/lwip \
        components/mbedtls/mbedtls
    if [ -d esp-idf/components/bt/controller/esp32 ]; then
        git -C esp-idf submodule update --init \
            components/bt/controller/lib_esp32 \
            components/bt/controller/lib_esp32c3_family
    else
        git -C esp-idf submodule update --init \
            components/bt/controller/lib
    fi
    ./esp-idf/install.sh
}

function ci_esp32_idf44_setup {
    ci_esp32_setup_helper 014ee65f1f5e291230e398c4913020be9a6278a1
}

function ci_esp32_idf504_setup {
    ci_esp32_setup_helper 8fbf4ba6058bcf736317d8a7aa75d0578563c38b
}

function ci_esp32_build {
    source esp-idf/export.sh
    make ${MAKEOPTS} -C m5stack submodules
    make ${MAKEOPTS} -C m5stack littlefs
    make ${MAKEOPTS} -C m5stack mpy-cross
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_8MB
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_SPIRAM_8MB

    # before lvgl build test, we need make clean
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_8MB clean
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_SPIRAM_8MB clean
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_8MB LVGL=1
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_SPIRAM_8MB LVGL=1
    
    # if [ -d $IDF_PATH/components/esp32c3 ]; then
    #     make ${MAKEOPTS} -C m5stack BOARD=M5STACK_C3
    #     make ${MAKEOPTS} -C m5stack BOARD=M5STACK_C3_USB
    # fi
    # if [ -d $IDF_PATH/components/esp32s2 ]; then
    #     make ${MAKEOPTS} -C m5stack BOARD=GENERIC_S2
    # fi

    if [ -d $IDF_PATH/components/esp32s3 ]; then
        make ${MAKEOPTS} -C m5stack BOARD=M5STACK_S3_8MB
        make ${MAKEOPTS} -C m5stack BOARD=M5STACK_S3_SPIRAM_8MB

        # before lvgl build test, we need make clean
        make ${MAKEOPTS} -C m5stack BOARD=M5STACK_S3_8MB clean
        make ${MAKEOPTS} -C m5stack BOARD=M5STACK_S3_SPIRAM_8MB clean
        make ${MAKEOPTS} -C m5stack BOARD=M5STACK_S3_8MB LVGL=1
        make ${MAKEOPTS} -C m5stack BOARD=M5STACK_S3_SPIRAM_8MB LVGL=1
    fi
}

function ci_esp32_nightly_build {
    source esp-idf/export.sh
    make ${MAKEOPTS} -C m5stack unpatch
    make ${MAKEOPTS} -C m5stack submodules
    make ${MAKEOPTS} -C m5stack patch
    make ${MAKEOPTS} -C m5stack littlefs
    make ${MAKEOPTS} -C m5stack mpy-cross
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_AirQ pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_AtomS3 pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_AtomS3_Lite pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_AtomS3U pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_Basic pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_Basic_4MB pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_Capsule pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_Cardputer pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_Core2 pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_CoreInk pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_CoreS3 pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_Dial pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_DinMeter pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_Fire pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_Paper pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_StampS3 pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_StickC pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_StickC_PLUS pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_StickC_PLUS2 pack_all
    make ${MAKEOPTS} -C m5stack BOARD=M5STACK_Tough pack_all
}

# BELOW PLATFORM NOT SUPPORTED FOR NOW, MAYBE SUPPORT IN THE FUTURE
########################################################################################
# ports/unix

CI_UNIX_OPTS_SYS_SETTRACE=(
    MICROPY_PY_BTREE=0
    MICROPY_PY_FFI=0
    MICROPY_PY_USSL=0
    CFLAGS_EXTRA="-DMICROPY_PY_SYS_SETTRACE=1"
)

CI_UNIX_OPTS_SYS_SETTRACE_STACKLESS=(
    MICROPY_PY_BTREE=0
    MICROPY_PY_FFI=0
    MICROPY_PY_USSL=0
    CFLAGS_EXTRA="-DMICROPY_STACKLESS=1 -DMICROPY_STACKLESS_STRICT=1 -DMICROPY_PY_SYS_SETTRACE=1"
)

CI_UNIX_OPTS_QEMU_MIPS=(
    CROSS_COMPILE=mips-linux-gnu-
    VARIANT=coverage
    MICROPY_STANDALONE=1
    LDFLAGS_EXTRA="-static"
)

CI_UNIX_OPTS_QEMU_ARM=(
    CROSS_COMPILE=arm-linux-gnueabi-
    VARIANT=coverage
    MICROPY_STANDALONE=1
)

function ci_unix_build_helper {
    make ${MAKEOPTS} -C mpy-cross
    make ${MAKEOPTS} -C ports/unix "$@" submodules
    make ${MAKEOPTS} -C ports/unix "$@" deplibs
    make ${MAKEOPTS} -C ports/unix "$@"
}

function ci_unix_build_ffi_lib_helper {
    $1 $2 -shared -o tests/unix/ffi_lib.so tests/unix/ffi_lib.c
}

function ci_unix_run_tests_helper {
    make -C ports/unix "$@" test
}

function ci_unix_run_tests_full_helper {
    variant=$1
    shift
    if [ $variant = standard ]; then
        micropython=micropython
    else
        micropython=micropython-$variant
    fi
    make -C ports/unix VARIANT=$variant "$@" test_full
    (cd tests && MICROPY_CPYTHON3=python3 MICROPY_MICROPYTHON=../ports/unix/$micropython ./run-multitests.py multi_net/*.py)
}

function ci_native_mpy_modules_build {
    if [ "$1" = "" ]; then
        arch=x64
    else
        arch=$1
    fi
    make -C examples/natmod/features1 ARCH=$arch
    make -C examples/natmod/features2 ARCH=$arch
    make -C examples/natmod/btree ARCH=$arch
    make -C examples/natmod/framebuf ARCH=$arch
    make -C examples/natmod/uheapq ARCH=$arch
    make -C examples/natmod/urandom ARCH=$arch
    make -C examples/natmod/ure ARCH=$arch
    make -C examples/natmod/uzlib ARCH=$arch
}

function ci_native_mpy_modules_32bit_build {
    ci_native_mpy_modules_build x86
}

function ci_unix_minimal_build {
    make ${MAKEOPTS} -C ports/unix VARIANT=minimal
}

function ci_unix_minimal_run_tests {
    (cd tests && MICROPY_CPYTHON3=python3 MICROPY_MICROPYTHON=../ports/unix/micropython-minimal ./run-tests.py -e exception_chain -e self_type_check -e subclass_native_init -d basics)
}

function ci_unix_standard_build {
    ci_unix_build_helper VARIANT=standard
    ci_unix_build_ffi_lib_helper gcc
}

function ci_unix_standard_run_tests {
    ci_unix_run_tests_full_helper standard
}

function ci_unix_standard_run_perfbench {
    (cd tests && MICROPY_CPYTHON3=python3 MICROPY_MICROPYTHON=../ports/unix/micropython ./run-perfbench.py 1000 1000)
}

function ci_unix_dev_build {
    ci_unix_build_helper VARIANT=dev
}

function ci_unix_dev_run_tests {
    ci_unix_run_tests_helper VARIANT=dev
}

function ci_unix_coverage_setup {
    sudo pip3 install setuptools
    sudo pip3 install pyelftools
    gcc --version
    python3 --version
}

function ci_unix_coverage_build {
    ci_unix_build_helper VARIANT=coverage
    ci_unix_build_ffi_lib_helper gcc
}

function ci_unix_coverage_run_tests {
    ci_unix_run_tests_full_helper coverage
}

function ci_unix_coverage_run_native_mpy_tests {
    MICROPYPATH=examples/natmod/features2 ./ports/unix/micropython-coverage -m features2
    (cd tests && ./run-natmodtests.py "$@" extmod/{btree*,framebuf*,uheapq*,ure*,uzlib*}.py)
}

function ci_unix_32bit_setup {
    sudo dpkg --add-architecture i386
    sudo apt-get update
    sudo apt-get install gcc-multilib g++-multilib libffi-dev:i386
    sudo pip3 install setuptools
    sudo pip3 install pyelftools
    gcc --version
    python2 --version
    python3 --version
}

function ci_unix_coverage_32bit_build {
    ci_unix_build_helper VARIANT=coverage MICROPY_FORCE_32BIT=1
    ci_unix_build_ffi_lib_helper gcc -m32
}

function ci_unix_coverage_32bit_run_tests {
    ci_unix_run_tests_full_helper coverage MICROPY_FORCE_32BIT=1
}

function ci_unix_coverage_32bit_run_native_mpy_tests {
    ci_unix_coverage_run_native_mpy_tests --arch x86
}

function ci_unix_nanbox_build {
    # Use Python 2 to check that it can run the build scripts
    ci_unix_build_helper PYTHON=python2 VARIANT=nanbox
    ci_unix_build_ffi_lib_helper gcc -m32
}

function ci_unix_nanbox_run_tests {
    ci_unix_run_tests_full_helper nanbox PYTHON=python2
}

function ci_unix_float_build {
    ci_unix_build_helper VARIANT=standard CFLAGS_EXTRA="-DMICROPY_FLOAT_IMPL=MICROPY_FLOAT_IMPL_FLOAT"
    ci_unix_build_ffi_lib_helper gcc
}

function ci_unix_float_run_tests {
    # TODO get this working: ci_unix_run_tests_full_helper standard CFLAGS_EXTRA="-DMICROPY_FLOAT_IMPL=MICROPY_FLOAT_IMPL_FLOAT"
    ci_unix_run_tests_helper CFLAGS_EXTRA="-DMICROPY_FLOAT_IMPL=MICROPY_FLOAT_IMPL_FLOAT"
}

function ci_unix_clang_setup {
    sudo apt-get install clang
    clang --version
}

function ci_unix_stackless_clang_build {
    make ${MAKEOPTS} -C mpy-cross CC=clang
    make ${MAKEOPTS} -C ports/unix submodules
    make ${MAKEOPTS} -C ports/unix CC=clang CFLAGS_EXTRA="-DMICROPY_STACKLESS=1 -DMICROPY_STACKLESS_STRICT=1"
}

function ci_unix_stackless_clang_run_tests {
    ci_unix_run_tests_helper CC=clang
}

function ci_unix_float_clang_build {
    make ${MAKEOPTS} -C mpy-cross CC=clang
    make ${MAKEOPTS} -C ports/unix submodules
    make ${MAKEOPTS} -C ports/unix CC=clang CFLAGS_EXTRA="-DMICROPY_FLOAT_IMPL=MICROPY_FLOAT_IMPL_FLOAT"
}

function ci_unix_float_clang_run_tests {
    ci_unix_run_tests_helper CC=clang
}

function ci_unix_settrace_build {
    make ${MAKEOPTS} -C mpy-cross
    make ${MAKEOPTS} -C ports/unix "${CI_UNIX_OPTS_SYS_SETTRACE[@]}"
}

function ci_unix_settrace_run_tests {
    ci_unix_run_tests_helper "${CI_UNIX_OPTS_SYS_SETTRACE[@]}"
}

function ci_unix_settrace_stackless_build {
    make ${MAKEOPTS} -C mpy-cross
    make ${MAKEOPTS} -C ports/unix "${CI_UNIX_OPTS_SYS_SETTRACE_STACKLESS[@]}"
}

function ci_unix_settrace_stackless_run_tests {
    ci_unix_run_tests_helper "${CI_UNIX_OPTS_SYS_SETTRACE_STACKLESS[@]}"
}

function ci_unix_macos_build {
    make ${MAKEOPTS} -C mpy-cross
    make ${MAKEOPTS} -C ports/unix submodules
    #make ${MAKEOPTS} -C ports/unix deplibs
    make ${MAKEOPTS} -C ports/unix
    # check for additional compiler errors/warnings
    make ${MAKEOPTS} -C ports/unix VARIANT=dev submodules
    make ${MAKEOPTS} -C ports/unix VARIANT=dev
    make ${MAKEOPTS} -C ports/unix VARIANT=coverage submodules
    make ${MAKEOPTS} -C ports/unix VARIANT=coverage
}

function ci_unix_macos_run_tests {
    # Issues with macOS tests:
    # - OSX has poor time resolution and these uasyncio tests do not have correct output
    # - import_pkg7 has a problem with relative imports
    # - urandom_basic has a problem with getrandbits(0)
    (cd tests && ./run-tests.py --exclude 'uasyncio_(basic|heaplock|lock|wait_task)' --exclude 'import_pkg7.py' --exclude 'urandom_basic.py')
}

function ci_unix_qemu_mips_setup {
    sudo apt-get update
    sudo apt-get install gcc-mips-linux-gnu g++-mips-linux-gnu
    sudo apt-get install qemu-user
    qemu-mips --version
}

function ci_unix_qemu_mips_build {
    # qemu-mips on GitHub Actions will seg-fault if not linked statically
    ci_unix_build_helper "${CI_UNIX_OPTS_QEMU_MIPS[@]}"
}

function ci_unix_qemu_mips_run_tests {
    # Issues with MIPS tests:
    # - (i)listdir does not work, it always returns the empty list (it's an issue with the underlying C call)
    # - ffi tests do not work
    file ./ports/unix/micropython-coverage
    (cd tests && MICROPY_MICROPYTHON=../ports/unix/micropython-coverage ./run-tests.py --exclude 'vfs_posix.py' --exclude 'ffi_(callback|float|float2).py')
}

function ci_unix_qemu_arm_setup {
    sudo apt-get update
    sudo apt-get install gcc-arm-linux-gnueabi g++-arm-linux-gnueabi
    sudo apt-get install qemu-user
    qemu-arm --version
}

function ci_unix_qemu_arm_build {
    ci_unix_build_helper "${CI_UNIX_OPTS_QEMU_ARM[@]}"
    ci_unix_build_ffi_lib_helper arm-linux-gnueabi-gcc
}

function ci_unix_qemu_arm_run_tests {
    # Issues with ARM tests:
    # - (i)listdir does not work, it always returns the empty list (it's an issue with the underlying C call)
    export QEMU_LD_PREFIX=/usr/arm-linux-gnueabi
    file ./ports/unix/micropython-coverage
    (cd tests && MICROPY_MICROPYTHON=../ports/unix/micropython-coverage ./run-tests.py --exclude 'vfs_posix.py')
}

########################################################################################
# ports/windows

function ci_windows_setup {
    sudo apt-get install gcc-mingw-w64
}

function ci_windows_build {
    make ${MAKEOPTS} -C mpy-cross
    make ${MAKEOPTS} -C ports/windows CROSS_COMPILE=i686-w64-mingw32-
}
