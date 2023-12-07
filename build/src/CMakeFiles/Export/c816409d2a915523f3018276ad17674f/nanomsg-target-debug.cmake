#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "nanomsg" for configuration "Debug"
set_property(TARGET nanomsg APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(nanomsg PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/libnanomsg.so.6.0.1"
  IMPORTED_SONAME_DEBUG "libnanomsg.so.6"
  )

list(APPEND _cmake_import_check_targets nanomsg )
list(APPEND _cmake_import_check_files_for_nanomsg "${_IMPORT_PREFIX}/lib/libnanomsg.so.6.0.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
