
# $(1) board type
# $(2) target dir
define base-files/install
	@cp ./fs/user/* $(2)/ -rf
	@cp ./fs/system/$(1) $(2)/res/ -rf
endef
