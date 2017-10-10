// =================== THIS IS A HEADER FILE ===========================
/* It is used to predeclare all classes, functions and variables to be used in the .cpp file.
 * These declarations tell cpp what to expect when you later in a different part of for example the main program.
 * It is needed because cpp needs to know what things do as it meets them in code. Its that stupid
 * (or rather its because it compiles separately from running, which makes it ALOT faster than python)
 */
// =====================================================================
// Im a bit unsure about this, but I think its here as a guard, it checks if PLANET_H is defined
// already (by some previous include-statement another part of the code), and defines the method if it isn't:
#ifndef PLANET_H
#define PLANET_H



#include <armadillo>

// like python:
class planet
{
public: // Public attributes and methods can be accessed from external code, for example with planet.mass

    // Here we declare the (public) attributes of this function, aka variables
    double mass;
    double G;
    arma::vec position[3];
    arma::vec velocity[3];


    // These are constructors, they are called when you create a new object of this class,
    // based on how you call it:
    planet(); // -> for creating a planet with no position, velocity or mass. You then have to set this later
    planet(arma::vec& pos0, arma::vec& vel0, double mass);
    planet(const planet& other); // for creating copies of a planet. Dunno if this works yet.

    // here comes the (public) methods of this class.
    double distance(planet other);
    double gravitationalForce(planet other);
    double acceleration(planet other);
    double kineticEnergy();
    double potentialEnergy(planet other, double epsilon);
    double get_kinetic();   // because we set kinetic and potential to be private. Just for show.
    double get_potential();
/*
 * Private files can't be accessed from outside, but the methods of this class can access them
 */
private:
    // Private attributes:
    double kinetic; // Doesnt need to be private, is just for show.
    double potential;
};

#endif // PLANET_H is fully defined
