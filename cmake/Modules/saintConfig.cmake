INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_SAINT saint)

FIND_PATH(
    SAINT_INCLUDE_DIRS
    NAMES saint/api.h
    HINTS $ENV{SAINT_DIR}/include
        ${PC_SAINT_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    SAINT_LIBRARIES
    NAMES gnuradio-saint
    HINTS $ENV{SAINT_DIR}/lib
        ${PC_SAINT_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/saintTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(SAINT DEFAULT_MSG SAINT_LIBRARIES SAINT_INCLUDE_DIRS)
MARK_AS_ADVANCED(SAINT_LIBRARIES SAINT_INCLUDE_DIRS)
