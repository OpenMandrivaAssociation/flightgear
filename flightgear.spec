Name:		flightgear
Version:	2.6.0
Release:	%mkrel 1
Summary:	The FlightGear Flight Simulator
License:	GPLv2
Group:		Games/Other
URL:		http://www.flightgear.org/
Source0:	ftp://ftp.flightgear.org/pub/fgfs/Source/%{name}-%{version}.tar.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch0:		flightgear-2.6.0-linkage.patch
BuildRequires:	plib-devel
BuildRequires:	simgear-devel
BuildRequires:	freealut-devel
BuildRequires:	openscenegraph-devel
BuildRequires:	openal-devel
BuildRequires:	zlib-devel
BuildRequires:	boost-devel
Requires:	%{name}-data = %{version}

%description
The FlightGear project is working to create a sophisticated flight simulator
framework for the development and pursuit of interesting flight simulator
ideas. We are developing a solid basic sim that can be expanded and improved
upon by anyone interested in contributing.

%prep
%setup -q
%patch0 -p1

%build
%cmake -DFG_DATA_DIR=%{_datadir}/%{name}
%make

%install
%__rm -rf %{buildroot}
%makeinstall_std -C build

%__mkdir_p %{buildroot}%{_datadir}/applications
%__cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Flight Gear
Comment=%{Summary}
Exec=fgfs
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;Simulation;
EOF

%__install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
%__install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
%__install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

%__rm -rf %{buildroot}%{_docdir}/FlightGear

%clean
%__rm -rf %{buildroot}

%files
%doc README AUTHORS docs-mini/
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man1/*
%{_bindir}/*

