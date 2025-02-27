# CMake generated Testfile for 
# Source directory: /home/wangzhao/experiments/deneva/utils/nanomsg
# Build directory: /home/wangzhao/experiments/deneva/build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(inproc "/home/wangzhao/experiments/deneva/build/inproc" "12100")
set_tests_properties(inproc PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;402;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(inproc_shutdown "/home/wangzhao/experiments/deneva/build/inproc_shutdown" "12110")
set_tests_properties(inproc_shutdown PROPERTIES  TIMEOUT "10" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;403;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(ipc "/home/wangzhao/experiments/deneva/build/ipc" "12120")
set_tests_properties(ipc PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;404;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(ipc_shutdown "/home/wangzhao/experiments/deneva/build/ipc_shutdown" "12130")
set_tests_properties(ipc_shutdown PROPERTIES  TIMEOUT "40" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;405;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(ipc_stress "/home/wangzhao/experiments/deneva/build/ipc_stress" "12140")
set_tests_properties(ipc_stress PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;406;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(tcp "/home/wangzhao/experiments/deneva/build/tcp" "12150")
set_tests_properties(tcp PROPERTIES  TIMEOUT "20" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;407;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(tcp_shutdown "/home/wangzhao/experiments/deneva/build/tcp_shutdown" "12160")
set_tests_properties(tcp_shutdown PROPERTIES  TIMEOUT "120" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;408;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(ws "/home/wangzhao/experiments/deneva/build/ws" "12170")
set_tests_properties(ws PROPERTIES  TIMEOUT "20" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;409;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(pair "/home/wangzhao/experiments/deneva/build/pair" "12180")
set_tests_properties(pair PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;412;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(pubsub "/home/wangzhao/experiments/deneva/build/pubsub" "12190")
set_tests_properties(pubsub PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;413;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(reqrep "/home/wangzhao/experiments/deneva/build/reqrep" "12200")
set_tests_properties(reqrep PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;414;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(pipeline "/home/wangzhao/experiments/deneva/build/pipeline" "12210")
set_tests_properties(pipeline PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;415;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(survey "/home/wangzhao/experiments/deneva/build/survey" "12220")
set_tests_properties(survey PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;416;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(bus "/home/wangzhao/experiments/deneva/build/bus" "12230")
set_tests_properties(bus PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;417;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(async_shutdown "/home/wangzhao/experiments/deneva/build/async_shutdown" "12240")
set_tests_properties(async_shutdown PROPERTIES  TIMEOUT "30" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;420;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(block "/home/wangzhao/experiments/deneva/build/block" "12250")
set_tests_properties(block PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;421;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(term "/home/wangzhao/experiments/deneva/build/term" "12260")
set_tests_properties(term PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;422;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(timeo "/home/wangzhao/experiments/deneva/build/timeo" "12270")
set_tests_properties(timeo PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;423;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(iovec "/home/wangzhao/experiments/deneva/build/iovec" "12280")
set_tests_properties(iovec PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;424;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(msg "/home/wangzhao/experiments/deneva/build/msg" "12290")
set_tests_properties(msg PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;425;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(prio "/home/wangzhao/experiments/deneva/build/prio" "12300")
set_tests_properties(prio PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;426;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(poll "/home/wangzhao/experiments/deneva/build/poll" "12310")
set_tests_properties(poll PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;427;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(device "/home/wangzhao/experiments/deneva/build/device" "12320")
set_tests_properties(device PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;428;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(device4 "/home/wangzhao/experiments/deneva/build/device4" "12330")
set_tests_properties(device4 PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;429;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(device5 "/home/wangzhao/experiments/deneva/build/device5" "12340")
set_tests_properties(device5 PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;430;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(device6 "/home/wangzhao/experiments/deneva/build/device6" "12350")
set_tests_properties(device6 PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;431;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(device7 "/home/wangzhao/experiments/deneva/build/device7" "12360")
set_tests_properties(device7 PROPERTIES  TIMEOUT "30" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;432;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(emfile "/home/wangzhao/experiments/deneva/build/emfile" "12370")
set_tests_properties(emfile PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;433;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(domain "/home/wangzhao/experiments/deneva/build/domain" "12380")
set_tests_properties(domain PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;434;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(trie "/home/wangzhao/experiments/deneva/build/trie" "12390")
set_tests_properties(trie PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;435;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(list "/home/wangzhao/experiments/deneva/build/list" "12400")
set_tests_properties(list PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;436;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(hash "/home/wangzhao/experiments/deneva/build/hash" "12410")
set_tests_properties(hash PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;437;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(stats "/home/wangzhao/experiments/deneva/build/stats" "12420")
set_tests_properties(stats PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;438;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(symbol "/home/wangzhao/experiments/deneva/build/symbol" "12430")
set_tests_properties(symbol PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;439;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(separation "/home/wangzhao/experiments/deneva/build/separation" "12440")
set_tests_properties(separation PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;440;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(zerocopy "/home/wangzhao/experiments/deneva/build/zerocopy" "12450")
set_tests_properties(zerocopy PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;441;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(shutdown "/home/wangzhao/experiments/deneva/build/shutdown" "12460")
set_tests_properties(shutdown PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;442;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(cmsg "/home/wangzhao/experiments/deneva/build/cmsg" "12470")
set_tests_properties(cmsg PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;443;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(bug328 "/home/wangzhao/experiments/deneva/build/bug328" "12480")
set_tests_properties(bug328 PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;444;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(bug777 "/home/wangzhao/experiments/deneva/build/bug777" "12490")
set_tests_properties(bug777 PROPERTIES  TIMEOUT "5" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;445;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(ws_async_shutdown "/home/wangzhao/experiments/deneva/build/ws_async_shutdown" "12500")
set_tests_properties(ws_async_shutdown PROPERTIES  TIMEOUT "10" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;446;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(reqttl "/home/wangzhao/experiments/deneva/build/reqttl" "12510")
set_tests_properties(reqttl PROPERTIES  TIMEOUT "10" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;447;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
add_test(surveyttl "/home/wangzhao/experiments/deneva/build/surveyttl" "12520")
set_tests_properties(surveyttl PROPERTIES  TIMEOUT "10" _BACKTRACE_TRIPLES "/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;396;add_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;448;add_libnanomsg_test;/home/wangzhao/experiments/deneva/utils/nanomsg/CMakeLists.txt;0;")
subdirs("src")
