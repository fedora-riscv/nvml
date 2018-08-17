
# rpmbuild options:
#   --with | --without fabric
#   --with | --without ndctl
#   --define _testconfig <path to custom testconfig.sh>

# do not terminate build if files in the $RPM_BUILD_ROOT
# directory are not found in %%files (without fabric case)
%define _unpackaged_files_terminate_build 0

# disable 'make check' on suse
%if %{defined suse_version}
	%define _skip_check 1
	%define dist .suse%{suse_version}
%endif

%if (0%{?suse_version} > 1315) || (0%{?fedora} >= 27) || (0%{?rhel} >= 7)
%bcond_without fabric
%else
%bcond_with fabric
%endif

# by default build with ndctl, unless explicitly disabled
%bcond_without ndctl

%define min_libfabric_ver 1.4.2
%define min_ndctl_ver 60.1
%define upstreamversion 1.4.2

Name:		nvml
Version:	1.4.2
Release:	1%{?dist}
Summary:	Persistent Memory Development Kit (formerly NVML)
License:	BSD
URL:		http://pmem.io/pmdk

Source0:	https://github.com/pmem/%{name}/archive/%{upstreamversion}.tar.gz#/%{name}-%{upstreamversion}.tar.gz

BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	glibc-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	man
BuildRequires:	pkgconfig
BuildRequires:	doxygen
BuildRequires:	gdb

%if %{with ndctl}
BuildRequires:	ndctl-devel >= %{min_ndctl_ver}
BuildRequires:	daxctl-devel >= %{min_ndctl_ver}
%endif

%if %{with fabric}
BuildRequires:	libfabric-devel >= %{min_libfabric_ver}
%endif


# Debug variants of the libraries should be filtered out of the provides.
%global __provides_exclude_from ^%{_libdir}/pmdk_debug/.*\\.so.*$

# By design, PMDK does not support any 32-bit architecture.
# Due to dependency on xmmintrin.h and some inline assembly, it can be
# compiled only for x86_64 at the moment.
# Other 64-bit architectures could also be supported, if only there is
# a request for that, and if somebody provides the arch-specific
# implementation of the low-level routines for flushing to persistent
# memory.

# https://bugzilla.redhat.com/show_bug.cgi?id=1340634
# https://bugzilla.redhat.com/show_bug.cgi?id=1340635
# https://bugzilla.redhat.com/show_bug.cgi?id=1340636
# https://bugzilla.redhat.com/show_bug.cgi?id=1340637

ExclusiveArch: x86_64

%description
The Persistent Memory Development Kit is a collection of libraries for
using memory-mapped persistence, optimized specifically for persistent memory.


%package -n libpmem
Summary: Low-level persistent memory support library
Group: System Environment/Libraries
%description -n libpmem
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided.

%files -n libpmem
%dir %{_datadir}/pmdk
%{_libdir}/libpmem.so.*
%{_datadir}/pmdk/pmdk.magic
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
%{_libdir}/libpmem.so
%{_libdir}/pkgconfig/libpmem.pc
%{_includedir}/libpmem.h
%{_mandir}/man7/libpmem.7.gz
%{_mandir}/man3/pmem_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmem-debug
Summary: Debug variant of the low-level persistent memory library
Group: Development/Libraries
Requires: libpmem = %{version}-%{release}
%description -n libpmem-debug
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmem-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmem.so
%{_libdir}/pmdk_debug/libpmem.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemblk
Summary: Persistent Memory Resident Array of Blocks library
Group: System Environment/Libraries
Requires: libpmem >= %{version}-%{release}
%description -n libpmemblk
The libpmemblk implements a pmem-resident array of blocks, all the same
size, where a block is updated atomically with respect to power
failure or program interruption (no torn blocks).

%files -n libpmemblk
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
%{_libdir}/libpmemblk.so
%{_libdir}/pkgconfig/libpmemblk.pc
%{_includedir}/libpmemblk.h
%{_mandir}/man7/libpmemblk.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmemblk_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemblk-debug
Summary: Debug variant of the Persistent Memory Resident Array of Blocks library
Group: Development/Libraries
Requires: libpmemblk = %{version}-%{release}
%description -n libpmemblk-debug
The libpmemblk implements a pmem-resident array of blocks, all the same
size, where a block is updated atomically with respect to power
failure or program interruption (no torn blocks).

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmemblk-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmemblk.so
%{_libdir}/pmdk_debug/libpmemblk.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemlog
Summary: Persistent Memory Resident Log File library
Group: System Environment/Libraries
Requires: libpmem >= %{version}-%{release}
%description -n libpmemlog
The libpmemlog library provides a pmem-resident log file. This is
useful for programs like databases that append frequently to a log
file.

%files -n libpmemlog
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
%{_libdir}/libpmemlog.so
%{_libdir}/pkgconfig/libpmemlog.pc
%{_includedir}/libpmemlog.h
%{_mandir}/man7/libpmemlog.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmemlog_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemlog-debug
Summary: Debug variant of the Persistent Memory Resident Log File library
Group: Development/Libraries
Requires: libpmemlog = %{version}-%{release}
%description -n libpmemlog-debug
The libpmemlog library provides a pmem-resident log file. This
library is provided for cases requiring an append-mostly file to
record variable length entries. Most developers will find higher
level libraries like libpmemobj to be more generally useful.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmemlog-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmemlog.so
%{_libdir}/pmdk_debug/libpmemlog.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemobj
Summary: Persistent Memory Transactional Object Store library
Group: System Environment/Libraries
Requires: libpmem >= %{version}-%{release}
%description -n libpmemobj
The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming.

%files -n libpmemobj
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
%{_libdir}/libpmemobj.so
%{_libdir}/pkgconfig/libpmemobj.pc
%{_includedir}/libpmemobj.h
%{_includedir}/libpmemobj/*.h
%{_mandir}/man7/libpmemobj.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmemobj_*.3.gz
%{_mandir}/man3/pobj_*.3.gz
%{_mandir}/man3/oid_*.3.gz
%{_mandir}/man3/toid*.3.gz
%{_mandir}/man3/direct_*.3.gz
%{_mandir}/man3/d_r*.3.gz
%{_mandir}/man3/tx_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemobj-debug
Summary: Debug variant of the Persistent Memory Transactional Object Store library
Group: Development/Libraries
Requires: libpmemobj = %{version}-%{release}
%description -n libpmemobj-debug
The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming. Developers new to persistent memory
probably want to start with this library.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmemobj-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmemobj.so
%{_libdir}/pmdk_debug/libpmemobj.so.*
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
%{_libdir}/libvmem.so
%{_libdir}/pkgconfig/libvmem.pc
%{_includedir}/libvmem.h
%{_mandir}/man7/libvmem.7.gz
%{_mandir}/man3/vmem_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libvmem-debug
Summary: Debug variant of the Volatile Memory allocation library
Group: Development/Libraries
Requires: libvmem = %{version}-%{release}
%description -n libvmem-debug
The libvmem library turns a pool of persistent memory into a volatile
memory pool, similar to the system heap but kept separate and with
its own malloc-style API.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libvmem-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libvmem.so
%{_libdir}/pmdk_debug/libvmem.so.*
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
%{_libdir}/libvmmalloc.so
%{_libdir}/pkgconfig/libvmmalloc.pc
%{_includedir}/libvmmalloc.h
%{_mandir}/man7/libvmmalloc.7.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libvmmalloc-debug
Summary: Debug variant of the Dynamic-to-Persistent allocation library
Group: Development/Libraries
Requires: libvmmalloc = %{version}-%{release}
%description -n libvmmalloc-debug
The libvmmalloc library transparently converts all the dynamic memory
allocations into persistent memory allocations. This allows the use
of persistent memory as volatile memory without modifying the target
application.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libvmmalloc-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libvmmalloc.so
%{_libdir}/pmdk_debug/libvmmalloc.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


# Specify a virtual Provide for libpmemobj++-static package, so the package
# usage can be tracked.
%package -n libpmemobj++-devel
Summary: C++ bindings for Persistent Memory Transactional Object Store library
Group: Development/Libraries
Provides: libpmemobj++-static = %{version}-%{release}
Requires: libpmemobj-devel = %{version}-%{release}
%description -n libpmemobj++-devel
The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming.

This sub-package contains header files for libpmemobj C++ bindings.

%files -n libpmemobj++-devel
%{_libdir}/pkgconfig/libpmemobj++.pc
%{_includedir}/libpmemobj++/*.hpp
%{_includedir}/libpmemobj++/detail/*.hpp
%{_docdir}/libpmemobj++-devel/*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmempool
Summary: Persistent Memory pool management library
Group: System Environment/Libraries
Requires: libpmem >= %{version}-%{release}
%description -n libpmempool
The libpmempool library provides a set of utilities for off-line
administration, analysis, diagnostics and repair of persistent memory
pools created by libpmemlog, libpemblk and libpmemobj libraries.

%files -n libpmempool
%{_libdir}/libpmempool.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmempool-devel
Summary: Development files for Persistent Memory pool management library
Group: Development/Libraries
Requires: libpmempool = %{version}-%{release}
Requires: libpmem-devel = %{version}-%{release}
%description -n libpmempool-devel
The libpmempool library provides a set of utilities for off-line
administration, analysis, diagnostics and repair of persistent memory
pools created by libpmemlog, libpemblk and libpmemobj libraries.

%files -n libpmempool-devel
%{_libdir}/libpmempool.so
%{_libdir}/pkgconfig/libpmempool.pc
%{_includedir}/libpmempool.h
%{_mandir}/man7/libpmempool.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmempool_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmempool-debug
Summary: Debug variant of the Persistent Memory pool management library
Group: Development/Libraries
Requires: libpmempool = %{version}-%{release}
%description -n libpmempool-debug
The libpmempool library provides a set of utilities for off-line
administration, analysis, diagnostics and repair of persistent memory
pools created by libpmemlog, libpemblk and libpmemobj libraries.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmempool-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmempool.so
%{_libdir}/pmdk_debug/libpmempool.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%if %{with fabric}

%package -n librpmem
Summary: Remote Access to Persistent Memory library
Group: System Environment/Libraries
Requires: libfabric >= %{min_libfabric_ver}
Requires: openssh-clients
%description -n librpmem
The librpmem library provides low-level support for remote access
to persistent memory utilizing RDMA-capable NICs. It can be used
to replicate peristent memory regions over RDMA protocol.

%files -n librpmem
%{_libdir}/librpmem.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n librpmem-devel
Summary: Development files for the Remote Access to Persistent Memory library
Group: Development/Libraries
Requires: librpmem = %{version}-%{release}
%description -n librpmem-devel
The librpmem library provides low-level support for remote access
to persistent memory utilizing RDMA-capable NICs. It can be used
to replicate peristent memory regions over RDMA protocol.

This sub-package contains libraries and header files for developing
applications that want to specifically make use of librpmem.

%files -n librpmem-devel
%{_libdir}/librpmem.so
%{_libdir}/pkgconfig/librpmem.pc
%{_includedir}/librpmem.h
%{_mandir}/man7/librpmem.7.gz
%{_mandir}/man3/rpmem_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n librpmem-debug
Summary: Debug variant of the Remote Access to Persistent Memory library
Group: Development/Libraries
Requires: librpmem = %{version}-%{release}
%description -n librpmem-debug
The librpmem library provides low-level support for remote access
to persistent memory utilizing RDMA-capable NICs. It can be used
to replicate peristent memory regions over RDMA protocol.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n librpmem-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/librpmem.so
%{_libdir}/pmdk_debug/librpmem.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n rpmemd
Group: System Environment/Base
Summary: Target node process executed by librpmem
Requires: libfabric >= %{min_libfabric_ver}
%description -n rpmemd
The rpmemd process is executed on a target node by librpmem library
and facilitates access to persistent memory over RDMA.

%files -n rpmemd
%{_bindir}/rpmemd
%{_mandir}/man1/rpmemd.1.gz

%endif # _with_fabric


%package -n libpmemcto
Summary: Close-to-Open Persistence library
Group: System Environment/Libraries
Requires: libpmem >= %{version}-%{release}
%description -n libpmemcto
The libpmemcto library is a Persistent Memory allocator with no overhead
imposed by run-time flushing or transactional updates.

%files -n libpmemcto
%{_libdir}/libpmemcto.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemcto-devel
Summary: Development files for Close-to-Open Persistence library
Group: Development/Libraries
Requires: libpmemcto = %{version}-%{release}
Requires: libpmem-devel = %{version}-%{release}
%description -n libpmemcto-devel
The libpmemcto library is a Persistent Memory allocator with no overhead
imposed by run-time flushing or transactional updates.

%files -n libpmemcto-devel
%{_libdir}/libpmemcto.so
%{_libdir}/pkgconfig/libpmemcto.pc
%{_includedir}/libpmemcto.h
%{_mandir}/man7/libpmemcto.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmemcto*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemcto-debug
Summary: Debug variant of the Close-to-Open Persistence library
Group: Development/Libraries
Requires: libpmemcto = %{version}-%{release}
%description -n libpmemcto-debug
The libpmemcto library is a Persistent Memory allocator with no overhead
imposed by run-time flushing or transactional updates.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmemcto-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmemcto.so
%{_libdir}/pmdk_debug/libpmemcto.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n pmempool
Summary: Utilities for Persistent Memory
Group: System Environment/Base
Requires: libpmem >= %{version}-%{release}
Requires: libpmemlog >= %{version}-%{release}
Requires: libpmemblk >= %{version}-%{release}
Requires: libpmemobj >= %{version}-%{release}
Requires: libpmempool >= %{version}-%{release}
Requires: libpmemcto >= %{version}-%{release}
Obsoletes: nvml-tools < %{version}-%{release}
%description -n pmempool
The pmempool is a standalone utility for management and off-line analysis
of Persistent Memory pools created by PMDK libraries. It provides a set
of utilities for administration and diagnostics of Persistent Memory pools.
The pmempool may be useful for troubleshooting by system administrators
and users of the applications based on PMDK libraries.

%files -n pmempool
%{_bindir}/pmempool
%{_mandir}/man1/pmempool.1.gz
%{_mandir}/man1/pmempool-*.1.gz
%config(noreplace) %{_sysconfdir}/bash_completion.d/pmempool
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%if %{with ndctl}

%package -n daxio
Summary: Perform I/O on Device DAX devices or zero a Device DAX device
Group: System Environment/Base
Requires: libpmem >= %{version}-%{release}
%description -n daxio
The daxio utility performs I/O on Device DAX devices or zero
a Device DAX device.  Since the standard I/O APIs (read/write) cannot be used
with Device DAX, data transfer is performed on a memory-mapped device.
The daxio may be used to dump Device DAX data to a file, restore data from
a backup copy, move/copy data to another device or to erase data from
a device.

%files -n daxio
%{_bindir}/daxio
%{_mandir}/man1/daxio.1.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%endif # _with_ndctl


%prep
%setup -q -n pmdk-%{upstreamversion}


%build
# For debug build default flags may be overriden to disable compiler
# optimizations.
CFLAGS="%{optflags}" \
LDFLAGS="%{?__global_ldflags}" \
make %{?_smp_mflags} NORPATH=1


# Override LIB_AR with empty string to skip installation of static libraries
%install
make install DESTDIR=%{buildroot} \
	LIB_AR= \
	prefix=%{_prefix} \
	libdir=%{_libdir} \
	includedir=%{_includedir} \
	mandir=%{_mandir} \
	bindir=%{_bindir} \
	sysconfdir=%{_sysconfdir} \
	docdir=%{_docdir} \
	CPP_DOC_DIR=libpmemobj++-devel
mkdir -p %{buildroot}%{_datadir}/pmdk
cp utils/pmdk.magic %{buildroot}%{_datadir}/pmdk/



%check
%if 0%{?_skip_check} == 1
	echo "Check skipped"
%else
	%if %{defined _testconfig}
		cp %{_testconfig} src/test/testconfig.sh
	%else
		echo "PMEM_FS_DIR=/tmp" > src/test/testconfig.sh
		echo "PMEM_FS_DIR_FORCE_PMEM=1" >> src/test/testconfig.sh
	%endif
	make check
%endif

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
%post   -n libpmempool -p /sbin/ldconfig
%postun -n libpmempool -p /sbin/ldconfig
%post   -n libpmemcto -p /sbin/ldconfig
%postun -n libpmemcto -p /sbin/ldconfig

%if %{with fabric}
%post   -n librpmem -p /sbin/ldconfig
%postun -n librpmem -p /sbin/ldconfig
%endif

%if 0%{?__debug_package} == 0
%debug_package
%endif


%changelog
* Fri Aug 17 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.4.2-1
- Update to PMDK version 1.4.2 (RHBZ #1589406)

* Tue Aug 14 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.4.2-0.2.rc1
- Revert package name change

* Tue Aug 14 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.4.2-0.1.rc1
- Update to PMDK version 1.4.2-rc1 (RHBZ #1589406)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 30 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.4-3
- Revert package name change
- Re-enable check

* Thu Mar 29 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.4-2
- Fix issues found by rpmlint

* Thu Mar 29 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.4-1
- Rename NVML project to PMDK
- Update to PMDK version 1.4 (RHBZ #1480578, #1539562, #1539564)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.3.1-1
- Update to NVML version 1.3.1 (RHBZ #1480578)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.3-1
- Update to NVML version 1.3 (RHBZ #1451741, RHBZ #1455216)
- Add librpmem and rpmemd sub-packages
- Force file system to appear as PMEM for make check

* Fri Jun 16 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2.3-2
- Update to NVML version 1.2.3 (RHBZ #1451741)

* Sat Apr 15 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2.2-1
- Update to NVML version 1.2.2 (RHBZ #1436820, RHBZ #1425038)

* Thu Mar 16 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2.1-1
- Update to NVML version 1.2.1 (RHBZ #1425038)

* Tue Feb 21 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2-3
- Fix compilation under gcc 7.0.x (RHBZ #1424004)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 30 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2-1
- Update to NVML version 1.2 (RHBZ #1383467)
- Add libpmemobj C++ bindings

* Thu Jul 14 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.1-3
- Add missing package version requirements

* Mon Jul 11 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.1-2
- Move debug variants of the libraries to -debug subpackages

* Sun Jun 26 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.1-1
- NVML 1.1 release
- Update link to source tarball
- Add libpmempool subpackage
- Remove obsolete patches

* Wed Jun 01 2016 Dan Horák <dan[at]danny.cz> - 1.0-3
- switch to ExclusiveArch

* Sun May 29 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.0-2
- Exclude PPC architecture
- Add bug numbers for excluded architectures

* Tue May 24 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.0-1
- Initial RPM release