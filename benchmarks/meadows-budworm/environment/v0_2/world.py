"""Operator-side constructed ecology. Parameters are assumptions, not fitted estimates."""
import hashlib
import math

VERSION = 'constructed-forest-0.2'


def noise(seed, *keys):
    data = '|'.join(map(str, (seed,) + keys)).encode()
    return int.from_bytes(hashlib.sha256(data).digest()[:8], 'big') / 2**64


def clamp(x, low=0., high=1.):
    return max(low, min(high, x))


def climate(seed, year):
    return {'temperature_anomaly_C': round(2.6 * (noise(seed, 'temperature', year) - .5) +
            (2. if year % 23 in (10, 11, 12) else 0.), 3),
            'spring_rain_mm': round(45 + 85 * noise(seed, 'rain', year), 2)}


def initial(seed):
    plots = []
    for i in range(12):
        fir = .35 + .3 * noise(seed, 'fir', i)
        spruce = .15 + .1 * noise(seed, 'spruce', i)
        plots.append({'id': 'S%02d' % (i + 1), 'x': i % 4, 'y': i // 4,
            'fir': fir, 'spruce': spruce, 'birch': 1 - fir - spruce,
            'foliage': .85, 'insects': .12 + .2 * noise(seed, 'insects', i),
            'enemies': .55 + .2 * noise(seed, 'enemies', i), 'stress': 0., 'age': 35. + 4 * i})
    return plots


def step(plot, weather, treatment=None, harvest=0.):
    """One annual step; direct non-target mortality is explicit and method-dependent."""
    p = dict(plot)
    treatment = treatment or {'dose': 0., 'method': 'broad'}
    dose = treatment['dose']
    broad = treatment['method'] == 'broad'
    kill = .88 if broad else .65
    non_target = .65 if broad else .06
    b, e, f = p['insects'], p['enemies'], p['foliage']
    host = p['fir'] + .45 * p['spruce']
    available = max(.03, host * f)
    capacity = .6 + 13 * available
    warmth = .17 * weather['temperature_anomaly_C'] + .003 * (90 - weather['spring_rain_mm'])
    growth = (2.3 + warmth) * b * (1 - b / capacity)
    consumption = 2.3 * e * b * b / (.35**2 + b * b)
    bnext = clamp(b + growth - consumption - kill * dose * b, .008, 30.)
    enext = clamp((e + .18 * (.25 + .65 * b / (.7 + b) - e)) * (1 - non_target * dose), .01, 1.8)
    damage = clamp(.15 * b / (.35 + available), 0., .8)
    stress = .7 * p['stress'] + .3 * damage
    mortality = clamp(.18 * max(0., stress - .25), 0., .12)
    fir_loss = p['fir'] * mortality + harvest * p['fir']
    spruce_loss = p['spruce'] * mortality * .35 + harvest * p['spruce']
    birch = clamp(p['birch'] + .75 * (fir_loss + spruce_loss) - .012 * p['birch'])
    fir = clamp(p['fir'] - fir_loss + .012 * p['birch'])
    spruce = clamp(p['spruce'] - spruce_loss + .25 * (fir_loss + spruce_loss))
    total = fir + spruce + birch
    p.update(insects=bnext, enemies=enext,
        foliage=clamp(f + .14 * (1 - f) - damage * f - .15 * harvest, .025, 1.),
        fir=fir / total, spruce=spruce / total, birch=birch / total,
        stress=stress, age=max(0., p['age'] + 1 - harvest * p['age']))
    return p, {'damage_fraction': damage, 'natural_enemy_consumption': consumption,
               'host_mortality_fraction': mortality, 'timber_units': 100 * harvest * host,
               'protection_cost': dose * (8 if broad else 11), 'harvest_cost': 5 * harvest}


def history(seed=7021, years=80):
    plots = initial(seed)
    rows = []
    for year in range(-years + 1, 1):
        weather = climate(seed, year)
        next_plots = []
        for p in plots:
            dose = .8 if year >= -25 and p['insects'] > .6 else 0.
            nxt, metrics = step(p, weather, {'dose': dose, 'method': 'broad'})
            rows.append({'year': year, 'plot': p['id'], **nxt, **weather, **metrics,
                         'treatment_dose': dose, 'method': 'broad'})
            next_plots.append(nxt)
        plots = next_plots
    return rows, plots


def observe(seed, year, plot, metric, occurrence):
    units = {'insects': 'larvae per 75 cm branch', 'enemies': 'standardized trap activity index',
             'foliage': 'fraction of baseline host foliage', 'fir': 'fraction of stand',
             'spruce': 'fraction of stand', 'birch': 'fraction of stand', 'age': 'years'}
    if metric not in units:
        raise ValueError('Unsupported instrument metric')
    error = .06 * (2 * noise(seed, 'measurement', year, plot['id'], metric, occurrence) - 1)
    return {'plot': plot['id'], 'year': year, 'metric': metric,
            'value': round(max(0., plot[metric] * (1 + error)), 5),
            'unit': units[metric], 'relative_error_bound': .06,
            'origin': 'constructed_measurement'}
