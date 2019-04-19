cmake_minimum_required(VERSION 3.14)
project(NGEN VERSION 1.0.0 LANGUAGES CXX)

add_library(NGEN SHARED src/IO.cc src/Module.cc src/ModulePool.cc src/noise.cc src/Property.cc)

target_include_directories(NGEN
        PUBLIC
        $<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        )
target_compile_features(NGEN PUBLIC cxx_std_17)

include(GNUInstallDirs)

message(STATUS "CMAKE_INSTALL_INCLUDEDIR:" ${CMAKE_INSTALL_INCLUDEDIR})
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(TARGETS NGEN
        EXPORT NGEN-targets
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        )

set(INSTALL_CONFIGDIR ${CMAKE_INSTALL_LIBDIR}/cmake/NGEN)

install(EXPORT
        NGEN-targets
        FILE
        NGENTargets.cmake
        NAMESPACE
        NGEN::
        DESTINATION
        ${INSTALL_CONFIGDIR}
        )

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
        ${CMAKE_CURRENT_BINARY_DIR}/NGENConfigVersion.cmake
        VERSION ${PROJECT_VERSION}
        COMPATIBILITY AnyNewerVersion
)

configure_package_config_file(${CMAKE_CURRENT_LIST_DIR}/cmake/NGENConfig.cmake.in
        ${CMAKE_CURRENT_BINARY_DIR}/NGENConfig.cmake
        INSTALL_DESTINATION ${INSTALL_CONFIGDIR}
        )

install(FILES
        ${CMAKE_CURRENT_BINARY_DIR}/NGENConfig.cmake
        ${CMAKE_CURRENT_BINARY_DIR}/NGENConfigVersion.cmake
        DESTINATION ${INSTALL_CONFIGDIR}
        )


configure_file(src/NGEN.pc.in src/NGEN.pc @ONLY)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/src/NGEN.pc"
        DESTINATION "${CMAKE_INSTALL_LIBDIR}/pkgconfig")

export(EXPORT NGEN-targets FILE ${CMAKE_CURRENT_BINARY_DIR}/NGENTargets.cmake NAMESPACE NGEN::)
export(PACKAGE NGEN)


