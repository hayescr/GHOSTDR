"""
Recipes available to data with tags ``['GHOST', 'CAL', 'SLITV', 'ARC']``.
Default is ``makeProcessedSlitArc``, which is an alias to
:any:`makeProcessedSlit`.
"""
recipe_tags = set(['GHOST', 'CAL', 'SLITV', 'ARC'])

from .recipes_SLITV import makeProcessedSlit

def makeProcessedSlitArc(p):
    """
    This recipe performs the standardization and corrections needed to convert
    the raw input arc images into a single stacked arc image. This output
    processed arc is stored on disk using storeProcessedArc and has a name
    equal to the name of the first input arc image with "_arc.fits" appended.

    Parameters
    ----------
    p : Primitives object
        A primitive set matching the recipe_tags.
    """

    p.prepare()
    p.addDQ()
    p.addVAR(read_noise=True)
    p.biasCorrect()
    p.addVAR(poisson_noise=True)
    p.ADUToElectrons()
    p.darkCorrect()
    # p.correctSlitCosmics()
    p.stackFrames(operation='median', reject_method='none', apply_dq=True)
    p.storeProcessedArc()
    return

makeProcessedSlitArc = makeProcessedSlit

default = makeProcessedSlitArc
