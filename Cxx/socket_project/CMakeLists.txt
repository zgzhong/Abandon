cmake_minimum_required(VERSION 3.10)
project(socket_project)

set(CMAKE_CXX_STANDARD 11)

add_executable(client client.cc global.h peer.h peer.cc)

add_executable(aws aws.cc global.h peer.cc peer.h aws.h server_util.h)

add_executable(monitor monitor.cc global.h peer.cc peer.h)

add_executable(serverA serverA.cc server_util.h global.h peer.h peer.cc)

add_executable(serverB serverB.cc server_util.h global.h peer.h peer.cc)

add_executable(serverC serverC.cc server_util.h global.h peer.h peer.cc)
