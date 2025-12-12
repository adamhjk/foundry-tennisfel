.PHONY: all clean release test help

VERSION := $(shell jq -r .version module.json)
MODULE_NAME := tennisfel
ZIP_NAME := v$(VERSION).zip

help:
	@echo "Tennisfel Foundry Module - Build Targets"
	@echo "========================================"
	@echo "  make all      - Run conversion script"
	@echo "  make release  - Create release zip package"
	@echo "  make clean    - Remove build artifacts"
	@echo "  make test     - Verify release package"
	@echo "  make help     - Show this help message"

all:
	@echo "Running conversion script..."
	python3 convert.py

release: clean all
	@echo "Creating release package: $(ZIP_NAME)"
	@mkdir -p $(MODULE_NAME)-v$(VERSION)
	@cp module.json $(MODULE_NAME)-v$(VERSION)/
	@cp README.md $(MODULE_NAME)-v$(VERSION)/
	@cp -r packs $(MODULE_NAME)-v$(VERSION)/
	@cp -r assets $(MODULE_NAME)-v$(VERSION)/
	@zip -r $(ZIP_NAME) $(MODULE_NAME)-v$(VERSION)
	@rm -rf $(MODULE_NAME)-v$(VERSION)
	@echo "Release created: $(ZIP_NAME)"

clean:
	@echo "Cleaning build artifacts..."
	@rm -rf packs/*.db
	@rm -rf assets/images assets/banners assets/portraits assets/maps
	@rm -f v*.zip
	@rm -rf $(MODULE_NAME)-v*
	@echo "Clean complete"

test: release
	@echo "Testing release package..."
	@unzip -t $(ZIP_NAME)
	@echo "Archive structure:"
	@unzip -l $(ZIP_NAME)
