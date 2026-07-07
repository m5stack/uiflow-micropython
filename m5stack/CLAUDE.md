# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in the m5stack/ directory.

## Working Directory

You are in the `m5stack/` directory - the main MicroPython port for M5Stack devices. All build commands should be run from this directory.

## Quick Build Commands

```bash
# First-time setup
make submodules      # Clone dependencies
make patch           # Apply patches
make littlefs        # Build filesystem tools
make mpy-cross       # Build cross-compiler

# Build and flash (default board: M5STACK_AtomS3)
make flash_all

# Build for specific board
make BOARD=M5STACK_CoreS3 flash_all
make BOARD=M5STACK_Cardputer pack_all

# Development
make clean           # Clean build
make erase           # Erase flash
make monitor         # Serial monitor
make unpatch         # Remove patches
```

## Board Configuration

When adding or modifying board support:

1. **Board directory structure** (`boards/M5STACK_<Name>/`):
   - `board.json` - Hardware specs (display, buttons, sensors)
   - `mpconfigboard.h` - MicroPython feature flags
   - `mpconfigboard.cmake` - Build configuration
   - `sdkconfig.board` - ESP-IDF settings
   - `manifest.py` - Python modules to include
   - `files/system/` - Board-specific assets (images, fonts)

2. **Add to Makefile** - Update the `boards` list with mapping:
   ```makefile
   M5STACK_NewBoard:newboard
   ```

3. **Manifest includes** - Typical pattern:
   ```python
   include("$(MPY_DIR)/../m5stack/modules/startup/manifest_<board>.py")
   include("$(MPY_DIR)/../m5stack/libs/base/manifest.py")
   include("$(MPY_DIR)/../m5stack/libs/unit/manifest.py")
   ```

## Adding Python Libraries

Python libraries in `libs/` are frozen into firmware:

1. **Create module** in appropriate directory:
   - `libs/unit/` - Unit accessories
   - `libs/hat/` - HAT accessories
   - `libs/base/` - Base modules
   - `libs/hardware/` - Hardware APIs
   - `libs/driver/` - Device drivers

2. **Update manifest.py** in that directory:
   ```python
   package("unit", (
       "new_unit.py",
   ), base_path="..", opt=3)
   ```

3. **Add to board manifest** if not already included

## Adding C/C++ Modules

C modules in `cmodules/` provide native extensions:

1. **Create module directory** under `cmodules/`
2. **Add CMakeLists.txt** with:
   ```cmake
   add_library(usermod_<name> INTERFACE)
   target_sources(usermod_<name> INTERFACE ${CMAKE_CURRENT_LIST_DIR}/mod_<name>.c)
   target_include_directories(usermod_<name> INTERFACE ${CMAKE_CURRENT_LIST_DIR})
   target_link_libraries(usermod INTERFACE usermod_<name>)
   ```
3. **Register in** `cmodules/cmodules.cmake`

## M5Unified Component

The `components/M5Unified/` directory contains C++ bindings for hardware:

- **Pattern**: Each `mpy_m5*.cpp` file exposes hardware to MicroPython
- **Naming**: `mpy_m5<feature>.cpp` + `mpy_m5<feature>.h`
- **Registration**: Added to `mpy_m5unified.cpp` module dict

When modifying:
1. Update the C++ implementation
2. Ensure proper MicroPython object lifecycle (alloc/dealloc)
3. Use `mp_obj_t` for all Python-facing types
4. Register methods in the type's locals dict

## Patch System

Patches in `patches/` modify dependencies:

- `micropython/` - MicroPython core patches
- `esp-idf/` - ESP-IDF patches
- `M5Unified/` - M5Unified library patches
- `esp-adf/` - Audio framework patches
- `lv_binding_micropython/` - LVGL patches

**Workflow**:
```bash
make unpatch         # Remove all patches
# Make changes to submodules
make PKG=micropython update  # Generate new patch
make patch           # Reapply all patches
```

## Build Artifacts

- `build-<BOARD>/` - CMake build directory
- `build-<BOARD>/firmware.bin` - Main firmware
- `build-<BOARD>/bootloader.bin` - Bootloader
- `build-<BOARD>/partition_table.bin` - Partition table

## Common Issues

1. **"No rule to make target"** - Run `make submodules` first
2. **Patch conflicts** - Run `make unpatch` then `make patch`
3. **Build errors after git pull** - Clean and rebuild:
   ```bash
   make clean
   make patch
   make flash_all
   ```
4. **Board not found** - Check board name matches `boards/M5STACK_*/` exactly

## Code Style

- **C/C++**: Use `uncrustify` (config in `../tools/uncrustify.cfg`)
- **Python**: Use `black` and `ruff`
- **Format all**: `../tools/codeformat.py -v -c -f`

## Documentation

When adding new APIs, update documentation in `../docs/source/`:

1. Create `.rst` file following the template in `../docs/source/contribute/template.rst`
2. Structure: Title → Description → UiFlow2 Examples → MicroPython Examples → API
3. Use `.. autoclass::` and `.. py:method::` directives
4. Include code examples with `.. literalinclude::` or `.. code-block::`

## Testing

Before committing:
1. Build for at least one board: `make BOARD=M5STACK_AtomS3 flash_all`
2. Test on hardware if possible
3. Run code formatter: `../tools/codeformat.py -v -c -f`
4. Check documentation builds: `cd ../docs && make html`

## Commit Message Format

When committing changes in this directory, use prefixes without "m5stack/":

- `boards: Add Echo Pyramid support.`
- `libs/unit: Fix UnitV2 driver.`
- `components: Update M5Unified bindings.`
- `cmodules: Add camera module.`

Use the git-commit agent for proper formatting.
