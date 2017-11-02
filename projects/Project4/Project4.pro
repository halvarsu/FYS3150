TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += \
    cpp/main.cpp \
    cpp/metropolis.cpp \
    cpp/tools.cpp

HEADERS += \
    cpp/metropolis.h \
    cpp/tools.h

LIBS += -larmadillo -lblas -llapack
