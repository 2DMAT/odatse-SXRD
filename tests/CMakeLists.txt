add_test(
  NAME mapper
  COMMAND sh do.sh
  WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/tests/mapper
  )

add_test(
  NAME minsearch
  COMMAND sh do.sh
  WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/tests/minsearch
  )
