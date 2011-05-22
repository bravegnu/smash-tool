VER=$(shell python smash --version)

DESTDIR=build/debian
inject-version:
	sed -e "s/@VER@/$(VER)/" pkg/control.in > pkg/control
	sed -e "s/@VER@/$(VER)/" pkg/rpm.spec.in > pkg/rpm.spec

deb: inject-version install
	fakeroot chown -R root:root $(DESTDIR)/
	mkdir -p $(DESTDIR)/DEBIAN
	cp pkg/control $(DESTDIR)/DEBIAN
	mkdir -p dist
	fakeroot dpkg -b $(DESTDIR) dist/smash-$(VER).deb

sdist:
	python setup.py sdist

rpm: inject-version sdist
	rpmbuild -tb dist/smash-$(VER).tar.gz

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
