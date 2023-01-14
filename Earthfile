# TODO: remove the dockerfile.
mingw-builder:
	FROM fedora:37
	RUN dnf -y install mingw32-pkg-config mingw32-gcc mingw32-gcc-c++ wget curl xz tar meson ninja-build git make rpm-build squashfs-tools ruby-devel \
				mingw32-gettext mingw32-libffi mingw32-zlib mingw32-pcre2 && dnf clean all
	# Just for now, while I debug this.
	RUN dnf -y install nano plocate
	RUN gem install fpm
	WORKDIR /build

glib-builder:
	FROM +mingw-builder
	RUN wget -O - https://download.gnome.org/sources/glib/2.75/glib-2.75.2.tar.xz | tar -Jxf -
	WORKDIR /build/glib-2.75.2
	COPY cross_file.txt cross_file.txt
	# The suffix is needed due to a bug in fedora's version of mingw. I'll report it someday.
	RUN meson setup --prefix "$(i686-w64-mingw32-gcc --print-sysroot)/mingw" --cross-file cross_file.txt builddir
	RUN meson compile -C builddir
	RUN DESTDIR=/install-prefix meson install -C builddir
	RUN fpm -s dir -t rpm -p /mingw32-glib2.rpm --name mingw32-glib2 --license lgpl2.1-or-later --architecture all --version 2.75.2 --provides 'mingw32(libglib-2.0-0.dll)' \
		--provides 'mingw32(libgobject-2.0-0.dll)' --provides 'mingw32(libgio-2.0-0.dll)' --provides 'mingw32(libgmodule-2.0-0.dll)' /install-prefix/=/
	SAVE ARTIFACT /mingw32-glib2.rpm

slirp-builder:
	FROM +mingw-builder
	COPY +glib-builder/mingw32-glib2.rpm /mingw32-glib2.rpm
	RUN dnf install -y /mingw32-glib2.rpm
	RUN wget -O - https://gitlab.freedesktop.org/slirp/libslirp/-/archive/v4.7.0/libslirp-v4.7.0.tar.gz | tar -xzf -
	WORKDIR /build/libslirp-v4.7.0
	COPY cross_file.txt cross_file.txt
	RUN meson setup --prefix "$(i686-w64-mingw32-gcc --print-sysroot)/mingw" --cross-file cross_file.txt builddir
	RUN meson compile -C builddir
	RUN DESTDIR=/install-prefix meson install -C builddir
	# TODO add provides
	RUN fpm -s dir -t rpm -p /mingw32-libslirp.rpm --name mingw32-libslirp --license other --architecture all --version 4.7.0.fc37 /install-prefix/=/
	SAVE ARTIFACT /mingw32-libslirp.rpm

qemu-builder:
	FROM +mingw-builder
	GIT CLONE --branch v7.2.0-win32-debug https://github.com/LindirQuenya/qemu.git /build/qemu
	WORKDIR /build/qemu/build
	# TODO: fix deps so that hexagon works.
	COPY +glib-builder/mingw32-glib2.rpm /mingw32-glib2.rpm
	COPY +slirp-builder/mingw32-libslirp.rpm /mingw32-libslirp.rpm
	RUN dnf install -y /mingw32-glib2.rpm mingw32-pixman /mingw32-libslirp.rpm iasl genisoimage gcc sparse
	RUN ../configure --cross-prefix=i686-w64-mingw32- --disable-docs --disable-guest-agent --disable-vnc --target-list=i386-softmmu --disable-cloop --disable-bochs \
			--disable-vdi --disable-dmg --disable-parallels --disable-qed --disable-vvfat --enable-slirp --disable-sdl --disable-bzip2 --disable-qcow1 \
			--disable-curl --disable-png --enable-pie --enable-lto --enable-membarrier --enable-sparse --enable-strip --prefix=/qemu
	RUN make
	RUN make install
	WORKDIR /qemu
	RUN cp "$(i686-w64-mingw32-gcc --print-sysroot)/mingw/bin/gspawn-win32-helper{,-console}.exe" /qemu/
	COPY copy_dlls.py copy_dlls.py
	RUN python3 copy_dlls.py qemu-system-i386.exe
	RUN zip -9r /qemu.zip *
	SAVE ARTIFACT /qemu.zip
