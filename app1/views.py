from django.shortcuts import render, redirect
from .model import *
import numpy as np

import skfuzzy as fuzz
from skfuzzy import control as ctrl
# Create your views here.

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

# New Antecedent/Consequent objects hold universe variables and membership
# functions
quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

# Auto-membership function population is possible with .automf(3, 5, or 7)
quality.automf(3)
service.automf(3)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])

rule1 = ctrl.Rule(quality['poor'] | service['poor'], tip['low'])
rule2 = ctrl.Rule(service['average'], tip['medium'])
rule3 = ctrl.Rule(service['good'] | quality['good'], tip['high'])

tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)


def loginview(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(request, 'predictfunc.html')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def predictfunc(request):
    return render(request, "predictfunc.html")


def app1homepage(request):

    return render(request, 'app1homepage.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def predictcount(request):
    try:

        serviceInput = request.GET.get("service", "")
        qualityInput = request.GET.get("quality", "")
        print(serviceInput)
        print(qualityInput)
        serviceInput = float(serviceInput)
        qualityInput = float(qualityInput)
        if((serviceInput>10) or (qualityInput>10)):
          raise

        tipping.input['quality'] = qualityInput
        tipping.input['service'] = serviceInput

        # Crunch the numbers
        tipping.compute()

        result1 = 'The resulting suggested tip is ' + \
            str(round(tipping.output['tip'],2)) + ' % of your bill value'
        passdict = {'result': result1,'quality':str(qualityInput),'service':str(serviceInput)}

        return render(request, 'predict.html',
                      passdict
                      )
    except:
        return render(request, 'predict.html',
                      {'result': "Error Occured: Please check the input"}
                      )
