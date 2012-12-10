Name:		flightgear
Version:	2.8.0
Release:	2
Summary:	The FlightGear Flight Simulator
License:	GPLv2
Group:		Games/Other
URL:		http://www.flightgear.org/

Source0:	ftp://ftp.flightgear.org/pub/fgfs/Source/%{name}-%{version}.tar.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png

BuildRequires:	cmake
BuildRequires:  git-core
BuildRequires:	plib-devel
BuildRequires:	subversion-devel
BuildRequires:	simgear-devel
BuildRequires:	pkgconfig(apr-1)
BuildRequires:	pkgconfig(freealut)
BuildRequires:  pkgconfig(glut)
BuildRequires:	pkgconfig(openscenegraph)
BuildRequires:	pkgconfig(openal)
BuildRequires:  pkgconfig(udev)
BuildRequires:  pkgconfig(xmu)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	boost-devel
Requires:	%{name}-data = %{version}

%description
The FlightGear project is working to create a sophisticated flight simulator
framework for the development and pursuit of interesting flight simulator
ideas. We are developing a solid basic sim that can be expanded and improved
upon by anyone interested in contributing.

%prep
%setup -q

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
CFLAGS="${CFLAGS:--O2 -g -frecord-gcc-switches -Wstrict-aliasing=2 -pipe \
    -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fstack-protector --param=ssp-buffer-size=4 -fPIC}"
export CFLAGS

CXXFLAGS="${CXXFLAGS:--O2 -g -frecord-gcc-switches -Wstrict-aliasing=2 \
    -pipe -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fstack-protector --param=ssp-buffer-size=4 -fPIC}"
export CXXFLAGS

FFLAGS="${FFLAGS:--O2 -g -frecord-gcc-switches -Wstrict-aliasing=2 -pipe \
    -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fstack-protector --param=ssp-buffer-size=4 -fPIC}"
export FFLAGS

#LDFLAGS="$LDFLAGS -Wl,--as-needed -Wl,--no-undefined -Wl,-z,relro -Wl,-O1 -Wl,--build-id -Wl,--enable-new-dtags"
#export LDFLAGS

mkdir -p build
cd build
cmake 	-DFG_DATA_DIR=%{_datadir}/%{name} \
	-DENABLE_TESTS:BOOL=OFF \
	-DCMAKE_INSTALL_PREFIX:PATH=/usr \
        -DCMAKE_INSTALL_LIBDIR:PATH=/usr/lib64 \
        -DINCLUDE_INSTALL_DIR:PATH=/usr/include \
        -DLIB_INSTALL_DIR:PATH=/usr/lib64 \
        -DSYSCONF_INSTALL_DIR:PATH=/etc \
        -DSHARE_INSTALL_PREFIX:PATH=/usr/share \
        -DCMAKE_BUILD_TYPE=release \
%if "lib64" == "lib64" 
        -DLIB_SUFFIX=64 \
%endif 
        -DCMAKE_SKIP_RPATH:BOOL=ON \
        -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
        -DBUILD_SHARED_LIBS:BOOL=ON \
        -DBUILD_STATIC_LIBS:BOOL=OFF \
        -DCMAKE_MODULE_LINKER_FLAGS="-Wl,--as-needed  -Wl,-z,relro -Wl,-O1 -Wl,--build-id -Wl,--enable-new-dtags" \
        ..
	
%make

%install
%makeinstall_std -C build

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
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

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

rm -rf %{buildroot}%{_docdir}/FlightGear

# remove obsolete utilities (taken from OBS)
cd %{buildroot}%{_bindir} && rm GPSsmooth MIDGsmooth UGsmooth metar

# copy libShivaVG from builddir
mkdir -p %{buildroot}/%{_libdir}
cp %{_builddir}/%{name}-%{version}/build/src/Canvas/ShivaVG/src/libShivaVG.so %{buildroot}/%{_libdir}

%files
%doc README AUTHORS docs-mini/
%{_datadir}/applications/%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man1/*
%{_bindir}/*
%{_libdir}/*.so

%changelog
* Mon Aug 20 2012 Anton Chernyshov <ach@rosalab.ru> 2.8.0-1
- New upstream release - 2.8.0
- Add some stuff from OBS spec
- Add new BuildRequires: libudev,git and subversion

* Fri Feb 24 2012 Andrey Bondrov <abondrov@mandriva.org> 2.6.0-1
+ Revision: 780067
- Add cmake to BuildRequires
- New version 2.6.0, switch to cmake and search game data in /usr/share/flightgear

* Sun Sep 18 2011 Andrey Bondrov <abondrov@mandriva.org> 2.4.0-1
+ Revision: 700207
- New version: 2.4.0

* Wed Jun 15 2011 Funda Wang <fwang@mandriva.org> 2.0.0-4
+ Revision: 685415
- rebuild

* Mon Apr 18 2011 Funda Wang <fwang@mandriva.org> 2.0.0-3
+ Revision: 655839
- rebuild

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-2mdv2011.0
+ Revision: 610711
- rebuild

* Sun Mar 07 2010 Frederik Himpe <fhimpe@mandriva.org> 2.0.0-1mdv2010.1
+ Revision: 515535
- Update to new version 2.0.0
- Remove gcc 4.4 patch: not needed anymore
- Remove unrecognized configure option
- Disable --as-needed ldflag because it breaks build

* Thu Aug 27 2009 Emmanuel Andry <eandry@mandriva.org> 1.9.1-3mdv2010.0
+ Revision: 421600
- add p1 to fix gcc44 build

* Sun Mar 22 2009 Frederik Himpe <fhimpe@mandriva.org> 1.9.1-2mdv2009.1
+ Revision: 360502
- Remove wrong patch attempting to fix build with Werror=format-security
  and disable this flag

* Tue Mar 03 2009 Frederik Himpe <fhimpe@mandriva.org> 1.9.1-1mdv2009.1
+ Revision: 348102
- Update to new version 1.9.1
- Add boost buildrequires
- Add patch fixing build with -Werror=format-security

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix no-buildroot-tag

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Thu Dec 20 2007 Andreas Hasenack <andreas@mandriva.com> 1.0.0-1mdv2008.1
+ Revision: 135970
- updated to version 1.0.0

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Sep 16 2007 Emmanuel Andry <eandry@mandriva.org> 0.9.10-6mdv2008.0
+ Revision: 88714
- drop old menu

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'


* Thu Apr 05 2007 Olivier Blin <oblin@mandriva.com> 0.9.10-5mdv2007.1
+ Revision: 150688
- buildrequire zlib-devel
- buildrequire freealut-devel (and link with it instead of old openal)

* Fri Dec 01 2006 Olivier Blin <oblin@mandriva.com> 0.9.10-4mdv2007.1
+ Revision: 89872
- split flightgear data out in flightgear-base

* Fri Dec 01 2006 Olivier Blin <oblin@mandriva.com> 0.9.10-3mdv2007.1
+ Revision: 89757
- fix menu entry
- Import flightgear

* Thu Aug 10 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.10-2mdv2007.0
- add xdg menu
- from Bertrand Coconnier <bcoconni@hotmail.com> :
	o Build for x86_64
	o Remove dependency

* Thu Apr 20 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.10-1mdk
- New release 0.9.10
- %%mkrel
- update menu section

* Mon Dec 05 2005 Olivier Blin <oblin@mandriva.com> 0.9.9-2mdk
- bump SimGear-devel BuildRequires (#20019)

* Mon Nov 21 2005 Lenny Cartier <lenny@mandriva.com> 0.9.9-1mdk
- 0.9.9

* Thu Jan 20 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.9.8-1mdk
- 0.9.8

* Thu Nov 04 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.9.6-2mdk
- flightgear is executable

* Tue Nov 02 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.9.6-1mdk
- 0.9.6

* Mon Aug 16 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.9.5-2mdk
- fix buildrequires
- fix path data files

* Fri Aug 06 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.9.5-1mdk
- 0.9.5

* Sun Jul 18 2004 Michael Scherer <misc@mandrake.org> 0.9.4-2mdk 
- rebuild for new gcc

* Wed Jun 02 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.9.4-1mdk
- 0.9.4
- fix buildrequires (lib64..)

