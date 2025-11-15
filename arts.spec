#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg arts
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_sbindir %{tde_prefix}/sbin
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.5.10
Release:	%{?tde_version}_%{?!preversion:3}%{?preversion:0_%{preversion}}%{?dist}
Summary:	ARTS (analog realtime synthesizer) - the TDE sound system
Group:		System Environment/Daemons 
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Project
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz
Source1:	%{name}-rpmlintrc

BuildRequires:    cmake make

BuildRequires:	libtqt4-devel >= %{tde_epoch}:4.2.0
BuildRequires:	trinity-filesystem >= %{tde_version}
Requires:		trinity-filesystem >= %{tde_version}

BuildRequires:	trinity-tde-cmake >= %{tde_version}
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(audiofile)

BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gsl)

# VORBIS support
BuildRequires:  pkgconfig(vorbis)

# ALSA support
BuildRequires:  pkgconfig(alsa)


# ESOUND support
#define with_esound 0
# %if 0%{?with_esound}
# BuildRequires:  pkgconfig(esound)
# %endif

# JACK support
%define with_jack 1
%if 0%{?with_jack}
BuildRequires:  pkgconfig(jack)
%endif

# LIBTOOL
BuildRequires:  libtool-devel

# MAD support
%define with_mad 1
%if 0%{?with_mad}
BuildRequires:  pkgconfig(mad)
%endif

# Pulseaudio config file
%if 0%{?mgaversion} || 0%{?mdkversion} || 0%{?rhel} >= 6 || 0%{?fedora} || 0%{?suse_version}
%define with_pulseaudio 1
%endif

Requires:		libtqt4 >= %{tde_epoch}:4.2.0
#Requires:		audiofile

%if "%{?tde_prefix}" == "/usr"
Obsoletes:	arts < %{?epoch:%{epoch}:}%{version}-%{release}
%endif

%description
arts (analog real-time synthesizer) is the sound system of TDE.

The principle of arts is to create/process sound using small modules which do
certain tasks. These may be create a waveform (oscillators), play samples,
filter data, add signals, perform effects like delay/flanger/chorus, or
output the data to the soundcard.

By connecting all those small modules together, you can perform complex
tasks like simulating a mixer, generating an instrument or things like
playing a wave file with some effects.

%files
%defattr(-,root,root,-)
%doc COPYING.LIB
%dir %{tde_libdir}/mcop
%dir %{tde_libdir}/mcop/Arts
%{tde_libdir}/mcop/Arts/*
%{tde_libdir}/mcop/*.mcopclass
%{tde_libdir}/mcop/*.mcoptype
%{tde_libdir}/lib*.so.*
%{tde_bindir}/artscat
%{tde_bindir}/artsd
%{tde_bindir}/artsdsp
%{tde_bindir}/artsplay
%{tde_bindir}/artsrec
%{tde_bindir}/artsshell
%{tde_bindir}/artswrapper
# The '.la' files are needed for runtime, not devel !
%{tde_libdir}/lib*.la
%{tde_mandir}/man1/artsc-config-trinity.1*
%{tde_mandir}/man1/artscat-trinity.1*
%{tde_mandir}/man1/artsdsp-trinity.1*

##########

%package devel
Group:		Development/Libraries
Summary:	ARTS (analog realtime synthesizer) - the TDE sound system (Development files)
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%if "%{?tde_prefix}" == "/usr"
Obsoletes:	arts-devel < %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Requires:	pkgconfig(alsa)
Requires:	pkgconfig(audiofile)
Requires:  pkgconfig(vorbis)
#Requires:  pkgconfig(esound)
Requires:  pkgconfig(mad)
Requires:  pkgconfig(jack)

%description devel
arts (analog real-time synthesizer) is the sound system of TDE.

The principle of arts is to create/process sound using small modules which do
certain tasks. These may be create a waveform (oscillators), play samples,
filter data, add signals, perform effects like delay/flanger/chorus, or
output the data to the soundcard.

By connecting all those small modules together, you can perform complex
tasks like simulating a mixer, generating an instrument or things like
playing a wave file with some effects.

%files devel
%defattr(-,root,root,-)
%{tde_bindir}/mcopidl
# Arts includes are under 'tde' - this is on purpose !
%{tde_tdeincludedir}/arts/
# Artsc includes are not under 'tde'.
%{tde_includedir}/artsc/
%{tde_bindir}/artsc-config
%{tde_libdir}/lib*.so
%{tde_libdir}/pkgconfig/*.pc
%{tde_libdir}/*.a

%if 0%{?with_pulseaudio}
%package config-pulseaudio
Group:		System Environment/Daemons
Summary:	ARTS - Default configuration file for Pulseaudio
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description config-pulseaudio
This package contains a default ARTS configuration file, that is 
intended for systems running the Pulseaudio server.

%files config-pulseaudio
%defattr(-,root,root,-)
%config %{tde_confdir}/kcmartsrc
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_NO_BUILTIN_CHRPATH=ON \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=ON \
  \
  -DCMAKE_INSTALL_PREFIX="%{tde_prefix}" \
  -DBIN_INSTALL_DIR="%{tde_bindir}" \
  -DINCLUDE_INSTALL_DIR="%{tde_tdeincludedir}" \
  -DLIB_INSTALL_DIR="%{tde_libdir}" \
  -DMAN_INSTALL_DIR="%{tde_mandir}" \
  -DPKGCONFIG_INSTALL_DIR="%{tde_libdir}/pkgconfig" \
  \
  -DWITH_ALSA=ON \
  -DWITH_AUDIOFILE=ON \
  -DWITH_VORBIS=ON \
  %{?with_libmad:-DWITH_MAD=ON} %{!?with_libmad:-DWITH_MAD=OFF} \
  -DWITH_ESOUND=OFF \
  %{?with_jack:-DWITH_JACK=ON} %{!?with_jack:-DWITH_JACK=OFF} \
  ..

%__make %{?_smp_mflags} || %__make


%install
%__make install -C build DESTDIR=%{?buildroot}

%__install -d -m 755 %{?buildroot}%{tde_datadir}/config
%__install -d -m 755 %{?buildroot}%{tde_datadir}/doc

# Installs the Pulseaudio configuration file
%if 0%{?with_pulseaudio}
%__mkdir_p "%{?buildroot}%{tde_confdir}"
cat <<EOF >"%{?buildroot}%{tde_confdir}/kcmartsrc"
[Arts]
Arguments=\s-F 10 -S 4096 -a esd -n -s 1 -m artsmessage -c drkonqi -l 3 -f
NetworkTransparent=true
SuspendTime=1
EOF
chmod 644 "%{?buildroot}%{tde_confdir}/kcmartsrc"
%endif

# Add supplementary folders
%__install -d -m 755 "%{?buildroot}%{tde_libdir}/mcop/Arts/Environment"
