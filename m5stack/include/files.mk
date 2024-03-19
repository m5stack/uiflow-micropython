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
