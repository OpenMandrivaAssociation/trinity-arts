%bcond clang 1
%bcond jack 1
%bcond mad 1
%bcond esound 0
%bcond pulseaudio 1

# TDE variables
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg arts

%define tde_prefix /opt/trinity

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Version:	1.5.10
Release:	%{?tde_version:%{tde_version}_}8
Summary:	ARTS (analog realtime synthesizer) - the TDE sound system
Group:		System Environment/Daemons 
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}.tar.xz
Source1:	%{name}-rpmlintrc

BuildSystem:    cmake

BuildOption:    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_SKIP_RPATH=OFF
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DPKGCONFIG_INSTALL_DIR=%{tde_prefix}/%{_lib}/pkgconfig
BuildOption:    -DWITH_MAD=%{!?with_mad:OFF}%{?with_mad:ON}
BuildOption:    -DWITH_ESOUND=%{!?with_esound:OFF}%{?with_esound:ON}
BuildOption:    -DWITH_JACK=%{!?with_jack:OFF}%{?with_jack:ON} 

BuildRequires:	pkgconfig(tqt)
BuildRequires:	trinity-filesystem >= %{tde_version}

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

#Requires:		audiofile

%if "%{?prefix}" == "/usr"
Obsoletes:	arts < %{EVRD}
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
%dir %{tde_prefix}/%{_lib}/mcop
%dir %{tde_prefix}/%{_lib}/mcop/Arts
%{tde_prefix}/%{_lib}/mcop/Arts/*
%{tde_prefix}/%{_lib}/mcop/*.mcopclass
%{tde_prefix}/%{_lib}/mcop/*.mcoptype
%{tde_prefix}/%{_lib}/lib*.so.*
%{tde_prefix}/bin/artscat
%{tde_prefix}/bin/artsd
%{tde_prefix}/bin/artsdsp
%{tde_prefix}/bin/artsplay
%{tde_prefix}/bin/artsrec
%{tde_prefix}/bin/artsshell
%{tde_prefix}/bin/artswrapper
# The '.la' files are needed for runtime, not devel !
%{tde_prefix}/%{_lib}/lib*.la
%{tde_prefix}/share/man/man1/artsc-config-trinity.1*
%{tde_prefix}/share/man/man1/artscat-trinity.1*
%{tde_prefix}/share/man/man1/artsdsp-trinity.1*

##########

%package devel
Group:		Development/Libraries
Summary:	ARTS (analog realtime synthesizer) - the TDE sound system (Development files)
Requires:	%{name} = %{EVRD}
%if "%{?prefix}" == "/usr"
Obsoletes:	arts-devel < %{EVRD}
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
%{tde_prefix}/bin/mcopidl
# Arts includes are under 'tde' - this is on purpose !
%{tde_prefix}/include/tde/arts/
# Artsc includes are not under 'tde'.
%{tde_prefix}/include/artsc/
%{tde_prefix}/bin/artsc-config
%{tde_prefix}/%{_lib}/pkgconfig/*.pc
%{tde_prefix}/%{_lib}/lib*.so
%{tde_prefix}/%{_lib}/*.a

%if %{with pulseaudio}
%package config-pulseaudio
Group:		System Environment/Daemons
Summary:	ARTS - Default configuration file for Pulseaudio
Requires:	%{name} = %{EVRD}

%description config-pulseaudio
This package contains a default ARTS configuration file, that is 
intended for systems running the Pulseaudio server.

%files config-pulseaudio
%defattr(-,root,root,-)
%config %{_sysconfdir}/trinity/kcmartsrc
%endif

%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"


%install -a
%__install -d -m 755 %{?buildroot}%{tde_prefix}/share/config
%__install -d -m 755 %{?buildroot}%{tde_prefix}/share/doc

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
%__install -d -m 755 "%{?buildroot}%{tde_prefix}/%{_lib}/mcop/Arts/Environment"

