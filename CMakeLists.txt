cmake_minimum_required(VERSION 3.0.0)

#set( CMAKE_VERBOSE_MAKEFILE on )

set(CMAKE_TRY_COMPILE_TARGET_TYPE "STATIC_LIBRARY")
set(BUILD_SHARED_LIBS OFF)

project(launcher VERSION 0.1.0)

include(CTest)
enable_testing()

set(EXE lmr)

IF(WIN32 OR (${CMAKE_C_COMPILER} MATCHES "mingw"))
    set(PLATFORM Windows)
ELSE()
    set(PLATFORM Posix)
ENDIF()

file(GLOB ALL_SRC "*.cpp" "${PLATFORM}/*.cpp")

add_executable(${EXE} ${ALL_SRC})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})

include_directories(. ${PLATFORM})


include(CPack)
