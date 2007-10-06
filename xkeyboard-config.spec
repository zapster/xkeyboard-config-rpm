# INFO: Package contains data-only, no binaries, so no debuginfo is needed
%define debug_package %{nil}

Summary: xkeyboard-config alternative xkb data files
Name: xkeyboard-config
Version: 1.1
Release: 3%{?dist}
License: MIT
Group: User Interface/X
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: http://xlibs.freedesktop.org/xkbdesc/%{name}-%{version}.tar.bz2
# https://bugs.freedesktop.org/show_bug.cgi?id=12719
Patch0: dellm65.patch

BuildArch: noarch

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros
BuildRequires: xkbcomp
BuildRequires: perl(XML::Parser)
#autoreconf needed for macbook patch
BuildRequires: automake intltool

# NOTE: Any packages that need xkbdata to be installed should be using
# the following "Requires: xkbdata" virtual provide, and not directly depending
# on the specific package name that the data is part of.  This ensures
# futureproofing of packaging in the event the package name changes, which
# has happened often.
Provides: xkbdata
# NOTE: We obsolete xorg-x11-xkbdata but currently intentionally do not
# virtual-provide it.  The idea is to find out which packages have a
# dependency on xorg-x11-xkbdata currently and fix them to require "xkbdata"
# instead.  Later, if this causes a problem, which seems unlikely, we can
# add a virtual provide for the old package name for compatibility, but
# hopefully everything is using the virtual name and we can avoid that.
Obsoletes: xorg-x11-xkbdata

%description
xkeyboard-config alternative xkb data files

%prep
%setup -q
%patch0 -p1 -b .dellm65

%build
%configure \
    --enable-compat-rules \
    --with-xkb-base=%{_datadir}/X11/xkb \
    --disable-xkbcomp-symlink \
    --with-xkb-rules-symlink=xorg

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
# Remove unnecessary symlink
rm -f $RPM_BUILD_ROOT%{_datadir}/X11/xkb/compiled

# Create filelist
{
   FILESLIST=${PWD}/files.list
   pushd $RPM_BUILD_ROOT
   find ./usr/share/X11 -type d | sed -e "s/^\./%dir /g" > $FILESLIST
   find ./usr/share/X11 -type f | sed -e "s/^\.//g" >> $FILESLIST
   popd
}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f files.list
%defattr(-,root,root,-)
%{_datadir}/X11/xkb/rules/xorg
%{_datadir}/X11/xkb/rules/xorg.lst
%{_datadir}/X11/xkb/rules/xorg.xml

%changelog
* Sat Oct  6 2007 Matthias Clasen <mclasen@redhat.com> - 1.1-3
- Somehow the Dell M65 model lost its vendor

* Wed Sep 26 2007 Matthias Clasen <mclasen@redhat.com> - 1.1-2
- Pick up the respun 1.1 release

* Wed Sep 26 2007 Matthias Clasen <mclasen@redhat.com> - 1.1-1
- Update to 1.1
- Drop upstreamed patches

* Wed Sep  5 2007 Matthias Clasen <mclasen@redhat.com> - 1.0-1
- Update to 1.0
- Drop upstreamed patches
- Update remaining patches

* Fri Sep  1 2006 Alexander Larsson <alexl@redhat.com> - 0.8-7
- Update macbook patch to be closer to what got in upstream
- (kp enter is ralt, not the option key)

* Fri Sep  1 2006 Matthias Clasen <mclasen@redhat.com> - 0.8-6
- Add support for Korean 106 key keyboards (204158)

* Tue Aug 29 2006 Alexander Larsson <alexl@redhat.com> - 0.8-5
- Add MacBook model and geometry, plus alt_win option

* Thu Aug 22 2006 Matthias Clasen <mclasen@redhat.com> 0.8-4
- Fix geometry description for Thinkpads
- Add a Kinesis model
- Add Dell Precision M65 geometry and model

* Tue Aug 22 2006 Adam Jackson <ajackson@redhat.com> 0.8-3
- Add Compose semantics to right Alt when that's ISO_Level3_Shift (#193922)

* Fri Jul 07 2006 Mike A. Harris <mharris@redhat.com> 0.8-2
- Rename spec file from xorg-x11-xkbdata to xkeyboard-config.spec

* Fri Jul 07 2006 Mike A. Harris <mharris@redhat.com> 0.8-1
- Renamed package from 'xorg-x11-xkbdata' to 'xkeyboard-config' to match the
  upstream project name and tarball.  I kept the rpm changelog intact however
  to preserve history, so all entries older than today, are from the
  prior 'xorg-x11-xkbdata' package.  (#196229,197939)
- Added "Obsoletes: xorg-x11-xkbdata"
- Removed 'pre' script from spec file, as that was a temporary hack to help
  transition from modular X.Org xkbdata to modular xkeyboard-config during
  FC5 development.  The issue it resolved is not present in any officially
  released distribution release or updates, so the hack is no longer needed.

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-8.xkbc0.8.0
- Embed xkeyboard-config version in Release field so we can tell from the
  filename what is really in this package without having to look in the
  spec file.  We should rename the package to xkeyboard-config and restart
  the versioning.

* Tue Jun 06 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-8
- Added "BuildRequires: perl(XML::Parser)" for (#194188)

* Sat Mar 04 2006 Ray Strode <rstrode@redhat.com> 1.0.1-7
- Update to 0.8.

* Wed Mar 01 2006 Ray Strode <rstrode@redhat.com> 1.0.1-6
- Turn on compat symlink (bug 183521)

* Tue Feb 28 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-5
- Fixed rpm pre script upgrade/install testing
- Rebuild package as 1.0.1-5 in rawhide, completing the transition to
  xkeyboard-config.

* Tue Feb 28 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-4.0.7.xkbcfg.5
- Added rpm pre script, to pre-remove the symbols/pc during package upgrades,
  to avoid an rpm cpio error if the X11R7.0 modular xkbdata package is already
  installed, because rpm can not replace a directory with a file.  

* Fri Feb 24 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-4.0.7.xkbcfg.1
- Package renamed to xorg-x11-xkbdata and version/release tweaked since it
  is too late to add new package names to Fedora Core 5 development.
- Added "Provides: xkeyboard-config" virtual provide.

* Fri Feb 24 2006 Mike A. Harris <mharris@redhat.com> 0.7-1
- Initial package created with xkeyboard-config-0.7.

* Tue Feb 21 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-3
- Added xkbdata-1.0.1-greek-fix-bug181313.patch to fix (#181313,181313)
- Added xkbdata-1.0.1-cz-fix-bug177362.patch to fix (#177362,178892)

* Thu Feb 09 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Added xkbdata-1.0.1-sysreq-fix-bug175661.patch to fix (#175661)

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated to xbitmaps 1.0.1 from X11R7.0

* Sat Dec 17 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated to xbitmaps 1.0.0 from X11R7 RC4.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Add a few missing rpm 'dir' directives to file manifest.
- Bump release, and build as a 'noarch' package.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated to xkbdata 0.99.1 from X11R7 RC2.
