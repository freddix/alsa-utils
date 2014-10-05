Summary:	ALSA Utils
Name:		alsa-utils
Version:	1.0.28
Release:	1
License:	GPL
Group:		Applications/Sound
Source0:	ftp://ftp.alsa-project.org/pub/utils/%{name}-%{version}.tar.bz2
# Source0-md5:	361552d5b1cacd0a1e7ba09e69990211
Source1:	alsactl.conf
Source2:	snd-seq-midi.conf
URL:		http://www.alsa-project.org/
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	xmlto
Requires:	awk
Requires:	dialog
Requires:	pciutils
Requires:	psmisc
Requires:	which
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ALSA command line utilities.

%prep
%setup -q

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-alsaconf				\
	--with-systemdsystemunitdir=%{systemdunitdir}	\
	--with-udev-rules-dir=%{_prefix}/lib/udev/rules.d
%{__make}
%{__make} -C alsactl 90-alsa-restore.rules

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/arecord.1
echo ".so aplay.1" > $RPM_BUILD_ROOT%{_mandir}/man1/arecord.1

install -D %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/alsa/alsactl.conf
install -D %{SOURCE2} $RPM_BUILD_ROOT%{_prefix}/lib/modules-load.d/snd-seq-midi.conf

install -d $RPM_BUILD_ROOT%{_prefix}/lib/alsa
mv $RPM_BUILD_ROOT%{_datadir}/alsa/init $RPM_BUILD_ROOT%{_prefix}/lib/alsa

ln -s %{_prefix}/lib/alsa/init $RPM_BUILD_ROOT%{_datadir}/alsa/init

install alsactl/90-alsa-restore.rules \
	$RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d/90-alsa-restore.rules

%find_lang alsa-utils --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f alsa-utils.lang
%defattr(644,root,root,755)
%doc README ChangeLog

%dir %{_datadir}/alsa/init
%dir /var/lib/alsa
%dir %{_prefix}/lib/alsa
%{_prefix}/lib/alsa/init

%attr(755,root,root) %{_bindir}/aconnect
%attr(755,root,root) %{_bindir}/alsaloop
%attr(755,root,root) %{_bindir}/alsamixer
%attr(755,root,root) %{_bindir}/alsaucm
%attr(755,root,root) %{_bindir}/amidi
%attr(755,root,root) %{_bindir}/amixer
%attr(755,root,root) %{_bindir}/aplay
%attr(755,root,root) %{_bindir}/aplaymidi
%attr(755,root,root) %{_bindir}/arecord
%attr(755,root,root) %{_bindir}/arecordmidi
%attr(755,root,root) %{_bindir}/aseqdump
%attr(755,root,root) %{_bindir}/aseqnet
%attr(755,root,root) %{_bindir}/iecset
%attr(755,root,root) %{_bindir}/speaker-test
%attr(755,root,root) %{_sbindir}/alsactl
%{_datadir}/alsa/speaker-test
%{_datadir}/sounds/alsa
%{_datadir}/alsa/alsactl.conf

%{_prefix}/lib/modules-load.d/snd-seq-midi.conf
%{_prefix}/lib/udev/rules.d/90-alsa-restore.rules
%{systemdunitdir}/basic.target.wants/alsa-restore.service
%{systemdunitdir}/basic.target.wants/alsa-state.service
%{systemdunitdir}/shutdown.target.wants/alsa-store.service
%{systemdunitdir}/alsa-restore.service
%{systemdunitdir}/alsa-state.service
%{systemdunitdir}/alsa-store.service

%{_mandir}/man1/aconnect.1*
%{_mandir}/man1/alsactl.1*
%{_mandir}/man1/alsaloop.1*
%{_mandir}/man1/alsamixer.1*
%{_mandir}/man1/amidi.1*
%{_mandir}/man1/amixer.1*
%{_mandir}/man1/aplay.1*
%{_mandir}/man1/aplaymidi.1*
%{_mandir}/man1/arecord.1*
%{_mandir}/man1/arecordmidi.1*
%{_mandir}/man1/aseqdump.1*
%{_mandir}/man1/aseqnet.1*
%{_mandir}/man1/iecset.1*
%{_mandir}/man1/speaker-test.1*
%{_mandir}/man7/alsactl_init.7*

