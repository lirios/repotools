project(qmlOS)

cmake_minimum_required(VERSION 3.0.2 FATAL_ERROR)

message(STATUS "Building in SuperBuild mode. Builds all qmlOS CMake projects at once.")
if (NOT DEFINED CMAKE_PREFIX_PATH AND NOT DEFINED ENV{CMAKE_PREFIX_PATH})
    message(FATAL_ERROR "CMAKE_PREFIX_PATH environment variable not set. When configuring for the first time, make sure CMAKE_PREFIX_PATH is set to the root of the build directory. It can be done by passing it to cmake as an command line parameter (e.g. cmake -DCMAKE_PREFIX_PATH=path_to_your_build_dir ..) OR by setting the CMAKE_PREFIX_PATH environment variable (e.g. export CMAKE_PREFIX_PATH=path_to_your_build_dir ..).")
endif()

set(USE_SUPERBUILD ON)

add_custom_target(check COMMAND ${CMAKE_CTEST_COMMAND} -VV)

add_subdirectory(greenisland)
add_subdirectory(fluid)
add_subdirectory(libqmlos)
add_subdirectory(qtaccountsservice)
add_subdirectory(shell)
add_subdirectory(workspace)
add_subdirectory(appcenter)
add_subdirectory(settings)
#add_subdirectory(terminal)
add_subdirectory(files)
