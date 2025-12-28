%bcond clang 1
%bcond jack 1
%bcond mad 1
%bcond esound 0
%bcond pulseaudio 1

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 4

%define tde_pkg arts

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.5.10
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	ARTS (analog realtime synthesizer) - the TDE sound system
Group:		System Environment/Daemons 
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

Prefix:		/opt/trinity

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz
Source1:	%{name}-rpmlintrc

Patch0:   trinity-arts-fix-rpath.patch

BuildSystem:    cmake

BuildOption:    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_SKIP_RPATH=OFF
BuildOption:    -DCMAKE_SKIP_INSTALL_RPATH=OFF
BuildOption:    -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
BuildOption:    -DCMAKE_INSTALL_RPATH=%{prefix}/%{_lib}
BuildOption:    -DCMAKE_NO_BUILTIN_CHRPATH=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{prefix}/include/tde
BuildOption:    -DPKGCONFIG_INSTALL_DIR=%{prefix}/%{_lib}/pkgconfig
BuildOption:    -DWITH_MAD=%{!?with_mad:OFF}%{?with_mad:ON}
BuildOption:    -DWITH_ESOUND=%{!?with_esound:OFF}%{?with_esound:ON}
BuildOption:    -DWITH_JACK=%{!?with_jack:OFF}%{?with_jack:ON} 


BuildRequires:	libtqt4-devel >= %{tde_epoch}:4.2.0
BuildRequires:	trinity-filesystem >= %{tde_version}
Requires:		trinity-filesystem >= %{tde_version}

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(audiofile)

BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gsl)

# VORBIS support
BuildRequires:  pkgconfig(vorbis)

# ALSA support
BuildRequires:  pkgconfig(alsa)


# ESOUND support
%{?with_esound:BuildRequires:  pkgconfig(esound)}

# JACK support
%{?with_jack:BuildRequires:  pkgconfig(jack)}

# LIBTOOL
BuildRequires:  libtool-devel

# MAD support
%{?with_mad:BuildRequires:  pkgconfig(mad)}

Requires:		libtqt4 >= %{tde_epoch}:4.2.0
#Requires:		audiofile

%if "%{?prefix}" == "/usr"
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
%dir %{prefix}/%{_lib}/mcop
%dir %{prefix}/%{_lib}/mcop/Arts
%{prefix}/%{_lib}/mcop/Arts/*
%{prefix}/%{_lib}/mcop/*.mcopclass
%{prefix}/%{_lib}/mcop/*.mcoptype
%{prefix}/%{_lib}/lib*.so.*
%{prefix}/bin/artscat
%{prefix}/bin/artsd
%{prefix}/bin/artsdsp
%{prefix}/bin/artsplay
%{prefix}/bin/artsrec
%{prefix}/bin/artsshell
%{prefix}/bin/artswrapper
# The '.la' files are needed for runtime, not devel !
%{prefix}/%{_lib}/lib*.la
%{prefix}/share/man/man1/artsc-config-trinity.1*
%{prefix}/share/man/man1/artscat-trinity.1*
%{prefix}/share/man/man1/artsdsp-trinity.1*

##########

%package devel
Group:		Development/Libraries
Summary:	ARTS (analog realtime synthesizer) - the TDE sound system (Development files)
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%if "%{?prefix}" == "/usr"
Obsoletes:	arts-devel < %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Requires:	pkgconfig(alsa)
Requires:	pkgconfig(audiofile)
Requires:  pkgconfig(vorbis)
%{?with_esound:Requires:  pkgconfig(esound)}
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
%{prefix}/bin/mcopidl
# Arts includes are under 'tde' - this is on purpose !
%{prefix}/include/tde/arts/
# Artsc includes are not under 'tde'.
%{prefix}/include/artsc/
%{prefix}/bin/artsc-config
%{prefix}/%{_lib}/pkgconfig/*.pc
%{prefix}/%{_lib}/lib*.so
%{prefix}/%{_lib}/*.a

%if %{with pulseaudio}
%package config-pulseaudio
Group:		System Environment/Daemons
Summary:	ARTS - Default configuration file for Pulseaudio
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description config-pulseaudio
This package contains a default ARTS configuration file, that is 
intended for systems running the Pulseaudio server.

%files config-pulseaudio
%defattr(-,root,root,-)
%config %{_sysconfdir}/trinity/kcmartsrc
%endif

%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{prefix}/%{_lib}/pkgconfig"


%install -a
%__install -d -m 755 %{?buildroot}%{prefix}/share/config
%__install -d -m 755 %{?buildroot}%{prefix}/share/doc

# Installs the Pulseaudio configuration file
%if %{with pulseaudio}
%__mkdir_p "%{?buildroot}%{_sysconfdir}/trinity"
cat <<EOF >"%{?buildroot}%{_sysconfdir}/trinity/kcmartsrc"
[Arts]
Arguments=\s-F 10 -S 4096 -a esd -n -s 1 -m artsmessage -c drkonqi -l 3 -f
NetworkTransparent=true
SuspendTime=1
EOF
chmod 644 "%{?buildroot}%{_sysconfdir}/trinity/kcmartsrc"
%endif

# Add supplementary folders
%__install -d -m 755 "%{?buildroot}%{prefix}/%{_lib}/mcop/Arts/Environment"
