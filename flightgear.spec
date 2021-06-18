Summary:	The FlightGear Flight Simulator
Name:		flightgear
Version:	2020.3.9
Release:	1
License:	GPLv2+
Group:		Games/Other
Url:		http://www.flightgear.org/
Source0: https://sourceforge.net/projects/flightgear/files/release-2020.3/%{name}-%{version}.tar.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Source14:	%{name}.64.png
Source15:	%{name}.128.png

Patch0:		flightgear-2020.3.5-fix-build-openmandriva.patch
Patch1:		flightgear-2020.3.6-non-x86.patch

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(SimGear) >= %{version}
BuildRequires:	cmake(Qt5Qml)
BuildRequires:	cmake(Qt5QuickWidgets)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	cmake(Qt5LinguistTools)
BuildRequires:	qt5-linguist
BuildRequires:	curl-devel
BuildRequires:	git-core
BuildRequires:	boost-devel
BuildRequires:	flite-devel
BuildRequires:	fltk-devel
BuildRequires:	glew-devel
BuildRequires:	gsm-devel
BuildRequires:	plib-devel
BuildRequires:	qt5-devel
BuildRequires:	subversion-devel
BuildRequires:	pkgconfig(apr-1)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(freealut)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(openscenegraph)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(speexdsp)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(zlib)
Requires:	%{name}-data = %{version}
Requires:	openscenegraph-plugins

%description
The FlightGear project is working to create a sophisticated flight simulator
framework for the development and pursuit of interesting flight simulator
ideas. We are developing a solid basic sim that can be expanded and improved
upon by anyone interested in contributing.

%files
%doc README AUTHORS docs-mini/
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/org.flightgear.FlightGear.desktop
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/22x22/apps/%{name}.png
%{_iconsdir}/hicolor/24x24/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/64x64/apps/%{name}.png
%{_iconsdir}/hicolor/128x128/apps/%{name}.png
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/it/man1/*
%{_mandir}/it/man5/*
%{_datadir}/bash-completion/completions/fgfs
%{_datadir}/zsh/site-functions/_fgfs
%{_datadir}/metainfo/org.flightgear.FlightGear.metainfo.xml

#----------------------------------------------------------------------------

%prep
%autosetup -p1

# Taken from OBS
for f in docs-mini/README.xmlparticles Thanks
do
    iconv -f iso-8859-1 -t utf-8 -o ${f}.utf8 ${f}
    mv -f ${f}.utf8 ${f}
done
sed -i 's/\r//' docs-mini/AptNavFAQ.FlightGear.html

# remove some unneeded doc files
for ext in Cygwin IRIX Joystick Linux MSVC MSVC8 MacOS SimGear Unix Win32-X autoconf mingw plib src xmlsyntax; do
    rm -f docs-mini/README.${ext}
done

%cmake \
	-G Ninja \
	-DFG_DATA_DIR=%{_datadir}/%{name} \
	-DJPEG_FACTORY:BOOL=ON \
	-DSYSTEM_SQLITE:BOOL=ON \
	-DSYSTEM_FLITE:BOOL=ON \
	-DSYSTEM_SPEEX=ON \
	-DSYSTEM_GSM=ON \
	-DBUILD_SHARED_LIBS=OFF \
	-DSIMGEAR_SHARED=ON

%build
%ninja_build -C build

%install
%ninja_install -C build

mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_iconsdir}/hicolor/16x16/apps
mkdir -p %{buildroot}%{_iconsdir}/hicolor/32x32/apps
mkdir -p %{buildroot}%{_iconsdir}/hicolor/48x48/apps
mkdir -p %{buildroot}%{_iconsdir}/hicolor/64x64/apps
mkdir -p %{buildroot}%{_iconsdir}/hicolor/128x128/apps
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Flight Gear
Name[ru]=Flight Gear
Comment=Flight Gear
Comment[ru]=Авиасимулятор Flight Gear
Exec=fgfs
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;Simulation;
EOF

#install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m644 %{SOURCE14} -D %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
install -m644 %{SOURCE15} -D %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png
#install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

rm -rf %{buildroot}%{_docdir}/FlightGear

# remove obsolete utilities (taken from OBS)
cd %{buildroot}%{_bindir} && rm GPSsmooth MIDGsmooth UGsmooth metar

