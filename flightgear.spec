%define	name	flightgear
%define	oname	FlightGear
%define	version	1.9.1
%define release	%mkrel 1
%define	Summary	The FlightGear Flight Simulator

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
Patch1:		FlightGear-1.9.1-string-fmt.patch
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
%patch1 -p1 -b .strfmt
./autogen.sh

rm -f docs-mini/*~

%build
%configure2_5x	--bindir=%{_gamesbindir} \
		--libdir=%{_gamesdatadir} \
		--datadir=%{_gamesdatadir} \
		--without-logging \
		--with-multiplayer
make

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall} bindir=$RPM_BUILD_ROOT%{_gamesbindir}

mkdir -p $RPM_BUILD_ROOT%_sbindir
cd utils
%{makeinstall}

install -m 755 js_server/js_server $RPM_BUILD_ROOT%_sbindir

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
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

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

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


