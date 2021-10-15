%global optflags %{optflags} -Wno-error=unused-function
%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

%define oname	OpenColrIO

Summary:	Enables color transforms and image display across graphics apps
Name:		OpenColorIO1
Version:	1.1.1
Release:	2
Group:		System/Libraries
License:	BSD
Url:		http://opencolorio.org/
# Github archive was generated on the fly using the following URL:
# https://github.com/imageworks/OpenColorIO/tarball/v1.0.9
Source0:        https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/v%{version}/OpenColorIO-%{version}.tar.gz
Patch0:		OpenColorIO-1.1.0-compile.patch

BuildRequires:	boost-devel
BuildRequires:	cmake ninja
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	python-sphinx
# FIXME this is a workaround for incompatibility with current glew and
# glext.h -- should really be a BuildRequires, the BuildConflict works
# around the problem by disabling some optional components.
BuildConflicts:	pkgconfig(glew)

#######################
# Unbundled libraries #
#######################
BuildRequires:	tinyxml-devel
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(yaml-cpp)

%description
OpenColorIO v1 compat package needed for Krita 4.x. OCIO enables color transforms and image display to be handled in a consistent
manner across multiple graphics applications. Unlike other color management
solutions, OCIO is geared towards motion-picture post production, with an
emphasis on visual effects and animation color pipelines.

%package -n %{libname}
Summary:	Enables color transforms and image display across graphics apps
Group:		System/Libraries

%description -n %{libname}
Enables color transforms and image display across graphics apps.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Development files for %{name} library.

%prep
%setup -qn OpenColorIO-%{version}
%autopatch -p1
# Remove what bundled libraries
rm -f ext/lcms*
rm -f ext/tinyxml*
rm -f ext/yaml*

%build
%cmake \
	-DCMAKE_SKIP_RPATH=TRUE \
	-DOCIO_BUILD_STATIC=OFF \
	-DPYTHON_INCLUDE_LIB_PREFIX=OFF \
	-DOCIO_BUILD_DOCS=OFF \
	-DOCIO_BUILD_TESTS=ON \
	-DOCIO_LINK_PYGLUE=ON \
	-DOCIO_PYGLUE_SONAME=OFF \
	-DUSE_EXTERNAL_YAML=TRUE \
	-DUSE_EXTERNAL_TINYXML=TRUE \
	-DUSE_EXTERNAL_LCMS=TRUE \
%ifnarch %{x86_64}
	-DOCIO_USE_SSE=OFF \
%endif
	-G Ninja

PYTHONDONTWRITEBYTECODE= %ninja_build

%install
%ninja_install -C build

# Fix location of cmake files.
mkdir -p %{buildroot}%{_datadir}/cmake/Modules
find %{buildroot} -name "*.cmake" -exec mv {} %{buildroot}%{_datadir}/cmake/Modules/ \;


%files
%doc ChangeLog LICENSE README.md
%{_bindir}/*
%{python_sitearch}/Py%{oname}.so
%{_datadir}/ocio

%files -n %{libname}
%{_libdir}/libOpenColorIO.so.%{major}*

%files -n %{devname}
%{_libdir}/lib%{oname}.so
%{_libdir}/pkgconfig/%{oname}.pc
%{_includedir}/%{oname}
%{_includedir}/Py%{oname}
%{_datadir}/cmake/Modules/*
