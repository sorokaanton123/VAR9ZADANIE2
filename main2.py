import urllib.request
import os
from scipy import special
import numpy as np
import re
import matplotlib.pyplot as plt
import xml.etree.cElementTree as ET


def h(n, x):
    return special.spherical_jn(n, x) + 1j * special.spherical_yn(n, x)


def a(n, x):
    return special.spherical_jn(n, x)/h(n, k*r)


def b(n, x):
    return (x * special.spherical_jn(n-1, x) - n * special.spherical_jn(n, x)) / (x * h(n - 1, x) - n * h(n, x))


def sigma(povtor, x):
    sigm = 0
    for n in range(1, povtor):
        sigm = sigm + np.power(-1, n)*(n+0.5)*(b(n, x)-a(n, x))
        print('n= ', n)
    return sigm


if __name__ == '__main__':
    url = 'https://jenyay.net/uploads/Student/Modelling/task_02.txt'

    if 'results' not in os.listdir():
        os.makedirs(os.path.join(os.getcwd(), 'results'))
    urllib.request.urlretrieve(url, 'results/results2.xml')

    with open('results/results2.xml', 'r') as file:
        book = file.readlines()

    var = int(input('Введите ваш вариант: '))
    var -= 1
    shkala = int(input('Введите приближение(число шагов): '))
    print(book[var])
    print(re.findall('\d+[.]*\d*e*[-]*\d*', book[var]))
    book1 = re.findall('\d+[.]*\d*e*[-]*\d*', book[var])
    D = float(book1[1])
    print('D= ', D)
    fmin = float(book1[2])
    print('fmin= ', fmin)
    fmax = float(book1[3])
    print('fmax= ', fmax)
    r = D/2
    print('r= ', r)
    f = np.linspace(fmin, fmax, shkala)
    print('f= ', f)
    lamda = 3*10**8/f
    print('lamda= ', lamda)
    k = 2*np.pi/lamda
    print('k= ', k)
    result = lamda**2/np.pi*abs(sigma(70, k*r))**2
    print('sigma = ',result)

    root = ET.Element("data")
    freq = ET.SubElement(root, "frequencydata")

    for i in range(shkala):
        ET.SubElement(freq, "f").text = "{}".format(f[i])

    lam = ET.SubElement(root, "lambdadata")

    for i in range(shkala):
        ET.SubElement(lam, "lambda").text = "{}".format(lamda[i])

    rc = ET.SubElement(root, "rcsdata")

    for i in range(shkala):
        ET.SubElement(rc, "rcs").text = "{}".format(result[i])

    tree = ET.ElementTree(root)
    ET.indent(tree, '  ')
    tree.write("results.xml", encoding="utf-8", xml_declaration=True)

    plt.plot(2*np.pi*r / lamda, result/(np.pi*r**2))
    plt.show()
    plt.plot(f, result)
    plt.show()
