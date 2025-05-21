# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# $(1) board type
# $(2) target dir
define base-files/install
	@cp -rf ./fs/user/* $(2)/
	@ if [ -d ./fs/system/$(1) ]; then \
		cp -rf ./fs/system/$(1) $(2)/res/;\
	fi
	@cp -rf ./fs/system/common/img/avatar.jpg $(2)/res/img/
endef


##
## $(1): TARGET_DIR
## $(2): PATCH_SERIES (space-separated list)
##
define abs_path
	$(abspath $(CURDIR)/patches/$(1))
endef

##
## $(1): TARGET_DIR
## $(2): PATCH_SERIES (space-separated list)
##
define Patch/prepare
	@echo "Preparing $(1) ..."
	@(cd $(1) && [ -e patches ] || mkdir patches)
	@(cd $(1) && \
		quilt import $(foreach patch,$(2),$(call abs_path,$(patch))) && \
		cd - >/dev/null)
	@echo "Applying all patches in $(1) ..."
	@cd $(1) && quilt push -a && cd -
endef


##
## $(1): TARGET_DIR
## $(2): OUTPUT_DIR
##
##
define Patch/update
	@echo "Exporting patches from $(1) to $(2) ..."
	@mkdir -p $(2)
	@cd $(1) && \
	for p in `quilt series`; do \
		echo "Exporting $$p to $(2) ..." ; \
		cp $$p $(2) ; \
	done
endef


##
## $(1) TARGET_DIR
##
define Patch/clean
	@echo "Cleaning patch state in $(1) ..."
	@cd $(1) && \
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