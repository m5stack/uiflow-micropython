# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# $(1) board type
# $(2) target dir
define base-files/install
	@cp ./fs/user/* $(2)/ -rf
	@ if [ -d ./fs/system/$(1) ]; then \
		cp ./fs/system/$(1) $(2)/res/ -rf ; \
	fi
	@cp ./fs/system/common/img/avatar.jpg $(2)/res/img/ -rf
endef


##
## $(1) TARGET_DIR
## $(2) PATCH_FILE
##
##
define Package/patche
	@echo "Push patch on $(1)" && \
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
	@echo "Pop on $(1)" && \
	file_name=$(shell basename $(2)) && \
	if [ -e $(1)/prereq_$$file_name ]; then \
		cd $(1) ; \
		git apply -R $(2) ; \
		rm $(1)/prereq_$$file_name ; \
		cd - ; \
	fi ;
endef