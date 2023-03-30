from __future__ import division, print_function
import pytest
import ghostdr.ghost.polyfit as polyfit
import astropy.io.fits as pyfits
import pdb
import numpy as np

# Most of the testing of polyspect methods is done within test_ghost, as
# GhostArm provides all the necessary instantiation calls. This is easier
# than trying to work out the minimalist calls required ourselves.

# Assert if all the correct attributes of the Polyspect class needed are there
@pytest.mark.ghostunit
def test_polyspect_init():
    with pytest.raises(TypeError):
        # Must provide all init parameters
        _ = polyfit.polyspect.Polyspect()
