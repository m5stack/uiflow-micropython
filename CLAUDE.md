# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the UIFlow MicroPython firmware repository for M5Stack devices. It's a custom MicroPython port built on ESP-IDF v5.4.2, providing hardware abstraction and device drivers for the M5Stack ecosystem of ESP32-based controllers, modules, units, and accessories.

## Build System

### Prerequisites Setup

```bash
mkdir uiflow_workspace && cd uiflow_workspace
git clone --depth 1 --branch v5.4.2 https://github.com/espressif/esp-idf.git
git -C esp-idf submodule update --init --recursive
./esp-idf/install.sh
. ./esp-idf/export.sh
```

### Building Firmware

All build commands are run from the `m5stack/` directory:

```bash
cd m5stack
make submodules      # Initialize git submodules
make patch           # Apply patches to dependencies
make littlefs        # Build littlefs filesystem tools
make mpy-cross       # Build MicroPython cross-compiler
make flash_all       # Build and flash firmware (default: M5STACK_AtomS3)
```

### Board-Specific Builds

Specify a board with `BOARD=<board_name>`:

```bash
make BOARD=M5STACK_CoreS3 pack_all
make BOARD=M5STACK_Cardputer flash_all
```

Board definitions are in `m5stack/boards/`. Each board has:
- `board.json` - Hardware configuration
- `mpconfigboard.h` - MicroPython config
- `mpconfigboard.cmake` - CMake config
- `sdkconfig.board` - ESP-IDF config
- `manifest.py` - Python module manifest
- `files/system/` - Board-specific assets

### Common Make Targets

- `make clean` - Clean build artifacts
- `make erase` - Erase flash
- `make monitor` - Open serial monitor
- `make pack_all` - Build firmware package
- `make unpatch` - Remove patches from dependencies

## Architecture

### Directory Structure

- **m5stack/** - Main firmware port
  - **boards/** - Board-specific configurations (40+ M5Stack devices)
  - **components/** - ESP-IDF components
    - **M5Unified/** - Core hardware abstraction (C++ bindings to MicroPython)
  - **cmodules/** - C/C++ MicroPython modules
    - **m5unified/** - M5Unified integration
    - **m5camera/** - Camera support
    - **m5audio2/** - Audio processing
    - **omv/** - OpenMV machine vision
    - **lv_binding_micropython/** - LVGL GUI bindings
  - **libs/** - Python libraries
    - **base/** - Base modules (displays, motors, etc.)
    - **unit/** - Unit accessories
    - **hat/** - HAT accessories
    - **chain/** - Chain accessories
    - **hardware/** - Hardware APIs (IMU, touch, etc.)
    - **driver/** - Device drivers
  - **modules/** - Core Python modules (boot, startup)
  - **patches/** - Patches for dependencies

- **docs/** - Sphinx documentation (reStructuredText)
- **examples/** - Example code organized by category
- **tools/** - Build and development tools
- **micropython/** - Upstream MicroPython (submodule)
- **esp-adf/** - ESP Audio Development Framework (submodule)
- **third-party/** - External dependencies

### Module System

The firmware uses a manifest-based module system. Each board's `manifest.py` includes:
- Startup scripts from `m5stack/modules/startup/`
- Libraries from `m5stack/libs/` (base, unit, hat, chain, etc.)
- Board-specific Python packages

Python modules in `m5stack/libs/` are frozen into firmware at build time.

### Hardware Abstraction

The M5Unified component (`m5stack/components/M5Unified/`) provides the core hardware abstraction:
- `mpy_m5unified.cpp` - Main M5 module
- `mpy_m5gfx.cpp` - Display/graphics
- `mpy_m5btn.cpp` - Buttons
- `mpy_m5imu.cpp` - IMU/accelerometer
- `mpy_m5spk.cpp` - Speaker
- `mpy_m5mic.cpp` - Microphone
- `mpy_m5power.cpp` - Power management
- `mpy_m5touch.cpp` - Touch screen
- `mpy_m5led.cpp` - RGB LED
- `mpy_m5als.cpp` - Ambient light sensor

## Development Workflow

### Code Formatting

Format code before committing:

```bash
tools/codeformat.py -v -c -f
```

This runs:
- `uncrustify` for C/C++ code
- `black` for Python code
- `ruff` for Python linting

### Testing

Run tests from the `tests/` directory (test infrastructure is minimal).

### Documentation

Documentation is built with Sphinx from `docs/source/`:

```bash
cd docs
make html
```

Documentation follows a strict structure (see `.github/prompts/docs.prompt.md`):
1. Title and description
2. UiFlow2 examples (visual block programming)
3. MicroPython examples
4. API reference (using Sphinx autodoc)

### Commit Messages

Use the git-commit agent (`.github/agents/git-commit.agent.md`) for standardized commits:
- Format: `<prefix>: <Capitalized description>.`
- Prefix based on changed directory (boards, libs/unit, docs, etc.)
- Max 72 characters
- Always include `-s` flag (Signed-off-by)

For changes in `m5stack/`, omit the "m5stack/" prefix:
- ✓ `boards: Add Core2 config.`
- ✗ `m5stack/boards: Add Core2 config.`

## Important Notes

- The working directory for builds is `m5stack/`, not the repository root
- ESP-IDF v5.4.2 is required (specified in workflows and README)
- Patches in `m5stack/patches/` are critical - apply with `make patch` before building
- The default board is M5STACK_AtomS3 if BOARD is not specified
- Documentation uses reStructuredText with specific formatting requirements
- All Python code in `m5stack/libs/` is frozen into firmware (not loaded from filesystem)

## Skills Available

- **uiflow2-coder** - UIFlow2 MicroPython coding with official API lookup
- **uiflow2-reviewer** - Review code against M5Stack source for API correctness
- **m5stack-assistant** - M5Stack product queries, specs, and technical support
