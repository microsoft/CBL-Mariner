# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Go Utilities
#	- Chroot Utilities

$(call create_folder,$(RPMS_DIR))
$(call create_folder,$(CACHED_RPMS_DIR)/cache)
$(call create_folder,$(TOOL_BINS_DIR))
$(call create_folder,$(BUILD_DIR)/tools)

######## GO TOOLS ########

# List of go utilities in tools/ directory
go_tool_list = \
	boilerplate \
	depsearch \
	grapher \
	graphpkgfetcher \
	graphanalytics \
	imageconfigvalidator \
	imagepkgfetcher \
	imager \
	isomaker \
	liveinstaller \
	pkgworker \
	roast \
	scheduler \
	specreader \
	srpmpacker \
	validatechroot \

# For each utility "util", create a "out/tools/util" target which references code in "tools/util/"
go_tool_targets = $(foreach target,$(go_tool_list),$(TOOL_BINS_DIR)/$(target))
# Common files to monitor for all go targets
go_module_files = $(TOOLS_DIR)/go.mod $(TOOLS_DIR)/go.sum
go_internal_files = $(shell find $(TOOLS_DIR)/internal/ -type f -name '*.go')
go_imagegen_files = $(shell find $(TOOLS_DIR)/imagegen/ -type f -name '*.go')
go_common_files = $(go_module_files) $(go_internal_files) $(go_imagegen_files) $(BUILD_DIR)/tools/internal.test_coverage
# A report on test coverage for all the go tools
test_coverage_report=$(TOOL_BINS_DIR)/test_coverage_report.html

# For each utility "util", create an alias variable "$(go-util)", and a target "go-util".
# Also add file dependencies for the various tools.
#	go-util=$(TOOL_BINS_DIR)/util
#	.PHONY: go-util
#	go-util: $(go-util)
#   $(TOOL_BINS_DIR)/util: $(TOOLS_DIR)/util/*.go
define go_util_rule
go-$(notdir $(tool))=$(tool)
.PHONY: go-$(notdir $(tool))
go-$(notdir $(tool)): $(tool)
$(tool): $(shell find $(TOOLS_DIR)/$(notdir $(tool))/ -type f -name '*.go')
endef
$(foreach tool,$(go_tool_targets),$(eval $(go_util_rule)))

.PHONY: go-tools clean-go-tools go-tidy-all go-test-coverage
go-tools: $(go_tool_targets)

clean: clean-go-tools
clean-go-tools:
	rm -rf $(TOOL_BINS_DIR)
	rm -rf $(BUILD_DIR)/tools

# Matching rules for the above targets
# Tool specific pre-requisites are tracked via $(go-util): $(shell find...) dynamic variable defined above
ifneq ($(REBUILD_TOOLS),y)
# SDK by default will ship with tool binaries pre-compiled (REBUILD_TOOLS=n), don't build them, just copy.
$(TOOL_BINS_DIR)/%:
	@if [ ! -f $@ ]; then \
		if [ -f $(TOOLKIT_BINS_DIR)/$(notdir $@) ]; then \
			echo "Restoring '$@' from '$(TOOLKIT_BINS_DIR)/$(notdir $@)'"; \
			cp $(TOOLKIT_BINS_DIR)/$(notdir $@) $@ ; \
		fi ; \
	fi && \
	[ -f $@ ] || $(call print_error,Unable to find tool $@. Set TOOL_BINS_DIR=.../ or set REBUILD_TOOLS=y ) ; \
	touch $@
else
# Rebuild the go tools as needed
$(TOOL_BINS_DIR)/%: $(go_common_files)
	cd $(TOOLS_DIR)/$* && \
		go test -covermode=atomic -coverprofile=$(BUILD_DIR)/tools/$*.test_coverage ./... && \
		go build -o $(TOOL_BINS_DIR)
endif

# Runs tests for common components
$(BUILD_DIR)/tools/internal.test_coverage: $(go_internal_files) $(go_imagegen_files)
	cd $(TOOLS_DIR)/$* && \
		go test -covermode=atomic -coverprofile=$@ ./...

# Return a list of all directories inside tools/ which contains a *.go file in
# the form of "go-fmt-<directory>"
go-tidy-all: go-mod-tidy go-fmt-all
# Updates the go module file
go-mod-tidy:
	rm -f $(TOOLS_DIR)/go.sum
	cd $(TOOLS_DIR) && go mod tidy
# Runs go fmt inside each matching directory
go-fmt-all:
	cd $(TOOLS_DIR) && go fmt ./...

# Formats the test coverage for the tools
.PHONY: $(BUILD_DIR)/tools/all_tools.coverage
$(BUILD_DIR)/tools/all_tools.coverage: $(shell find $(TOOLS_DIR)/ -type f -name '*.go')
	cd $(TOOLS_DIR) && go test -covermode=atomic -coverprofile=$@ ./...
$(test_coverage_report): $(BUILD_DIR)/tools/all_tools.coverage
	cd $(TOOLS_DIR) && go tool cover -html=$(BUILD_DIR)/tools/all_tools.coverage -o $@
go-test-coverage: $(test_coverage_report)
	@echo Coverage report available at: $(test_coverage_report)

######## CHROOT TOOLS ########

chroot_worker = $(BUILD_DIR)/worker/worker_chroot.tar.gz

.PHONY: chroot-tools clean-chroot-tools validate-chroot
chroot-tools: $(chroot_worker)

clean: clean-chroot-tools
clean-chroot-tools:
	rm -f $(chroot_worker)
	@echo Verifying no mountpoints present in $(BUILD_DIR)/worker/
	$(SCRIPTS_DIR)/safeunmount.sh "$(BUILD_DIR)/worker/" && \
	$(SCRIPTS_DIR)/safeunmount.sh "$(BUILD_DIR)/validatechroot/" && \
	rm -rf $(BUILD_DIR)/worker && \
	rm -rf $(BUILD_DIR)/validatechroot

# Worker chroot manifest is a file corresponding to the TOOLCHAIN_MANIFEST name.
toolchain_config_name=$(notdir $(TOOLCHAIN_MANIFEST))
worker_manifest_name=$(shell echo "$(toolchain_config_name)" | sed -E 's:^toolchain:pkggen_core:' )
worker_chroot_manifest = $(TOOLCHAIN_MANIFESTS_DIR)/$(worker_manifest_name)
#$(TOOLCHAIN_MANIFESTS_DIR)/pkggen_core_$(build_arch).txt
# Find the *.rpm corresponding to each of the entries in the manifest
# regex operation: (.*\.([^\.]+)\.rpm) extracts *.(<arch>).rpm" to determine
# the exact path of the required rpm
# Outputs: $(RPMS_DIR)/<arch>/<name>.<arch>.rpm
sed_regex_full_path = 's`(.*\.([^\.]+)\.rpm)`$(toolchain_rpms_dir)/\2/\1`p'
sed_regex_arch_only = 's`(.*\.([^\.]+)\.rpm)`\2`p'
worker_chroot_rpm_paths := $(shell sed -nr $(sed_regex_full_path) < $(worker_chroot_manifest))

worker_chroot_deps := \
	$(worker_chroot_manifest) \
	$(worker_chroot_rpm_paths) \
	$(toolchain_rpms) \
	$(PKGGEN_DIR)/worker/create_worker_chroot.sh

$(chroot_worker): $(worker_chroot_deps)
	$(PKGGEN_DIR)/worker/create_worker_chroot.sh $(BUILD_DIR)/worker $(worker_chroot_manifest) $(toolchain_rpms_dir) $(LOGS_DIR)

validate-chroot: $(go-validatechroot) $(chroot_worker)
	$(go-validatechroot) \
	--rpm-dir="$(toolchain_rpms_dir)" \
	--tmp-dir="$(BUILD_DIR)/validatechroot" \
	--worker-chroot="$(chroot_worker)" \
	--worker-manifest="$(worker_chroot_manifest)" \
	--log-file="$(LOGS_DIR)/worker/validate.log" \
	--log-level="$(LOG_LEVEL)"

######## MACRO TOOLS ########

macro_rpmrc = $(RPMRC_DIR)/rpmrc

macro_manifest = $(TOOLCHAIN_MANIFESTS_DIR)/macro_packages.txt

.PHONY: macro-tools clean-macro-tools
macro-tools: $(macro_rpmrc)

$(macro_rpmrc): $(toolchain_rpms)
	$(SCRIPTS_DIR)/preparemacros.sh $(MACRO_DIR) $(CACHED_RPMS_DIR)/cache $(macro_manifest)

clean: clean-macro-tools
clean-macro-tools:
	rm -rf $(MACRO_DIR)
