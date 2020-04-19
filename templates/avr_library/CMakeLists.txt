cmake_minimum_required(VERSION 3.0)

set(TARGET **target name**)

#-----------------------------------------------------------------------------#

add_subdirectory()

add_library(${TARGET} STATIC **source files**)

target_link_libraries(${TARGET} **lib**)
target_include_directories(${TARGET} PRIVATE **dirs**)

#-----------------------------------------------------------------------------#

target_compile_options(${TARGET} PUBLIC -mmcu=${MCU}
										-std=gnu11
										-O2
										-Wall
										-Werror
)

target_compile_definitions(${TARGET} PUBLIC F_CPU=${F_CPU})

#-----------------------------------------------------------------------------#

#install(TARGETS ${TARGET} DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/bin)