# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# $(1) board type
# $(2) target dir
define base-files/install
	@cp -rf ./fs/user/* $(2)/
	@if [ -d ./fs/system/$(1) ]; then \
		cp -rf ./fs/system/$(1) $(2)/res/;\
	fi
	@cp -rf ./fs/system/common/img/avatar.jpg $(2)/res/img/
endef

# $(1) source dir
# $(2) target dir
define system-files/install
	@if [ ! -e $(1) ]; then \
		echo "system-files/install: source not found, skip: $(1)"; \
	else \
		if [ ! -d $(2) ]; then \
			mkdir -p $(2); \
		fi; \
		if [ -d $(1) ]; then \
			cp -rf $(1)/* $(2)/; \
		elif [ -f $(1) ]; then \
			cp -f $(1) $(2)/; \
		fi; \
	fi
endef

##
## $(1): TARGET_DIR
## $(2): PATCH_SERIES (space-separated list)
##
define abs_path
	$(abspath $(MAKEFILE_DIR)patches/$(1))
endef

##
## Abort with an actionable message when the ESP-IDF environment has not
## been exported in the current shell (IDF_PATH unset or pointing nowhere).
##
## $(1): target name used in the hint (optional, defaults to "patch")
##
define require-idf-env
	@if [ -z "$(strip $(IDF_PATH))" ]; then \
		echo "" >&2; \
		echo "*** ESP-IDF environment is not active: IDF_PATH is not set." >&2; \
		echo "*** Run ESP-IDF's export.sh in this shell first:" >&2; \
		echo "***     . ./esp-idf/export.sh      (from the repository root)" >&2; \
		echo "***     . ../esp-idf/export.sh     (from m5stack/)" >&2; \
		echo "*** Then re-run 'make $(if $(strip $(1)),$(1),patch)'." >&2; \
		echo "*** Alternatively pass the path explicitly:" >&2; \
		echo "***     make IDF_PATH=/path/to/esp-idf $(if $(strip $(1)),$(1),patch)" >&2; \
		echo "" >&2; \
		exit 1; \
	fi; \
	if [ ! -d "$(IDF_PATH)" ]; then \
		echo "" >&2; \
		echo "*** ESP-IDF environment is invalid: IDF_PATH='$(IDF_PATH)' is not a directory." >&2; \
		echo "*** Re-run ESP-IDF's export.sh, or pass make IDF_PATH=/path/to/esp-idf $(if $(strip $(1)),$(1),patch)." >&2; \
		echo "" >&2; \
		exit 1; \
	fi
endef

##
## $(1): TARGET_DIR
## $(2): PATCH_SERIES (space-separated list)
##
define Patch/prepare
	$(if $(strip $(2)),\
	@test -n "$(strip $(1))" && test -d "$(1)" || { \
		echo "Patch/prepare: target directory not found: '$(1)'" >&2; \
		echo "Patch/prepare: run 'make submodules' first if this is a git submodule." >&2; \
		exit 1; \
	}
	@echo "Preparing $(1) ..."
	@(cd "$(1)" && { [ -e patches ] || mkdir patches; })
	@(cd "$(1)" && \
		quilt import $(foreach patch,$(2),$(call abs_path,$(patch))) && \
		cd - >/dev/null)
	@echo "Applying all patches in $(1) ..."
	@cd $(1) && quilt push -a && cd -
	,\
	@echo "No patches required for $(1); skipping.")
endef


##
## $(1): TARGET_DIR
## $(2): OUTPUT_DIR
##
##
define Patch/update
	@test -n "$(strip $(1))" && test -d "$(1)" || { \
		echo "Patch/update: target directory not found: '$(1)'" >&2; \
		echo "Patch/update: if this is a git submodule, run 'make submodules' first." >&2; \
		exit 1; \
	}
	@echo "Exporting patches from $(1) to $(2) ..."
	@mkdir -p $(2)
	@cd "$(1)" && \
	for p in `quilt series`; do \
		echo "Exporting $$p to $(2) ..." ; \
		cp $$p $(2) ; \
	done
endef


##
## $(1) TARGET_DIR
##
define Patch/clean
	@test -n "$(strip $(1))" && test -d "$(1)" || { \
		echo "Patch/clean: target directory not found: '$(1)'" >&2; \
		echo "Patch/clean: if this is a git submodule, run 'make submodules' first." >&2; \
		exit 1; \
	}
	@echo "Cleaning patch state in $(1) ..."
	@cd "$(1)" && \
		(quilt pop -a || true) && \
		rm -rf .pc patches
endef


##
## $(1) TARGET_DIR
## $(2) PATCH_FILE
##
##
define Package/patche
	@echo "Push $(2) on $(1)" && \
	file_name=$(shell basename $(2)) && \
	if [ ! -e $(1)/prereq_$$file_name ]; then \
		cd $(1) ; \
		git apply $(2) ; \
		touch $(1)/prereq_$$file_name ; \
		cd - ; \
	fi ;
endef

##
## $(1) TARGET_DIR
## $(2) PATCH_FILE
##
##
define Package/unpatche
	@echo "Pop $(2) on $(1)" && \
	file_name=$(shell basename $(2)) && \
	if [ -e $(1)/prereq_$$file_name ]; then \
		cd $(1) ; \
		git apply -R $(2) ; \
		rm $(1)/prereq_$$file_name ; \
		cd - ; \
	fi ;
endef
