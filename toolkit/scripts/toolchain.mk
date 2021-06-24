# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Toolchain Bootstrapping

######## TOOLCHAIN BOOTSTRAPPING ########

$(call create_folder,$(RPMS_DIR)/$(build_arch))
$(call create_folder,$(RPMS_DIR)/noarch)
$(call create_folder,$(SRPMS_DIR))

toolchain_build_dir = $(BUILD_DIR)/toolchain
toolchain_local_temp = $(BUILD_DIR)/toolchain_temp
toolchain_logs_dir = $(LOGS_DIR)/toolchain
toolchain_downloads_logs_dir = $(toolchain_logs_dir)/downloads
toolchain_log_tail_length = 20
populated_toolchain_chroot = $(toolchain_build_dir)/populated_toolchain
toolchain_sources_dir = $(populated_toolchain_chroot)/usr/src/mariner/SOURCES
populated_toolchain_rpms = $(populated_toolchain_chroot)/usr/src/mariner/RPMS
toolchain_spec_list = $(toolchain_build_dir)/toolchain_specs.txt
raw_toolchain = $(toolchain_build_dir)/toolchain_from_container.tar.gz
final_toolchain = $(toolchain_build_dir)/toolchain_built_rpms_all.tar.gz
toolchain_files = \
	$(shell find $(SCRIPTS_DIR)/toolchain -name *.sh) \
	$(shell find $(SCRIPTS_DIR)/toolchain/SCRIPTS ) \
	$(SCRIPTS_DIR)/toolchain/container/Dockerfile

TOOLCHAIN_MANIFEST ?= $(TOOLCHAIN_MANIFESTS_DIR)/toolchain_$(build_arch).txt
# Find the *.rpm corresponding to each of the entries in the manifest
# regex operation: (.*\.([^\.]+)\.rpm) extracts *.(<arch>).rpm" to determine
# the exact path of the required rpm
# Outputs: $(toolchain_rpms_dir)/<arch>/<name>.<arch>.rpm
sed_regex_full_path = 's`(.*\.([^\.]+)\.rpm)`$(toolchain_rpms_dir)/\2/\1`p'
toolchain_rpms := $(shell sed -nr $(sed_regex_full_path) < $(TOOLCHAIN_MANIFEST))
toolchain_rpms_buildarch := $(shell grep $(build_arch) $(TOOLCHAIN_MANIFEST))
toolchain_rpms_noarch := $(shell grep noarch $(TOOLCHAIN_MANIFEST))

$(call create_folder,$(toolchain_build_dir))
$(call create_folder,$(toolchain_downloads_logs_dir))
$(call create_folder,$(populated_toolchain_chroot))

.PHONY: raw-toolchain toolchain clean-toolchain check-manifests check-aarch64-manifests check-x86_64-manifests
raw-toolchain: $(raw_toolchain)
toolchain: $(toolchain_rpms)

clean: clean-toolchain

clean-toolchain:
	rm -rf $(toolchain_build_dir)
	rm -rf $(toolchain_local_temp)
	rm -rf $(toolchain_logs_dir)
	rm -rf $(STATUS_FLAGS_DIR)/toolchain_local_temp.flag
	rm -f $(SCRIPTS_DIR)/toolchain/container/toolchain-local-wget-list
	rm -f $(SCRIPTS_DIR)/toolchain/container/texinfo-perl-fix.patch
	rm -f $(SCRIPTS_DIR)/toolchain/container/Awt_build_headless_only.patch
	rm -f $(SCRIPTS_DIR)/toolchain/container/check-system-ca-certs.patch
	rm -f $(SCRIPTS_DIR)/toolchain/container/rpm-define-RPM-LD-FLAGS.patch
	rm -f $(SCRIPTS_DIR)/toolchain/container/.bashrc

clean-toolchain-rpms:
	for f in $(toolchain_rpms_buildarch); do rm -vf $(RPMS_DIR)/$(build_arch)/$$f; done
	for f in $(toolchain_rpms_noarch); do rm -vf $(RPMS_DIR)/noarch/$$f; done

copy-toolchain-rpms:
	for f in $(toolchain_rpms_buildarch); do cp -vf $(toolchain_rpms_dir)/$(build_arch)/$$f $(RPMS_DIR)/$(build_arch); done
	for f in $(toolchain_rpms_noarch); do cp -vf $(toolchain_rpms_dir)/noarch/$$f $(RPMS_DIR)/noarch; done


# check that the manifest files only contain RPMs that could have been generated from toolchain specs.
check-manifests: check-x86_64-manifests check-aarch64-manifests
check-aarch64-manifests: $(toolchain_spec_list)
	cd $(SCRIPTS_DIR)/toolchain && \
		./check_manifests.sh \
			$(toolchain_spec_list) \
			$(SPECS_DIR) \
			$(TOOLCHAIN_MANIFESTS_DIR) \
			$(DIST_TAG) \
			aarch64
check-x86_64-manifests: $(toolchain_spec_list)
	cd $(SCRIPTS_DIR)/toolchain && \
		./check_manifests.sh \
			$(toolchain_spec_list) \
			$(SPECS_DIR) \
			$(TOOLCHAIN_MANIFESTS_DIR) \
			$(DIST_TAG) \
			x86_64

# Generate a list of a specs built as part of the toolchain.
$(toolchain_spec_list): $(toolchain_files)
	cd $(SCRIPTS_DIR)/toolchain && \
		./list_toolchain_specs.sh \
			$(SCRIPTS_DIR)/toolchain/build_official_toolchain_rpms.sh \
			$(toolchain_spec_list)

# To save toolchain artifacts use compress-toolchain and cache the tarballs
# To restore toolchain artifacts use hydrate-toolchain and give the location of the tarballs on the command-line
# sudo make compress-toolchain TOOLCHAIN_SOURCE_ARCHIVE=~/cache/toolchain_sources.tar.gz CACHE_DIR=~/cache
# sudo make hydrate-toolchain TOOLCHAIN_CONTAINER_ARCHIVE=~/cache/toolchain_from_container.tar.gz TOOLCHAIN_ARCHIVE=~/cache/toolchain_built_rpms_all.tar.gz TOOLCHAIN_SOURCE_ARCHIVE=~/cache/toolchain_source.tar.gz
compress-toolchain:
	tar -I $(ARCHIVE_TOOL) -cvp --exclude='SOURCES' -f $(raw_toolchain) -C $(toolchain_build_dir) populated_toolchain
	tar -I $(ARCHIVE_TOOL) -cvp -f $(final_toolchain) -C $(toolchain_build_dir) built_rpms_all
	$(if $(CACHE_DIR), cp $(raw_toolchain) $(final_toolchain) $(CACHE_DIR))

# After hydrating the toolchain run
# "sudo touch build/toolchain/toolchain_from_container.tar.gz" (should really check for existence of files in toolchain_*.txt)
# "sudo make toolchain REBUILD_TOOLCHAIN=y INCREMENTAL_TOOLCHAIN=y"
# Needs more testing before checkin
hydrate-toolchain:
	$(if $(TOOLCHAIN_CONTAINER_ARCHIVE),,$(error Must set TOOLCHAIN_CONTAINER_ARCHIVE=))
	$(if $(TOOLCHAIN_ARCHIVE),,$(error Must set TOOLCHAIN_ARCHIVE=))
	sudo mkdir -vp $(toolchain_build_dir)
	sudo cp $(TOOLCHAIN_CONTAINER_ARCHIVE) $(raw_toolchain)
	tar -I $(ARCHIVE_TOOL) -xf $(TOOLCHAIN_CONTAINER_ARCHIVE) -C $(toolchain_build_dir) --skip-old-files --touch --checkpoint=100000 --checkpoint-action=echo="%T"
	sudo cp $(TOOLCHAIN_ARCHIVE) $(final_toolchain)
	tar -I $(ARCHIVE_TOOL) -xf $(TOOLCHAIN_ARCHIVE) -C $(toolchain_build_dir) --skip-old-files --touch --checkpoint=100000 --checkpoint-action=echo="%T"
	sudo touch $(final_toolchain)
	sudo mkdir -vp $(RPMS_DIR)/noarch
	sudo mkdir -vp $(RPMS_DIR)/$(build_arch)
	sudo cp $(toolchain_build_dir)/built_rpms_all/*.noarch.rpm $(RPMS_DIR)/noarch
	sudo cp $(toolchain_build_dir)/built_rpms_all/*.$(build_arch).rpm $(RPMS_DIR)/$(build_arch)
	sudo find $(RPMS_DIR) -name '*.rpm' -exec sudo touch {} ';'
	sudo mkdir -vp $(populated_toolchain_rpms)/noarch
	sudo mkdir -vp $(populated_toolchain_rpms)/$(build_arch)
	sudo cp $(toolchain_build_dir)/built_rpms_all/*.$(build_arch).rpm $(populated_toolchain_rpms)/$(build_arch)
	sudo cp  $(toolchain_build_dir)/built_rpms_all/*.noarch.rpm $(populated_toolchain_rpms)/noarch
	sudo find $(populated_toolchain_rpms) -name '*.rpm' -exec sudo touch {} ';'
	sudo rm $(final_toolchain)
	sudo touch $(raw_toolchain)

# Output:
# out/toolchain/toolchain_from_container.tar.gz
$(raw_toolchain): $(toolchain_files)
	@echo "Building raw toolchain"
	cd $(SCRIPTS_DIR)/toolchain && \
		./create_toolchain_in_container.sh \
			$(BUILD_DIR) \
			$(SPECS_DIR) \
			$(SOURCE_URL)

# Always start with a fresh toolchain chroot when rebuilding toolchain RPMs
#
# Output:
# out/toolchain/built_rpms
# out/toolchain/toolchain_built_rpms.tar.gz
$(final_toolchain): $(raw_toolchain) $(STATUS_FLAGS_DIR)/build_toolchain_srpms.flag
	@echo "Building base packages"
	# Always clean the existing chroot
	$(if $(filter y,$(INCREMENTAL_TOOLCHAIN)),,rm -rf $(populated_toolchain_chroot))
	cd $(SCRIPTS_DIR)/toolchain && \
		./build_mariner_toolchain.sh \
			$(DIST_TAG) \
			$(BUILD_NUMBER) \
			$(RELEASE_VERSION) \
			$(BUILD_DIR) \
			$(RPMS_DIR) \
			$(SPECS_DIR) \
			$(RUN_CHECK) \
			$(TOOLCHAIN_MANIFESTS_DIR) \
			$(INCREMENTAL_TOOLCHAIN) \
			$(BUILD_SRPMS_DIR) \
			$(SRPMS_DIR) && \
	mkdir -p $(RPMS_DIR)/noarch && \
	mkdir -p $(RPMS_DIR)/$(build_arch) && \
	cp -v $(toolchain_build_dir)/built_rpms_all/*noarch.rpm $(RPMS_DIR)/noarch && \
	cp -v $(toolchain_build_dir)/built_rpms_all/*$(build_arch).rpm $(RPMS_DIR)/$(build_arch)
	$(if $(filter y,$(UPDATE_TOOLCHAIN_LIST)), ls -1 $(toolchain_build_dir)/built_rpms_all > $(MANIFESTS_DIR)/package/toolchain_$(build_arch).txt)
	touch $@

.SILENT: $(toolchain_rpms)

ifeq ($(REBUILD_TOOLCHAIN),y)
# The basic set of RPMs can always be produced by bootstrapping the toolchain.
# Try to skip extracting individual RPMS if the toolchain step has already placed
# them into the RPM folder.
$(toolchain_rpms): $(TOOLCHAIN_MANIFEST) | $(final_toolchain)
	@echo Extracting RPM $@ from toolchain && \
	if [ ! -f $@ -o $(final_toolchain) -nt $@ ]; then \
		mkdir -p $(dir $@) && \
		tar -I $(ARCHIVE_TOOL) -xvf $(final_toolchain) -C $(dir $@) --strip-components 1 built_rpms_all/$(notdir $@) && \
		touch $@ ; \
	fi || $(call print_error, $@ failed) ;
else
ifneq (,$(TOOLCHAIN_ARCHIVE))
# Extract a set of RPMS from an archive instead of building them from scratch.
$(toolchain_local_temp): $(STATUS_FLAGS_DIR)/toolchain_local_temp.flag
	@touch $@

$(toolchain_local_temp)%: ;
$(STATUS_FLAGS_DIR)/toolchain_local_temp.flag: $(TOOLCHAIN_ARCHIVE) $(shell find $(toolchain_local_temp)/* 2>/dev/null)
	mkdir -p $(BUILD_DIR)/toolchain_temp/ && \
	tar -I $(ARCHIVE_TOOL) -xvf $(TOOLCHAIN_ARCHIVE) -C $(BUILD_DIR)/toolchain_temp/ --strip-components 1 && \
	touch $(BUILD_DIR)/toolchain_temp/* && \
	touch $@

$(toolchain_rpms): $(TOOLCHAIN_MANIFEST) $(toolchain_local_temp)
	tempFile=$(toolchain_local_temp)/$(notdir $@) && \
	if [ ! -f $@ -o $(TOOLCHAIN_ARCHIVE) -nt $@ ]; then \
		echo Extracting RPM $@ from toolchain && \
		mkdir -p $(dir $@) && \
		mv $$tempFile $(dir $@) && \
		touch $@ ; \
	fi || $(call print_error, $@ failed) && \
	touch $@
else
# Download from online package server
$(toolchain_rpms):
	rpm_filename="$(notdir $@)" && \
	rpm_dir="$(dir $@)" && \
	log_file="$(toolchain_downloads_logs_dir)/$$rpm_filename.log" && \
	echo "Downloading toolchain RPM: $$rpm_filename" | tee "$$log_file" && \
	mkdir -p $$rpm_dir && \
	cd $$rpm_dir && \
	for url in $(PACKAGE_URL_LIST); do \
		wget $$url/$$rpm_filename \
			$(if $(TLS_CERT),--certificate=$(TLS_CERT)) \
			$(if $(TLS_KEY),--private-key=$(TLS_KEY)) \
			-a $$log_file && \
		echo "Downloaded toolchain RPM: $$rpm_filename" >> $$log_file && \
		break; \
	done || { \
		echo "\nERROR: Failed to download toolchain package: $$rpm_filename." && \
		echo "ERROR: Last $(toolchain_log_tail_length) lines from log '$$log_file':\n" && \
		tail -n$(toolchain_log_tail_length) $$log_file | sed 's/^/\t/' && \
		$(call print_error,\nToolchain download failed. See above errors for more details.) \
	}
endif
endif
