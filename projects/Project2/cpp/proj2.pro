TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += main.cpp \
    solve.cpp \
    tests/test.cpp

HEADERS += solve.h catch.hpp \
    main.h

LIBS += -larmadillo -llapack -lblas
