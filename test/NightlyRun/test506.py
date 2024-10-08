#Test Name: PigTranHO
from model import *
from socket import gethostname
from triangle import *
from setmask import *
from parameterize import *
from setflowequation import *
from solve import *


md = triangle(model(), '../Exp/Pig.exp', 30000.)
md = setmask(md, '../Exp/PigShelves.exp', '../Exp/PigIslands.exp')
md = parameterize(md, '../Par/Pig.py')
md.mesh.scale_factor = 0.9 * np.ones((md.mesh.numberofvertices))
md.extrude(2, 1.)
md = setflowequation(md, 'HO', 'all')
md.transient.requested_outputs = ['default', 'IceVolume', 'IceVolumeScaled', 'GroundedArea', 'GroundedAreaScaled', 'FloatingArea', 'FloatingAreaScaled', 'TotalSmb', 'TotalSmbScaled', 'TotalFloatingBmb', 'TotalFloatingBmbScaled']
md.cluster = generic('name', gethostname(), 'np', 3)
md = solve(md, 'Transient')

# Fields and tolerances to track changes
field_names = [
    'Vx1', 'Vy1', 'Vz1', 'Vel1', 'Pressure1', 'Bed1', 'Surface1', 'Thickness1', 'Temperature1', 'BasalforcingsGroundediceMeltingRate1', 'IceVolume1', 'IceVolumeScaled1', 'GroundedArea1', 'GroundedAreaScaled1', 'FloatingArea1', 'FloatingAreaScaled1', 'TotalSmb1', 'TotalSmbScaled1', 'TotalFloatingBmb1', 'TotalFloatingBmbScaled1',
    'Vx2', 'Vy2', 'Vz2', 'Vel2', 'Pressure2', 'Bed2', 'Surface2', 'Thickness2', 'Temperature2', 'BasalforcingsGroundediceMeltingRate2', 'IceVolume2', 'IceVolumeScaled2', 'GroundedArea2', 'GroundedAreaScaled2', 'FloatingArea2', 'FloatingAreaScaled2', 'TotalSmb2', 'TotalSmbScaled2', 'TotalFloatingBmb2', 'TotalFloatingBmbScaled2']
field_tolerances = [
    1e-10, 1e-10, 1e-10, 1e-10, 1e-12, 1e-11, 2e-12, 1e-11, 1e-12, 1e-09, 2e-13, 2e-13, 1e-13, 1e-13, 1e-13, 1e-13, 1e-13, 1e-13, 1e-13, 1e-13,
    2e-11, 2e-11, 1e-09, 1e-11, 1e-11, 1e-10, 1e-11, 1e-10, 1e-11, 2e-08, 2e-13, 2e-13, 1e-13, 1e-13, 1e-13, 1e-13, 1e-13, 1e-13, 1e-13, 1e-13]
field_values = [md.results.TransientSolution[0].Vx,
                md.results.TransientSolution[0].Vy,
                md.results.TransientSolution[0].Vz,
                md.results.TransientSolution[0].Vel,
                md.results.TransientSolution[0].Pressure,
                md.results.TransientSolution[0].Base,
                md.results.TransientSolution[0].Surface,
                md.results.TransientSolution[0].Thickness,
                md.results.TransientSolution[0].Temperature,
                md.results.TransientSolution[0].BasalforcingsGroundediceMeltingRate,
                md.results.TransientSolution[0].IceVolume,
                md.results.TransientSolution[0].IceVolumeScaled,
                md.results.TransientSolution[0].GroundedArea,
                md.results.TransientSolution[0].GroundedAreaScaled,
                md.results.TransientSolution[0].FloatingArea,
                md.results.TransientSolution[0].FloatingAreaScaled,
                md.results.TransientSolution[0].TotalSmb,
                md.results.TransientSolution[0].TotalSmbScaled,
                md.results.TransientSolution[0].TotalFloatingBmb,
                md.results.TransientSolution[0].TotalFloatingBmbScaled,
                md.results.TransientSolution[1].Vx,
                md.results.TransientSolution[1].Vy,
                md.results.TransientSolution[1].Vz,
                md.results.TransientSolution[1].Vel,
                md.results.TransientSolution[1].Pressure,
                md.results.TransientSolution[1].Base,
                md.results.TransientSolution[1].Surface,
                md.results.TransientSolution[1].Thickness,
                md.results.TransientSolution[1].Temperature,
                md.results.TransientSolution[1].BasalforcingsGroundediceMeltingRate,
                md.results.TransientSolution[1].IceVolume,
                md.results.TransientSolution[1].IceVolumeScaled,
                md.results.TransientSolution[1].GroundedArea,
                md.results.TransientSolution[1].GroundedAreaScaled,
                md.results.TransientSolution[1].FloatingArea,
                md.results.TransientSolution[1].FloatingAreaScaled,
                md.results.TransientSolution[1].TotalSmb,
                md.results.TransientSolution[1].TotalSmbScaled,
                md.results.TransientSolution[1].TotalFloatingBmb,
                md.results.TransientSolution[1].TotalFloatingBmbScaled]
