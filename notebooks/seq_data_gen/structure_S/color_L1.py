#
# -- basicCodeBlock.py
#
import numpy as np
from pymol import cmd, stored

def color_L1( arg0, arg1, arg2, arg3, arg4=1,MOVIE=0,bgcol='hydrogen' ):
    '''
DESCRIPTION

    Brief description: Colors the identified L1 features 
    '''
    # Running on pymol cmdline
    #run ./pymol_scripts/color_L1.py
    #color_L1 pdb/1ruz.pdb, 78 137 158 188 241 292 573, green, 2
    filename=arg0
    
    cmd.load(filename)
    cmd.hide('everything')
    #cmd.cartoon('rectangle')
    cmd.show('cartoon')


    cmd.set('reflect',0.5)

    
    
    
    Feature_set=[int(j) for j in np.array(arg1.split())]    
    col=arg2
    L=int(arg3)

    #reset color to gray
    if arg4=='1':
        print('coloring gray')
        cmd.do('color '+bgcol)

    print(arg4)
        
    F=np.array([np.arange(i-L,i+L+1) for i in Feature_set]).flatten()    
    for feature in F:
        print("resi "+str(feature))
        cmd.color(col, "resi "+ str(feature))

    cmd.viewport("2560,1920")

    if MOVIE=="0":
        MOVIE=False
        
    if MOVIE:
        cmd.show('surface')
        cmd.mset('1 x 10')
        cmd.util.mroll(1,10,1)

        cmd.mplay
        cmd.viewport("2560,1920")
        cmd.set("ray_trace_frames",1)
        cmd.set("cache_frames",0)
        cmd.mclear
        cmd.mpng('zXXXmov')

cmd.extend( "color_L1", color_L1 );
