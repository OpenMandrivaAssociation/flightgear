%define	name	flightgear
%define	version	2.4.0
%define release	%mkrel 1
%define	Summary	The FlightGear Flight Simulator

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2
Group:		Games/Other
Source0:	ftp://ftp.flightgear.org/pub/fgfs/Source/%{name}-%{version}.tar.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png

BuildRequires:	plib-devel
BuildRequires:  libsimgear-devel
BuildRequires:  freealut-devel
BuildRequires:  openscenegraph-devel
BuildRequires:  openal-devel
BuildRequires:  zlib-devel
BuildRequires:	boost-devel

Requires:	%{name}-data = %{version}

URL:		http://www.flightgear.org/

%description
The FlightGear project is working to create a sophisticated flight simulator
framework for the development and pursuit of interesting flight simulator
ideas. We are developing a solid basic sim that can be expanded and improved
upon by anyone interested in contributing.

%prep
%setup -q

%build
%configure2_5x	--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir}
%make

%install
%makeinstall_std

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
Categories=Game;Simulation;
EOF

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

%files
%defattr(-,root,root)
%doc README AUTHORS docs-mini/
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man1/*
%{_gamesbindir}/*

