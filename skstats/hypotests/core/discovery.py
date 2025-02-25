from scipy.stats import norm

from .basetest import BaseTest


class Discovery(BaseTest):
    def __init__(self, calculator, poinull):
        """Class for discovery test.

            Args:
                calculator (`sktats.hypotests.BaseCalculator`): calculator to use for computing the pvalues
                poinull (List[`hypotests.POI`]): parameters of interest for the null hypothesis

            Example with `zfit`:
                >>> import zfit
                >>> from zfit.core.loss import ExtendedUnbinnedNLL
                >>> from zfit.minimize import MinuitMinimizer

                >>> bounds = (0.1, 3.0)
                >>> zfit.Space('x', limits=bounds)

                >>> bkg = np.random.exponential(0.5, 300)
                >>> peak = np.random.normal(1.2, 0.1, 25)
                >>> data = np.concatenate((bkg, peak))
                >>> data = data[(data > bounds[0]) & (data < bounds[1])]
                >>> N = data.size
                >>> data = zfit.data.Data.from_numpy(obs=obs, array=data)

                >>> lambda_ = zfit.Parameter("lambda", -2.0, -4.0, -1.0)
                >>> Nsig = zfit.Parameter("Ns", 20., -20., N)
                >>> Nbkg = zfit.Parameter("Nbkg", N, 0., N*1.1)
                >>> signal = Nsig * zfit.pdf.Gauss(obs=obs, mu=1.2, sigma=0.1)
                >>> background = Nbkg * zfit.pdf.Exponential(obs=obs, lambda_=lambda_)
                >>> loss = ExtendedUnbinnedNLL(model=[signal + background], data=[data], fit_range=[obs])

                >>> from skstats.hypotests.calculators import AsymptoticCalculator
                >>> from skstats.hypotests import Discovery
                >>> from skstats.hypotests.parameters import POI

                >>> calculator = AsymptoticCalculator(loss, MinuitMinimizer())
                >>> poinull = POI(Nsig, 0)
                >>> discovery_test = Discovery(calculator, [poinull])
                >>> discovery_test.result()
                p_value for the Null hypothesis = 0.0007571045424956679
                Significance (in units of sigma) = 3.1719464825102244
        """
        super(Discovery, self).__init__(calculator, poinull)

    def result(self, printlevel=1):
        """
        Returns the result of the discovery hypothesis test.

            Args:
                printlevel (int, default=1): if > 0 print the result

            Returns:
                Tuple(float, float): pnull, significance
        """
        pnull, _ = self.calculator.pvalue(self.poinull, onesideddiscovery=True)
        pnull = pnull[0]

        significance = norm.ppf(1. - pnull)

        if printlevel > 0:
            print("\np_value for the Null hypothesis = {0}".format(pnull))
            print("Significance (in units of sigma) = {0}".format(significance))

        return pnull, significance
