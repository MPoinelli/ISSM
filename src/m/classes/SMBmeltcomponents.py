import numpy as np

from checkfield import *
from fielddisplay import fielddisplay
from project3d import *
from WriteData import *


class SMBmeltcomponents(object):
    """SMBMELTCOMPONENTS class definition

    Usage:
        SMBmeltcomponents = SMBmeltcomponents();
    """

    def __init__(self, *args):  # {{{
        self.accumulation      = np.nan
        self.evaporation       = np.nan
        self.melt              = np.nan
        self.refreeze          = np.nan
        self.steps_per_step    = 1
        self.averaging         = 0
        self.requested_outputs = []

        if len(args) == 0:
            self.setdefaultparameters()
        else:
            error('constructor not supported')
    # }}}

    def __repr__(self):  # {{{
        s = '   surface forcings parameters with melt (SMB = accumulation-evaporation-melt+refreeze) :\n'
        s += '{}\n'.format(fielddisplay(self, 'accumulation', 'accumulated snow [m/yr ice eq]'))
        s += '{}\n'.format(fielddisplay(self, 'evaporation', 'mount of ice lost to evaporative processes [m/yr ice eq]'))
        s += '{}\n'.format(fielddisplay(self, 'melt', 'amount of ice melt in the ice column [m/yr ice eq]'))
        s += '{}\n'.format(fielddisplay(self, 'refreeze', 'amount of ice melt refrozen in the ice column [m/yr ice eq]'))
        s += '{}\n'.format(fielddisplay(self, 'steps_per_step', 'number of smb steps per time step'))
        s += '{}\n'.format(fielddisplay(self, 'averaging', 'averaging methods from short to long steps'))
        s += '\t\t{}\n'.format('0: Arithmetic (default)')
        s += '\t\t{}\n'.format('1: Geometric')
        s += '\t\t{}\n'.format('2: Harmonic')
        s += '{}\n'.format(fielddisplay(self, 'requested_outputs', 'additional outputs requested'))
        return s
    # }}}

    def extrude(self, md):  # {{{
        self.accumulation = project3d(md, 'vector', self.accumulation, 'type', 'node')
        self.evaporation = project3d(md, 'vector', self.evaporation, 'type', 'node')
        self.melt = project3d(md, 'vector', self.melt, 'type', 'node')
        self.refreeze = project3d(md, 'vector', self.refreeze, 'type', 'node')
        return self
    # }}}

    def defaultoutputs(self, md):  # {{{
        return ['SmbMassBalance']
    # }}}

    def initialize(self, md):  # {{{
        if np.all(np.isnan(self.accumulation)):
            self.accumulation = np.zeros((md.mesh.numberofvertices))
            print("      no smb.accumulation specified: values set as zero")

        if np.all(np.isnan(self.evaporation)):
            self.evaporation = np.zeros((md.mesh.numberofvertices))
            print("      no smb.evaporation specified: values set as zero")

        if np.all(np.isnan(self.refreeze)):
            self.refreeze = np.zeros((md.mesh.numberofvertices))
            print("      no smb.refreeze specified: values set as zero")

        if np.all(np.isnan(self.melt)):
            self.melt = np.zeros((md.mesh.numberofvertices))
            print("      no smb.melt specified: values set as zero")

        return self
    # }}}

    def checkconsistency(self, md, solution, analyses):  # {{{
        if 'MasstransportAnalysis' in analyses:
            md = checkfield(md, 'fieldname', 'smb.accumulation', 'timeseries', 1, 'NaN', 1, 'Inf', 1)
            md = checkfield(md, 'fieldname', 'smb.evaporation', 'timeseries', 1, 'NaN', 1, 'Inf', 1)
            md = checkfield(md, 'fieldname', 'smb.refreeze', 'timeseries', 1, 'NaN', 1, 'Inf', 1)
            md = checkfield(md, 'fieldname', 'smb.melt', 'timeseries', 1, 'NaN', 1, 'Inf', 1)

        if 'BalancethicknessAnalysis' in analyses:
            md = checkfield(md, 'fieldname', 'smb.accumulation', 'size', [md.mesh.numberofvertices], 'NaN', 1, 'Inf', 1)
            md = checkfield(md, 'fieldname', 'smb.evaporation', 'size', [md.mesh.numberofvertices], 'NaN', 1, 'Inf', 1)
            md = checkfield(md, 'fieldname', 'smb.refreeze', 'size', [md.mesh.numberofvertices], 'NaN', 1, 'Inf', 1)
            md = checkfield(md, 'fieldname', 'smb.melt', 'size', [md.mesh.numberofvertices], 'NaN', 1, 'Inf', 1)

        md = checkfield(md, 'fieldname', 'smb.steps_per_step', '>=', 1, 'numel', [1])
        md = checkfield(md, 'fieldname', 'smb.averaging', 'numel', [1], 'values', [0, 1, 2])
        md = checkfield(md, 'fieldname', 'smb.requested_outputs', 'stringrow', 1)
        return md
    # }}}
    def marshall(self, prefix, md, fid):  # {{{

        yts = md.constants.yts

        WriteData(fid, prefix, 'name', 'md.smb.model', 'data', 3, 'format', 'Integer')
        WriteData(fid, prefix, 'object', self, 'class', 'smb', 'fieldname', 'accumulation', 'format', 'DoubleMat', 'mattype', 1, 'scale', 1 / yts, 'timeserieslength', md.mesh.numberofvertices + 1, 'yts', yts)
        WriteData(fid, prefix, 'object', self, 'class', 'smb', 'fieldname', 'evaporation', 'format', 'DoubleMat', 'mattype', 1, 'scale', 1 / yts, 'timeserieslength', md.mesh.numberofvertices + 1, 'yts', yts)
        WriteData(fid, prefix, 'object', self, 'class', 'smb', 'fieldname', 'melt', 'format', 'DoubleMat', 'mattype', 1, 'scale', 1 / yts, 'timeserieslength', md.mesh.numberofvertices + 1, 'yts', yts)
        WriteData(fid, prefix, 'object', self, 'class', 'smb', 'fieldname', 'refreeze', 'format', 'DoubleMat', 'mattype', 1, 'scale', 1 / yts, 'timeserieslength', md.mesh.numberofvertices + 1, 'yts', yts)
        WriteData(fid, prefix, 'object', self, 'fieldname', 'steps_per_step', 'format', 'Integer')
        WriteData(fid, prefix, 'object', self, 'fieldname', 'averaging', 'format', 'Integer')

        #process requested outputs
        outputs = self.requested_outputs
        indices = [i for i, x in enumerate(outputs) if x == 'default']
        if len(indices) > 0:
            outputscopy = outputs[0:max(0, indices[0] - 1)] + self.defaultoutputs(md) + outputs[indices[0] + 1:]
            outputs = outputscopy
        WriteData(fid, prefix, 'data', outputs, 'name', 'md.smb.requested_outputs', 'format', 'StringArray')
    # }}}

    def setdefaultparameters(self):  # {{{
        self.requested_outputs = ['default']
        return self
    # }}}
