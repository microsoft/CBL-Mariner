# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Toolkit Creation

######## TOOLKIT CREATION ########

# Toolkit Components
toolkit_component_extra_files = \
	$(PROJECT_ROOT)/CONTRIBUTING.md \
	$(PROJECT_ROOT)/LICENSES-AND-NOTICES/LICENSE.md \
	$(toolkit_root)/.gitignore

mariner_repos_dir = $(SPECS_DIR)/mariner-repos

# Outputs
toolkit_version   = $(RELEASE_VERSION)-$(build_arch)
toolkit_archive   = $(OUT_DIR)/toolkit-$(toolkit_version).tar.gz
toolkit_remove_archive = $(OUT_DIR)/toolkit-*.tar.gz
toolkit_build_dir = $(BUILD_DIR)/toolkit
toolkit_repos_dir = $(toolkit_build_dir)/repos
toolkit_tools_dir = $(toolkit_build_dir)/tools/toolkit_bins
toolkit_release_file = $(toolkit_build_dir)/version.txt

.PHONY: package-toolkit clean-package-toolkit

clean: clean-package-toolkit
clean-package-toolkit:
	rm -f $(toolkit_remove_archive)
	rm -rf $(toolkit_build_dir)

package-toolkit: go-tools
	rm -rf $(toolkit_build_dir) && \
	mkdir -p $(toolkit_build_dir) && \
	mkdir -p $(toolkit_repos_dir) && \
	mkdir -p $(toolkit_tools_dir) && \
	cp -r $(toolkit_root)/* $(toolkit_build_dir) && \
	cp $(mariner_repos_dir)/*.repo $(toolkit_repos_dir) && \
	cp $(toolkit_component_extra_files) $(toolkit_build_dir) && \
	cp $(go_tool_targets) $(toolkit_tools_dir) && \
	echo "$(toolkit_version)" > $(toolkit_release_file) && \
	rm -rf $(toolkit_build_dir)/out && \
	tar -I $(ARCHIVE_TOOL) -cvp -f $(toolkit_archive) -C $(toolkit_build_dir)/.. $(notdir $(toolkit_build_dir))

print-build-summary:
	sed -E -n 's:^.+level=info msg="Built \(([^\)]+)\) -> \[(.+)\].+$:\1\t\2:gp' $(LOGS_DIR)/pkggen/rpmbuilding/* | tee $(LOGS_DIR)/pkggen/build-summary.csv
