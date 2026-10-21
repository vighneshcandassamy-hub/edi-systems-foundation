"""Constructed bug/tree world. Evaluator-side code, never a participant input.

Coefficients are engineering assumptions for a development environment. They
are not fitted ecological estimates or a reproduction of Meadows' equations.
"""
import math
import random

VERSION = 'bug-tree-development-world-0.1'

def initial_state(rng):
    return dict(insects=rng.uniform(.10,.18), foliage=rng.uniform(.84,.96),
                mature_host=rng.uniform(.12,.25), enemies=rng.uniform(.45,.55))

def step(state, weather, spray=0., conversion=0., *, nuisance=None):
    # Nuisance values are intentionally not read by any state transition.
    b,f,h,p=(state[k] for k in ('insects','foliage','mature_host','enemies'))
    capacity=(.4+14*h)*max(f,.1)
    consumed=2*p*b*b/(.4*.4+b*b)
    growth=max(.4,1.15+.45*weather)*b*(1-b/max(capacity,.1))
    damage=min(.7,.12*b/(.5+f))
    result={
        'insects':max(.015,min(25.,b+growth-consumed-.78*spray*b)),
        'foliage':max(.05,min(1.,f+.1*(1-f)-damage*f-.22*conversion)),
        'mature_host':max(.08,min(.95,h+.025*(1-h)-.025*damage*h-conversion)),
        'enemies':max(.05,min(1.5,p+.1*(.2+.6*b/(.5+b)-p)))}
    return result, {'foliage_loss_fraction':damage,'consumption_index':consumed,
                    'spending_units':.8*spray+8*conversion}

def history(seed, plots=8, years=60):
    rng=random.Random(seed);states=[initial_state(rng) for _ in range(plots)]
    rows=[]
    for year in range(1,years+1):
        warm=3. if year in (18,19,20,36,37,38,54,55,56) else 0.
        weather=rng.gauss(0,.4)+warm
        for j,state in enumerate(states):
            spray=.85 if state['insects']>1. else 0.
            next_state,metrics=step(state,weather,spray)
            rows.append(dict(year=year,plot=f'P{j+1:02d}',weather=weather,spray=spray,
                             **state,**metrics))
            states[j]=next_state
    return rows,states

POLICIES={
    'continue': {'spray_trigger':1.0,'spray_strength':.85,'annual_conversion':0.0},
    'intensive': {'spray_trigger':.30,'spray_strength':.95,'annual_conversion':0.0},
    'diversify': {'spray_trigger':25.,'spray_strength':0.,'annual_conversion':.045},
    'combined': {'spray_trigger':.8,'spray_strength':.85,'annual_conversion':.035},
    'observe': {'spray_trigger':25.,'spray_strength':0.,'annual_conversion':0.0}}

def rollout(states, policy, future_weather):
    states=[dict(s) for s in states];rows=[]
    for j,weather in enumerate(future_weather,61):
        current=[]
        for state in states:
            spray=policy['spray_strength'] if state['insects']>policy['spray_trigger'] else 0.
            state_next,m=step(state,weather,spray,policy['annual_conversion'])
            current.append(state_next)
            rows.append(dict(year=j,**m,**state_next))
        states=current
    n=len(rows);loss=sum(x['foliage_loss_fraction'] for x in rows)/n
    cost=sum(x['spending_units'] for x in rows)/n
    terminal=sum(s['foliage'] for s in states)/len(states)
    budget_violation=max(0.,max(x['spending_units'] for x in rows)-1.1)
    stock_violation=max(0.,.40-terminal)
    objective=loss+.20*cost+5*stock_violation+5*budget_violation
    return dict(objective=objective,mean_foliage_loss=loss,mean_spending=cost,
                terminal_foliage=terminal,budget_violation=budget_violation,
                stock_violation=stock_violation,
                next_year_mean_insects=sum(x['insects'] for x in rows[:len(states)])/len(states))

def future(seed):
    r=random.Random(seed+9182)
    return [r.gauss(0,.4)+(2.7 if j in (2,3,4) else 0.) for j in range(10)]
