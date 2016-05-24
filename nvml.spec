
Name:		nvml
Version:	1.0
Release:	1%{?dist}
Summary:	Non-Volatile Memory Library
License:	BSD
URL:		http://pmem.io/nvml
Source0:	https://github.com/pmem/nvml/archive/%{version}.tar.gz
Patch0:		1.0-0001-test-fix-timeouting-obj_tx_add_range-test.patch
Patch1:		1.0-0002-all-always-append-EXTRA_CFLAGS-after-our-CFLAGS.patch

BuildRequires:	glibc-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	man

# By design, NVML does not support any 32-bit architecture.
# Due to dependency on xmmintrin.h and some inline assembly, it can be
# compiled only for x86_64 at the moment.
# Other 64-bit architectures could also be supported, if only there is
# a request for that, and if somebody provides the arch-specific
# implementation of the low-level routines for flushing to persistent
# memory.
ExcludeArch:	%{ix86}
ExcludeArch:	%{arm}
ExcludeArch:	s390x

%description
The NVM Library is a collection of libraries for using memory-mapped
persistence, optimized specifically for persistent memory.


%package -n libpmem
Summary: Low-level persistent memory support library
Group: System Environment/Libraries
%description -n libpmem
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided.

%files -n libpmem
%defattr(644,root,root,-)
%dir %{_datadir}/nvml
%{_libdir}/libpmem.so.*
%{_datadir}/nvml/nvml.magic
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmem-devel
Summary: Development files for the low-level persistent memory library
Group: Development/Libraries
Requires: libpmem = %{version}-%{release}
%description -n libpmem-devel
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided.

This library is provided for software which tracks every store to
pmem and needs to flush those changes to durability. Most developers
will find higher level libraries like libpmemobj to be much more
convenient.

%files -n libpmem-devel
%defattr(644,root,root,-)
%dir %{_libdir}/nvml_debug
%{_libdir}/libpmem.so
%{_libdir}/pkgconfig/libpmem.pc
%{_libdir}/nvml_debug/libpmem.so
%{_libdir}/nvml_debug/libpmem.so.*
%{_includedir}/libpmem.h
%{_mandir}/man3/libpmem.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemblk
Summary: Persistent Memory Resident Array of Blocks library
Group: System Environment/Libraries
%description -n libpmemblk
The libpmemblk implements a pmem-resident array of blocks, all the same
size, where a block is updated atomically with respect to power
failure or program interruption (no torn blocks).

%files -n libpmemblk
%defattr(644,root,root,-)
%{_libdir}/libpmemblk.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemblk-devel
Summary: Development files for the Persistent Memory Resident Array of Blocks library
Group: Development/Libraries
Requires: libpmemblk = %{version}-%{release}
Requires: libpmem-devel = %{version}-%{release}
%description -n libpmemblk-devel
The libpmemblk implements a pmem-resident array of blocks, all the same
size, where a block is updated atomically with respect to power
failure or program interruption (no torn blocks).

For example, a program keeping a cache of fixed-size objects in pmem
might find this library useful. This library is provided for cases
requiring large arrays of objects at least 512 bytes each. Most
developers will find higher level libraries like libpmemobj to be
more generally useful.

%files -n libpmemblk-devel
%defattr(644,root,root,-)
%dir %{_libdir}/nvml_debug
%{_libdir}/libpmemblk.so
%{_libdir}/pkgconfig/libpmemblk.pc
%{_libdir}/nvml_debug/libpmemblk.so
%{_libdir}/nvml_debug/libpmemblk.so.*
%{_includedir}/libpmemblk.h
%{_mandir}/man3/libpmemblk.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemlog
Summary: Persistent Memory Resident Log File library
Group: System Environment/Libraries
%description -n libpmemlog
The libpmemlog library provides a pmem-resident log file. This is
useful for programs like databases that append frequently to a log
file.

%files -n libpmemlog
%defattr(644,root,root,-)
%{_libdir}/libpmemlog.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemlog-devel
Summary: Development files for the Persistent Memory Resident Log File library
Group: Development/Libraries
Requires: libpmemlog = %{version}-%{release}
Requires: libpmem-devel = %{version}-%{release}
%description -n libpmemlog-devel
The libpmemlog library provides a pmem-resident log file. This
library is provided for cases requiring an append-mostly file to
record variable length entries. Most developers will find higher
level libraries like libpmemobj to be more generally useful.

%files -n libpmemlog-devel
%defattr(644,root,root,-)
%dir %{_libdir}/nvml_debug
%{_libdir}/libpmemlog.so
%{_libdir}/pkgconfig/libpmemlog.pc
%{_libdir}/nvml_debug/libpmemlog.so
%{_libdir}/nvml_debug/libpmemlog.so.*
%{_includedir}/libpmemlog.h
%{_mandir}/man3/libpmemlog.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemobj
Summary: Persistent Memory Transactional Object Store library
Group: System Environment/Libraries
%description -n libpmemobj
The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming.

%files -n libpmemobj
%defattr(644,root,root,-)
%{_libdir}/libpmemobj.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemobj-devel
Summary: Development files for the Persistent Memory Transactional Object Store library
Group: Development/Libraries
Requires: libpmemobj = %{version}-%{release}
Requires: libpmem-devel = %{version}-%{release}
%description -n libpmemobj-devel
The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming. Developers new to persistent memory
probably want to start with this library.

%files -n libpmemobj-devel
%defattr(644,root,root,-)
%dir %{_libdir}/nvml_debug
%{_libdir}/libpmemobj.so
%{_libdir}/pkgconfig/libpmemobj.pc
%{_libdir}/nvml_debug/libpmemobj.so
%{_libdir}/nvml_debug/libpmemobj.so.*
%{_includedir}/libpmemobj.h
%{_mandir}/man3/libpmemobj.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libvmem
Summary: Volatile Memory allocation library
Group: System Environment/Libraries
%description -n libvmem
The libvmem library turns a pool of persistent memory into a volatile
memory pool, similar to the system heap but kept separate and with
its own malloc-style API.

%files -n libvmem
%defattr(644,root,root,-)
%{_libdir}/libvmem.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libvmem-devel
Summary: Development files for the Volatile Memory allocation library
Group: Development/Libraries
Requires: libvmem = %{version}-%{release}
%description -n libvmem-devel
The libvmem library turns a pool of persistent memory into a volatile
memory pool, similar to the system heap but kept separate and with
its own malloc-style API.

This sub-package contains libraries and header files for developing
applications that want to make use of libvmem.

%files -n libvmem-devel
%defattr(644,root,root,-)
%dir %{_libdir}/nvml_debug
%{_libdir}/libvmem.so
%{_libdir}/pkgconfig/libvmem.pc
%{_libdir}/nvml_debug/libvmem.so
%{_libdir}/nvml_debug/libvmem.so.*
%{_includedir}/libvmem.h
%{_mandir}/man3/libvmem.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libvmmalloc
Summary: Dynamic to Persistent Memory allocation translation library
Group: System Environment/Libraries
%description -n libvmmalloc
The libvmmalloc library transparently converts all the dynamic memory
allocations into persistent memory allocations. This allows the use
of persistent memory as volatile memory without modifying the target
application.

The typical usage of libvmmalloc is to load it via the LD_PRELOAD
environment variable.

%files -n libvmmalloc
%defattr(644,root,root,-)
%{_libdir}/libvmmalloc.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libvmmalloc-devel
Summary: Development files for the Dynamic-to-Persistent allocation library
Group: Development/Libraries
Requires: libvmmalloc = %{version}-%{release}
%description -n libvmmalloc-devel
The libvmmalloc library transparently converts all the dynamic memory
allocations into persistent memory allocations. This allows the use
of persistent memory as volatile memory without modifying the target
application.

This sub-package contains libraries and header files for developing
applications that want to specifically make use of libvmmalloc.

%files -n libvmmalloc-devel
%defattr(644,root,root,-)
%dir %{_libdir}/nvml_debug
%{_libdir}/libvmmalloc.so
%{_libdir}/pkgconfig/libvmmalloc.pc
%{_libdir}/nvml_debug/libvmmalloc.so
%{_libdir}/nvml_debug/libvmmalloc.so.*
%{_includedir}/libvmmalloc.h
%{_mandir}/man3/libvmmalloc.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package tools
Summary: Utilities for Persistent Memory
Group: System Environment/Base
%description tools
Useful applications for administration and diagnosis of persistent memory.

%files tools
%{_bindir}/pmempool
%{_mandir}/man1/pmempool.1.gz
%{_mandir}/man1/pmempool-info.1.gz
%{_mandir}/man1/pmempool-create.1.gz
%{_mandir}/man1/pmempool-dump.1.gz
%{_mandir}/man1/pmempool-check.1.gz
%{_mandir}/man1/pmempool-rm.1.gz
%config(noreplace) %{_sysconfdir}/bash_completion.d/pmempool.sh
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
chmod +x src/test/obj_tx_add_range/TEST2
%patch1 -p1


%build
# Currently, NVML makefiles do not allow to easily override CFLAGS,
# so the build flags are passed via EXTRA_CFLAGS.  For debug build
# selected flags are overriden to disable compiler optimizations.
EXTRA_CFLAGS_RELEASE="%{optflags}" \
EXTRA_CFLAGS_DEBUG="%{optflags} -Wp,-U_FORTIFY_SOURCE -O0" \
EXTRA_CXXFLAGS="%{optflags}" \
make %{?_smp_mflags}


# Override LIB_AR with empty string to skip installation of static libraries
%install
make install DESTDIR=%{buildroot} \
	LIB_AR= \
	prefix=%{_prefix} \
	libdir=%{_libdir} \
	includedir=%{_includedir} \
	mandir=%{_mandir} \
	bindir=%{_bindir} \
	sysconfdir=%{_sysconfdir}
mkdir -p %{buildroot}%{_datadir}/nvml
cp utils/nvml.magic %{buildroot}%{_datadir}/nvml/


%check
cp src/test/testconfig.sh.example src/test/testconfig.sh
make check


%post   -n libpmem -p /sbin/ldconfig
%postun -n libpmem -p /sbin/ldconfig
%post   -n libpmemblk -p /sbin/ldconfig
%postun -n libpmemblk -p /sbin/ldconfig
%post   -n libpmemlog -p /sbin/ldconfig
%postun -n libpmemlog -p /sbin/ldconfig
%post   -n libpmemobj -p /sbin/ldconfig
%postun -n libpmemobj -p /sbin/ldconfig
%post   -n libvmem -p /sbin/ldconfig
%postun -n libvmem -p /sbin/ldconfig
%post   -n libvmmalloc -p /sbin/ldconfig
%postun -n libvmmalloc -p /sbin/ldconfig


%if 0%{?__debug_package} == 0
%debug_package
%endif


%changelog
* Tue May 24 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.0-1
- Initial RPM release
