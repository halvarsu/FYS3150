TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += \
    cpp/main.cpp \
    cpp/planet.cpp \
    cpp/celestialbody.cpp \
    cpp/solarsystem.cpp \
    cpp/integrators/forwardeuler.cpp \
    cpp/celestialbody.cpp \
    cpp/forwardeuler.cpp \
    cpp/main.cpp \
    cpp/planet.cpp \
    cpp/solarsystem.cpp \
    cpp/integrators/forwardeuler.cpp \
    cpp/integrators/integratorbase.cpp

LIBS += -larmadillo -lblas -llapack

HEADERS += \
    cpp/planet.h \
    cpp/celestialbody.h \
    cpp/solarsystem.h \
    cpp/forwardeuler.h \
    cpp/celestialbody.h \
    cpp/forwardeuler.h \
    cpp/planet.h \
    cpp/solarsystem.h \
    cpp/integrators/forwardeuler.h \
    cpp/integrators/integratorbase.h
