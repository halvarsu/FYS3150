TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += main.cpp \
    solve.cpp \
    tests/tests.cpp \
    tests/tests_main.cpp \
    hamilton_solver.cpp

HEADERS += solve.h catch.hpp

LIBS += -larmadillo -llapack -lblas
