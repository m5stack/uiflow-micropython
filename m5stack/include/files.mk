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