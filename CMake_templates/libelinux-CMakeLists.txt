cmake_minimum_required(VERSION 3.0)

set(TARGET **target filename**)

#-----------------------------------------------------------------------------#

find_package(Threads REQUIRED)

#-----------------------------------------------------------------------------#

add_subdirectory()

add_library(${TARGET} STATIC **source files**)

target_link_libraries(${TARGET} ${CMAKE_THREAD_LIBS_INIT}
								**lib**
)

target_include_directories(${TARGET} PRIVATE **dirs**)

#-----------------------------------------------------------------------------#

target_compile_options(${TARGET} PUBLIC -std=gnu++11
										-Wall
										-Werror
										-O2
)

#-----------------------------------------------------------------------------#