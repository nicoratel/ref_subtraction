
import numpy as np
import os

def openfile(source):
    if hasattr(source, "seek"):
        source.seek(0)
    tth, I = np.loadtxt(source, unpack=True)
    return tth, I

def subtract_by_percentile(samplefilename, Cfilename, percentile=5,plot=False):
    tth_s, I_s = openfile(samplefilename)
    tth_c, I_c = openfile(Cfilename)
    
    I_c_interp = np.interp(tth_s, tth_c, I_c)
    
    mask = I_c_interp > 0
    ratios = I_s[mask] / I_c_interp[mask]
    alpha = np.percentile(ratios, percentile)
    
    I_result = I_s - alpha * I_c_interp
    
    n_neg = np.sum(I_result < 0)
    print(f"points négatifs : {n_neg} ({100*n_neg/len(I_result):.1f}%)")
       
    return tth_s, I_result


def subtract_C(samplefilename,
               Cfilename,
               percentile = 5,
               plot=False,
               save_output=True,
               output_path=None):
    tth, I= subtract_by_percentile(samplefilename,Cfilename,percentile,plot=plot)

    if save_output:
        if output_path is not None:
            output = output_path
        else:
            sample_name = getattr(samplefilename, "name", str(samplefilename))
            output = os.path.splitext(sample_name)[0] + '_subtracted.ASC'
        print(f"Saving subtracted data to {output}")
        np.savetxt(output, np.column_stack((tth, I)))
    return tth, I