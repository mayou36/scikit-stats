import pytest
import numpy as np
import zfit
from zfit.core.testing import setup_function  # allows redefinition of zfit.Parameter, needed for tests
from zfit.core.loss import UnbinnedNLL
from zfit.minimize import Minuit

from skstats.hypotests.calculators.basecalculator import BaseCalculator
from skstats.hypotests.core.basetest import BaseTest
from skstats.hypotests.parameters import POI


def create_loss():

    obs = zfit.Space('x', limits=(0.1, 2.0))
    data = zfit.data.Data.from_numpy(obs=obs, array=np.random.normal(1.2, 0.1, 10000))
    mean = zfit.Parameter("mu", 1.2)
    sigma = zfit.Parameter("sigma", 0.1)
    model = zfit.pdf.Gauss(obs=obs, mu=mean, sigma=sigma)
    loss = UnbinnedNLL(model=[model], data=[data], fit_range=[obs])

    return loss, (mean, sigma)


def test_constructor():
    with pytest.raises(TypeError):
        BaseTest()

    loss, (mean, sigma) = create_loss()
    calculator = BaseCalculator(loss, Minuit())

    poimean_1 = POI(mean, [1.0, 1.1, 1.2, 1.3])
    poimean_2 = POI(mean, [1.2])

    poisigma_1 = POI(sigma, [0.06, 0.08, 0.01, 0.012, 0.014])
    poisigma_2 = POI(sigma, [0.1])

    with pytest.raises(TypeError):
        BaseTest(calculator)

    with pytest.raises(ValueError):
        BaseTest(calculator, poimean_1)

    with pytest.raises(ValueError):
        BaseTest(calculator, [poimean_1], poimean_2)

    with pytest.raises(ValueError):
        BaseTest(calculator, [poimean_1], [poisigma_2])

    with pytest.raises(ValueError):
        BaseTest(calculator, [poisigma_1], [poimean_2])


def test_attributes():

    loss, (mean, sigma) = create_loss()
    calculator = BaseCalculator(loss, Minuit())

    poimean_1 = POI(mean, [1.0, 1.1, 1.2, 1.3])
    poimean_2 = POI(mean, [1.2])

    test = BaseTest(calculator, [poimean_1], [poimean_2])

    assert test.poinull == [poimean_1]
    assert test.poialt == [poimean_2]
    assert test.calculator == calculator
