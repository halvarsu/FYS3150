TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += \
    cpp/main.cpp \
    cpp/planet.cpp \
    cpp/celestialbody.cpp \
    cpp/solarsystem.cpp \
    cpp/forwardeuler.cpp \
    cpp/integrator.cpp

LIBS += -larmadillo -lblas -llapack

HEADERS += \
    cpp/planet.h \
    cpp/celestialbody.h \
    cpp/solarsystem.h \
    cpp/forwardeuler.h \
    cpp/forwardeuler.h \
    cpp/integrator.h
