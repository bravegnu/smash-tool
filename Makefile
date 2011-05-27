VER=$(shell python smash --version)

DESTDIR=build/debian
inject-version:
	sed -e "s/@VER@/$(VER)/" pkg/control.in > pkg/control
	sed -e "s/@VER@/$(VER)/" pkg/rpm.spec.in > pkg/rpm.spec

# We invoke sdist here so that setup.py can create the python modules
# for the resource files
deb: sdist inject-version install
	fakeroot chown -R root:root $(DESTDIR)/
	mkdir -p $(DESTDIR)/DEBIAN
	cp pkg/control $(DESTDIR)/DEBIAN
	mkdir -p dist
	fakeroot dpkg -b $(DESTDIR) dist/smash-$(VER).deb

sdist:
	python setup.py sdist

rpm: sdist
	mkdir -p build/rpm/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
	cp pkg/rpm.spec build/rpm/SPECS
	cp dist/smash-$(VER).tar.gz build/rpm/SOURCES
	rpmbuild --define "_topdir $$(pwd)/build/rpm" -bb build/rpm/SPECS/rpm.spec
	cp build/rpm/RPMS/noarch/smash-$(VER)-1.noarch.rpm dist/

install: BIN=$(DESTDIR)/usr/bin
install: APP=$(DESTDIR)/usr/share/smash
install:
	mkdir -p $(BIN)
	mkdir -p $(APP)
	mkdir -p $(APP)/smashlib
	mkdir -p $(APP)/smashlib/resources

	cp smash smash-gui $(BIN)
	chmod +x $(BIN)/smash
	chmod +x $(BIN)/smash-gui
	cp smashlib/*.py $(APP)/smashlib
	cp smashlib/resources/*.py $(APP)/smashlib/resources
