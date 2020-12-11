import cdstoolbox as ct
#To be used in CDStoolbox editor
#Code obtained from CDstoolbox application gallery! https://cds.climate.copernicus.eu/toolbox/doc/gallery/index.html 
layout = {
    'input_ncols': 2,
    'input_align': 'top'
}

extent = {
    'Europe': [-11, 35, 34, 60],
    'Arctic': [-180, 180, 70, 90],
    'Mediterranean': [-5.2, 34, 31, 45],
    'Global': [-180, 180, -90, 90],
}

variables = {
    'Surface Latent Heat Flux': 'surface_latent_heat_flux'
}


@ct.application(title='Calculate a regional mean and  anomalies', layout=layout)
@ct.input.dropdown('variable', label='Variable', values=variables.keys())
@ct.input.dropdown('region', label='Region', values=['Europe', 'Arctic', 'Mediterranean', 'Global'])
@ct.output.livefigure()
def compute_anomaly(variable, region):


    data = ct.catalogue.retrieve(
        'projections-cmip5-monthly-single-levels',
        {
            'experiment': 'amip',
            'variable': 'surface_latent_heat_flux',
            'model': 'giss_e2_r',
            'ensemble_member': 'r1i1p1',
            'period': '195101-201012',
        }
    )
    data_daily = ct.climate.monthly_mean(data)

    anomaly = ct.climate.anomaly(data_daily)
    anomaly_region = ct.cdo.fldmean(anomaly, extent=extent[region])

    figure = ct.chart.line(anomaly_region, layout_dict={'title': 'Region: %s' % (region)})

    return figure
