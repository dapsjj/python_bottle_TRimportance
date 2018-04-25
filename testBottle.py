# -*- coding:  utf-8 -*-
import bottle
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy import optimize as opt
import os


def generate(code, year,week):
    kion = pd.read_csv(r'D:/a.csv')
    kion.head()
    Px = np.arange(0, len(kion), 1)
    Py = kion['temp']
    plt.plot(Px, Py)
    res = opt.curve_fit(fit_func, Px, Py)
    a = res[0][0]
    b = res[0][1]
    c = res[0][2]
    d = res[0][3]
    print("a = %s" % a)
    print("b = %s" % b)
    print("c = %s" % c)
    print("d = %s" % d)
    Px2 = []
    for x in Px:
        Px2.append(a * x ** 3 + b * x ** 2 + c * x + d)
    plt.plot(Px, Py)
    plt.plot(Px, np.array(Px2))
    plt.savefig('./image/test.jpg')
    bottle.redirect('/show'+'test')


def fit_func(x, a, b, c, d):
    return a * x ** 3 + b * x ** 2 + c * x + d


@bottle.route('/show<name>')
def server_static(name):
    return bottle.static_file(name+'.jpg', root='./image')


@bottle.route('/index')
def index():
    # currentPath = os.path.dirname(__file__)
    # return bottle.template(currentPath+r'/html/index.html')
    return bottle.template('./html/index.html')

@bottle.route('/css/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='./css')

@bottle.route('/js/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='./js')

@bottle.route('/fonts/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='./fonts')

# @bottle.route('/locales/<filename>')
# def server_static(filename):
#     return bottle.static_file(filename, root='./locales')

@bottle.route('/generate', method='POST')
def get_para():
    enployeeCode = bottle.request.POST.get('employeeCode')
    reportYear = bottle.request.POST.get('reportYear')
    reportWeek = bottle.request.POST.get('reportWeek')
    if enployeeCode and reportYear and reportWeek:
        generate(enployeeCode, reportYear,reportWeek)

@bottle.error(404)
def error404(error):
    return 'Nothing here, sorry'



bottle.run(host='localhost', port=8081)
