PACKAGE=install-overwatch
VERSION=1.0
BUILD_DIR=$(CURDIR)/$(PACKAGE)
DEB_FILE=$(PACKAGE)_$(VERSION)_all.deb

.PHONY: all clean build install

all: build

build:
	dpkg-deb --build $(PACKAGE)
	mv $(PACKAGE).deb $(DEB_FILE)
	@echo "Built $(DEB_FILE)"

install: build
	sudo dpkg -i $(DEB_FILE)
	sudo systemctl daemon-reload
	sudo systemctl enable --now install_overwatch-init.service
	@echo "Installed and started install_overwatch"

clean:
	rm -f $(DEB_FILE)
