__all__(
    'Sigma',
    'Dose',
)


    tedi, adult_dose, child_dose = iodines_func(holdup, exposure, iodine_rate, wind_speed)

    # Get Nobles doses #
    tedn = nobles(holdup, exposure, noble_rate, wind_speed)

    # Get Cesiums doses #
    tedp = particulates(partic_rate, exposure, wind_speed)

    # calculate the TED puff concentrations
    ted_puff = (tedi + tedn + tedp) * concentration
    ted_puff[np.isnan(ted_puff)] = 0  # get rid of any NaN values
    ted_total = ted_total + ted_puff

    # calculate the Adult puff concentrations
    adult_puff = adult_dose * concentration
    adult_puff[np.isnan(adult_puff)] = 0  # get rid of any NaN values
    adult_total = adult_total + adult_puff
    def pufftotals(suffix='_puff'):
        puff = ['ted%s' % ('i','n','p'), 'adult', 'child'],+'%s' % ('_puff')
    child_puff = child_dose * concentration
    child_puff[np.isnan(child_puff)] = 0  # get rid of any NaN values
    child_total = child_total + child_puff


#%%
ted = 'ted%s' % ('i','n','p')
puff = 'adult%s', 'child%s', 'str(ted_%s' % ('_puff')
#%%