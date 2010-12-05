%define	name	flightgear
%define	oname	FlightGear
%define	version	2.0.0
%define release	%mkrel 2
%define	Summary	The FlightGear Flight Simulator

%define _disable_ld_as_needed 1
%define Werror_cflags %nil

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Games/Other
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0:	ftp://ftp.flightgear.org/pub/fgfs/Source/%{oname}-%{version}.tar.gz
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch0:		FlightGear-0.9.10-fix-x86_64.patch
BuildRequires:	plib-devel >= 1.8.4 SimGear-devel >= 1.9.1 mesa-common-devel freealut-devel openal-devel zlib-devel
BuildRequires:	boost-devel
Requires:	flightgear-base
URL:		http://www.flightgear.org/
Obsoletes:	%{oname}
Provides:	%{oname} = %{version}-%{release}

%description
The Flight Gear project is working to create a sophisticated flight simulator
framework for the development and pursuit of interesting flight simulator
ideas. We are developing a solid basic sim that can be expanded and improved
upon by anyone interested in contributing.

%prep
%setup -q -n %{oname}-%{version}
%patch0 -p1
./autogen.sh

rm -f docs-mini/*~

%build
%configure2_5x	--bindir=%{_gamesbindir} \
		--libdir=%{_gamesdatadir} \
		--datadir=%{_gamesdatadir} \
		--without-logging 
make

%install
rm -rf %{buildroot}
%{makeinstall} bindir=%{buildroot}%{_gamesbindir}

mkdir -p %{buildroot}%_sbindir
cd utils
%{makeinstall}

install -m 755 js_server/js_server %{buildroot}%_sbindir

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Flight Gear
Comment=%{Summary}
Exec=%{_gamesbindir}/fgfs
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;Simulation
EOF

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README AUTHORS docs-mini/
%{_bindir}/*
%{_sbindir}/js_server
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man1/*
%defattr(-,root,root,755)
%{_gamesbindir}/*
%defattr(644,root,root,755)


