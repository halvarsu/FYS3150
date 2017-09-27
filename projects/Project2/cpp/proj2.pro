TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += main.cpp \
    solve.cpp \
    tests/tests.cpp \
    solver.cpp \
    tests/tests_main.cpp

HEADERS += solve.h catch.hpp \
    solver.h

LIBS += -larmadillo -llapack -lblas
