import os,sys,shutil,datetime,time
from ROOT import *

execfile("/uscms_data/d3/jmanagan/EOSSafeUtils.py")

start_time = time.time()

#IO directories must be full paths

relbase = '/uscms_data/d3/bburgsta/CMSSW_10_2_16/'
inputDir='/eos/uscms/store/user/bburgsta/FWLJMET102X_1lep2016Dnn_042720_step1hadds/'
outputDir='/eos/uscms/store/user/bburgsta/FWLJMET102X_1lep2016Dnn_May2020_step2hadds/' 
condorDir='/uscms_data/d3/bburgsta/FWLJMET102X_1lep2016Dnn_May2020_step2hadds'

runDir=os.getcwd()

gROOT.ProcessLine('.x compileStep2.C')

cTime=datetime.datetime.now()
date='%i_%i_%i_%i_%i_%i'%(cTime.year,cTime.month,cTime.day,cTime.hour,cTime.minute,cTime.second)

inDir=inputDir[10:]
outDir=outputDir[10:]

print 'Starting submission'
count=0

rootfiles = EOSlist_root_files(inputDir)
os.system('eos root://cmseos.fnal.gov/ mkdir -p '+outDir)
os.system('mkdir -p '+condorDir)

for file in rootfiles:

    # can turn some files of/off, but right now don't need to.
    #if 'BprimeBprime_M-1800' not in file and 'WJetsToLNu_HT' not in file: continue 
    rawname = file[:-5]
    print file
    print "rawname: ",rawname
    count+=1
    dict={'RUNDIR':runDir, 'CONDORDIR':condorDir, 'INPUTDIR':inDir, 'FILENAME':rawname, 'CMSSWBASE':relbase, 'OUTPUTDIR':outDir}
    jdfName=condorDir+'/%(FILENAME)s.job'%dict
    print "jdfname: ",jdfName
    jdf=open(jdfName,'w')
    jdf.write(
        """use_x509userproxy = true
universe = vanilla
Executable = %(RUNDIR)s/makeStep2.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(RUNDIR)s/makeStep2.C, %(RUNDIR)s/step2.cc, %(RUNDIR)s/step2.h, %(RUNDIR)s/step2_cc.d, %(RUNDIR)s/step2_cc.so
Output = %(FILENAME)s.out
Error = %(FILENAME)s.err
Log = %(FILENAME)s.log
Notification = Never
Arguments = %(FILENAME)s.root %(FILENAME)s.root %(INPUTDIR)s %(OUTPUTDIR)s

Queue 1"""%dict)
    jdf.close()
    os.chdir('%s/'%(condorDir))
    os.system('condor_submit %(FILENAME)s.job'%dict)
    os.system('sleep 0.5')                                
    os.chdir('%s'%(runDir))
    print count, "jobs submitted!!!"


print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))




