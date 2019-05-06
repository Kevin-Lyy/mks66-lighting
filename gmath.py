import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    color = []

    normalize(normal)
    normalize(light[LOCATION])
    normalize(view)

    amb = calculate_ambient(ambient, areflect)
    dif = calculate_diffuse(light, dreflect, normal)
    spec = calculate_specular(light, sreflect, view, normal)


    [color.append( amb[i] + dif[i] + spec[i]) for i in range(3)]
    return limit_color(color)

def calculate_ambient(alight, areflect):
    amb = []
    [amb.append(int(alight[i] * areflect[i])) for i in range(3)]

    return limit_color(amb)

def calculate_diffuse(light, dreflect, normal):
    dif = []
    dot = dot_product( light[LOCATION], normal)
    [dif.append(light[COLOR][i] * dreflect[i] * dot) for i in range(3)]
    
    return limit_color(dif)

def calculate_specular(light, sreflect, view, normal):
    col = [0,0,0]
    t = [0,0,0]

    c = 2 * dot_product(light[LOCATION], normal)
    for i in range(len(t)):
        t[i] = normal[i] * c - light[LOCATION][i]

    c = (dot_product(t, view))
    if c > 0:
        c = c
    else:
        c = 0
    c = pow(c, SPECULAR_EXP)

    for i in range(len(col)):
        col[i] = light[COLOR][i] * sreflect[i] * c

    return limit_color(col)

def limit_color(color):
    return [ int((max(0, min(x, 255)))) for x in color]

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude
    return vector

def scale(vector, const):
    return [vector[0] * const, vector[1] * const, vector[2] * const]

def subtract(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
