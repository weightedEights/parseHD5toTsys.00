__author__ = 'sri-Wonder'


#def calcTsys():

from tables import *


h5ds = open_file("./d0111900.dt1.h5", "r")

sysConst = h5ds.root.Rx.SysConst.read()

h5ds.close()


print sysConst


"""

def tSys(self,caltemp,cal,no   i):
        mcp = np.mean(cal)
        mnp = np.mean(noi)
        tsys = (mnp*caltemp)/(mcp-mnp)
        return tsys

"""

"""

class fileEntry:
    def __init__(self,filepath):
        self.filepath = filepath
        self.h5 = h5 = openFile(filepath,'r')
        self.nRecs = len(h5.root.Time.RadacTime)
        self.start = 0
        self.stop = 0

    def __str__(self):
        res = ''
        res += 'filepath: %s\n' % (self.filepath)
        res += 'nrecs:    %d\n' % (self.nRecs)
        res += 'start:    %d\n' % (self.start)
        res += 'stop:     %d\n' % (self.stop)
        return res

    def inFile(self,n):
        return ((n>=self.start) and (n<=self.stop))

    def recIndex(self,n):
        return n-self.start

"""

"""

class S(baseProcessor):
    name = 'S'
    rootpath = '/S'
    subint = 10

    def processData(self,data,h5,rec=0,bcindex=0):
        data['S'] = {}

        pos = self.position(h5,rec,bcindex)

        path = '/S/Data/Power/Data'
        if h5.__contains__(path):
            pwr = h5.getNode(path).read(rec)[0]
            data['S']['datapower'] = pwr[bcindex,:].tolist()
            rng = h5.getNode('/S/Data/Power/Range').read()
            data['S']['altdatapower'] = self.altitude(pos,rng[0]).tolist()
            vertices = self.xyVertices(pos,rng)
            data['S']['verticesdatapower'] = vertices.tolist()

        path = '/S/Cal/Power/Data'
        if h5.__contains__(path):
            pwr = h5.getNode(path).read(rec)[0]
            data['S']['calpower'] = pwr[bcindex,:].tolist()
            rng = h5.getNode('/S/Cal/Power/Range').read()
            data['S']['altcalpower'] = self.altitude(pos,rng[0]).tolist()

        path = '/S/Noise/Power/Data'
        if h5.__contains__(path):
            pwr = h5.getNode(path).read(rec)[0]
            data['S']['noisepower'] = pwr[bcindex,:].tolist()
            rng = h5.getNode('/S/Noise/Power/Range').read()
            data['S']['altnoisepower'] = self.altitude(pos,rng[0]).tolist()

        if data['S'].has_key('noisepower') and data['S'].has_key('calpower'):
            caltemp = float(h5.root.Rx.CalTemp.read())
            bandwidth = float(h5.root.Rx.Bandwidth.read())
            sysconst = self.getSysConst(h5,bcindex)
            #sysconst = float(h5.root.Rx.SysConst.read())
            pulsewidth = float(h5.root.S.Data.Pulsewidth.read())

            try:
                txpwr = np.array(h5.root.Tx.Power[0])
            except:
                txpwr = np.array([3e6,3e6])
            txpwr = np.mean(txpwr)

            rng = h5.getNode('/S/Data/Power/Range').read()[0]
            dat = data['S']['datapower']
            cal = data['S']['calpower']
            noi = data['S']['noisepower']

            tsys = self.tSys(caltemp,cal,noi)
            den = self.density(caltemp,sysconst,bandwidth,pulsewidth,txpwr,rng,dat,cal,noi)
            indx = np.where(den<=0)
            den[indx] = 1.0

            data['S']['density'] = den.tolist()
            data['S']['tsys'] = tsys


        # spectra and velocities
        sampletime = float(h5.root.Rx.SampleTime.read())
        try:
            rxfreq = float(np.squeeze(h5.root.Rx.Frequency[rec,0]))
        except:
            rxfreq = 1290e6

        if h5.__contains__('/S/Noise/Acf/Data'):
            nacf = np.squeeze(h5.getNode('/S/Noise/Acf/Data').read(rec)[0,bcindex])
            nacf = np.mean(nacf,axis=1)
            shape = list(nacf.shape)
            shape.insert(1,1)
            nacf.shape = shape
            nspec,nfreq = self.acfToSpectra(nacf,sampletime)
            data['S']['noisespectra'] = nspec.real.tolist()


        if h5.__contains__('/S/Data/Acf/Data'):
            acf = np.squeeze(h5.getNode('/S/Data/Acf/Data').read(rec)[0,bcindex])
            rng = np.squeeze(h5.getNode('/S/Data/Acf/Range').read())
            si = self.subint
            sacf = self.rangeSubInt(acf,si,si,1)
            srng = self.rangeSubInt(rng,si,si,0)
            srng.shape = (1,)+srng.shape
            vertices = self.xyVertices(pos,srng)
            data['S']['verticesdataacf'] = vertices.tolist()
            data['S']['altdataacf'] = self.altitude(pos,srng[0]).tolist()
            spec,freq = self.acfToSpectra(sacf,sampletime)
            data['S']['spectra'] = spec.real.tolist()
            data['S']['specfreq'] = freq.tolist()

            if locals().has_key('nspec'):
                los = self.losVelocity(sampletime,rxfreq,spec,nspec,2.0)
                data['S']['velocities'] = los.tolist()
                # print data['S']['velocities']

"""