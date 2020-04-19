cmake_minimum_required(VERSION 3.0)

set(TARGET **target filename**)

#-----------------------------------------------------------------------------#

find_package(OpenCV REQUIRED)

#-----------------------------------------------------------------------------#

add_subdirectory()

add_library(${TARGET} STATIC **source files**)

target_link_libraries(${TARGET} ${OpenCV_LIBS} 
								**lib**
)

target_include_directories(${TARGET} PRIVATE ${OpenCV_INCLUDE_DIRS}
											**dirs**
)

#-----------------------------------------------------------------------------#

target_compile_options(${TARGET} PUBLIC -std=gnu++11
										-Wall
										-Werror
										-O2
)

#-----------------------------------------------------------------------------#

#install(TARGETS ${TARGET} DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/bin)