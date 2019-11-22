cmake_minimum_required(VERSION 3.0)

#-----------------------------------------------------------------------------#
find_package(OpenCV REQUIRED)
#-----------------------------------------------------------------------------#

add_subdirectory()

set(TARGET **target filename**)

add_executable(${TARGET} **source files**)
add_library(${TARGET} STATIC **source files**)
target_link_libraries(${TARGET} **lib**)
target_include_directories(${TARGET} PUBLIC **dirs**)

#-----------------------------------------------------------------------------#
target_compile_options(${TARGET} PUBLIC -std=gnu++11
										-Wall
										-Werror
										-O2
)
#-----------------------------------------------------------------------------#