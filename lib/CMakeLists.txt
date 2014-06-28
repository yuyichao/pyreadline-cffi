set(pyreadline_SRCS
  readline.cpp)

add_library(pyreadline SHARED
  ${pyreadline_SRCS})

# TODO
target_link_libraries(pyreadline readline history)

set_target_properties(pyreadline PROPERTIES
  COMPILE_FLAGS "-fvisibility=hidden"
  LINK_FLAGS "-Wl,--no-undefined"
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
  PREFIX ""
  OUTPUT_NAME "_pyreadline")

install(TARGETS pyreadline LIBRARY
  DESTINATION "${PYREADLINE_DIR}/readline")
install(FILES readline_api.h
  DESTINATION "${PYREADLINE_DIR}/readline")
