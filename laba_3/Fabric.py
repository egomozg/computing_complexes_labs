from Elems import R
from Elems import EDS
from Elems import C
from Elems import L
from Elems import J

class Fabric():

    def serialize(elem, h):
        match elem['type']:
            case 'R':
                return Fabric.R(elem, h)
            case 'E':
                return Fabric.E(elem, h)
            case 'C':
                return Fabric.C(elem, h)
            case 'L':
                return Fabric.L(elem, h)
            case 'J':
                return Fabric.J(elem, h)

    def R(elem, h):
        return R.Resistance(elem, h)

    def E(elem, h):
        return EDS.EDS(elem, h)

    def C(elem, h):
        return C.C(elem, h)

    def L(elem, h):
        return L.L(elem, h)

    def J(elem, h):
        return J.J(elem, h)

