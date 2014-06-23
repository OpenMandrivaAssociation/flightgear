%define _disable_ld_no_undefined 1

Name:		flightgear
Version:	3.0.0
Release:	2
Summary:	The FlightGear Flight Simulator
License:	GPLv2
Group:		Games/Other
URL:		http://www.flightgear.org/

Source0:	ftp://ftp.flightgear.org/pub/fgfs/Source/%{name}-%{version}.tar.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png

Patch0:		flightgear-2.6.0-mandriva-linkage.patch

BuildRequires:	cmake
BuildRequires:	git-core
BuildRequires:	boost-devel
BuildRequires:	fltk-devel
BuildRequires:	plib-devel
BuildRequires:	subversion-devel
BuildRequires:	simgear-devel >= %{version}
BuildRequires:	pkgconfig(apr-1)
BuildRequires:	pkgconfig(freealut)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(openscenegraph)
BuildRequires:	pkgconfig(openal)
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

%prep
%setup -q
%patch0 -p1

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
%cmake \
	-DFG_DATA_DIR=%{_datadir}/%{name} \
	-DJPEG_FACTORY:BOOL=ON -DSYSTEM_SQLITE:BOOL=ON

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

%files
%doc README AUTHORS docs-mini/
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man1/*

