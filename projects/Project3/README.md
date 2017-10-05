# Project 3

## Setup

This project uses [Qt creator](https://www1.qt.io/download/ "Qt creator download") for project management and building.

To setup, you need to configure your project manually (yes its tedious, sorry...).  After git clone, open Project3 in qt creator. Then do the following:
    - under Projects/Run/Deployment/ add a custom buildstep with the
      following parameters:

```
    Command: mkdir
    Arguments: -p out
    Working directory: %{buildDir}
```

    - under Projects/Run/Run/ set Working Directory to the project folder,


