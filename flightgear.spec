%define _disable_ld_no_undefined 1
%define _disable_lto 1

Summary:	The FlightGear Flight Simulator
Name:		flightgear
Version:	3.4.0
Release:	2
License:	GPLv2+
Group:		Games/Other
Url:		http://www.flightgear.org/
Source0:	http://download.flightgear.org/flightgear/Source/%{name}-%{version}.tar.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch0:		flightgear-3.2.0-linkage.patch
Patch1:		0005-explicitely-link-with-libX11.patch
BuildRequires:	cmake
BuildRequires:	git-core
BuildRequires:	boost-devel
BuildRequires:	flite-devel
BuildRequires:	fltk-devel
BuildRequires:	gsm-devel
BuildRequires:	plib-devel
BuildRequires:	qt5-devel
BuildRequires:	subversion-devel
BuildRequires:	simgear-devel >= %{version}
BuildRequires:	pkgconfig(apr-1)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(freealut)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(openscenegraph)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(speexdsp)
BuildRequires:  pkgconfig(sqlite3)
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
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man1/*

#----------------------------------------------------------------------------

%prep
%setup -q
%apply_patches

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

%build
export CC=gcc
export CXX=g++
%cmake \
	-DFG_DATA_DIR=%{_datadir}/%{name} \
	-DJPEG_FACTORY:BOOL=ON \
	-DSYSTEM_SQLITE:BOOL=ON \
	-DSYSTEM_FLITE:BOOL=ON \
	-DSYSTEM_SPEEX=ON \
	-DSYSTEM_GSM=ON \
	-DBUILD_SHARED_LIBS=OFF \
	-DSIMGEAR_SHARED=ON

%make

%install
%makeinstall_std -C build

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Flight Gear
Name[ru]=Flight Gear
Comment=%{Summary}
Comment[ru]=Авиасимулятор Flight Gear
Exec=fgfs
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;Simulation;
EOF

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

rm -rf %{buildroot}%{_docdir}/FlightGear

# remove obsolete utilities (taken from OBS)
cd %{buildroot}%{_bindir} && rm GPSsmooth MIDGsmooth UGsmooth metar

