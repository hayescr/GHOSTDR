"""
Recipes available to data with tags ``['GHOST', 'SLITV']``.
Default is ``makeProcessedSlit``.
"""
recipe_tags = set(['GHOST', 'SLITV'])

def makeProcessedSlit(p):
    """
    This recipe processes GHOST science data.

    Parameters
    ----------
    p : Primitives object
        A primitive set matching the recipe_tags.
    """

    p.prepare()
    p.addDQ()
    p.addVAR(read_noise=True)
    p.biasCorrect()
    p.ADUToElectrons()
    p.addVAR(poisson_noise=True)
    p.darkCorrect()
    #p.correctSlitCosmics()
    p.processSlits()
    p.stackFrames(apply_dq=True)
    p.storeProcessedSlit()
    return

default = makeProcessedSlit
