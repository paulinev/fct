#l = "Thread-9  Flow # 1  size:  2507  bytes syn_fct:  109  get_fct:  46"

import numpy

def get_fcts(sort, flowreq):
    fcts = []
    flow_fcts = {}
    syn_fcts = {}
    get_fcts = {}
    with open(flowreq, 'r') as flowreq:
        for line in flowreq:
            if "Flow #" in line:
                line = [i for i in line.split(' ') if i is not '']
                syn_fct = int(line[-3])
                get_fct = int(line[-1])
                flow_size = int(line[5])
                # Get all FCTS, syn and get, and store them in the same container
                if sort == 'all':
                    fcts.append(syn_fct)
                    fcts.append(get_fct)
                # Get FCTs by flow size, ignoring type.
                elif sort == 'flow':
                    if flow_size in flow_fcts:
                        flow_fcts[flow_size].extend([syn_fct, get_fct])
                    else:
                        flow_fcts[flow_size] = [syn_fct, get_fct]
                # Get FCTs by flow size and by type.
                else:
                    if flow_size in syn_fcts:
                        syn_fcts[flow_size].append(syn_fct)
                        get_fcts[flow_size].append(get_fct)
                    else:
                        syn_fcts[flow_size] = [syn_fct]
                        get_fcts[flow_size] = [get_fct]
    if sort == 'all':
        return fcts
    elif sort == 'flow':
        return flow_fcts
    else:

        for k in syn_fcts:
            syn_fcts[k] = float(sum(syn_fcts[k]))/len(syn_fcts[k])
            get_fcts[k] = float(sum(get_fcts[k]))/len(get_fcts[k])
        return syn_fcts, get_fcts

def mean(l):
    return float(sum(l))/len(l)

def list_mean(l1, l2):
    out = []
    for i in range(len(l1)):
        out.append(mean([l1[i], l2[i]]))
    return out

def save_data(flowreq, outfile, protocol, link, seed, flows):
    syn_fcts, get_fct = get_fcts('type', flowreq)
    basic_data = ['', protocol, link, 'Seed '+str(seed)+' - '+str(flows)+' flows', '']
    i = 0
    with open(outfile, 'w') as outfile:
        outfile.write(',Flow Size,Syn,Get,Mean\n')
        for k in sorted(syn_fcts):
            mean = str(float(syn_fcts[k]+get_fct[k])/2.0)
            if i < len(basic_data):
                data = basic_data[i]
            else:
                data = ''
            outfile.write(data+','+str(k)+','+str(syn_fcts[k])+','+str(get_fct[k])+','+mean)
            outfile.write('\n')
            i += 1
##        get = [get_fct[v] for v in sorted(get_fct)]
##        syn = [syn_fcts[v] for v in sorted(syn_fcts)]
##        means = list_mean(get, syn)
##        print get_fct
##        ## Skip a line
##        outfile.write(',,,,,\n')
##        ## Write the means
##        #outfile.write('Mean:,'+str(mean(syn_fcts.keys()))+','+str(mean(syn_fcts.values()))+','+
##        #              str(mean(get_fct.values()))+','+str(mean(means)))
##        #outfile.write('\n')
##        ## Write the medians
##        outfile.write('Median:,'+str(numpy.median(syn_fcts.keys()))+','+str(numpy.median(syn_fcts.values()))+','+
##                      str(numpy.median(get_fct.values()))+','+str(numpy.median(means)))
##        outfile.write('\n')
##        ## Write the percentiles
##        outfile.write('95th percentile:,'+str(numpy.percentile(syn_fcts.keys(), 95))+','+str(numpy.percentile(syn_fcts.values(), 95))+','+
##                      str(numpy.percentile(get_fct.values(), 95))+','+str(numpy.percentile(means, 95)))
##        outfile.write('\n')
##        outfile.write('99th percentile:,'+str(numpy.percentile(syn_fcts.keys(), 99))+','+str(numpy.percentile(syn_fcts.values(), 99))+','+
##                      str(numpy.percentile(get_fct.values(), 99))+','+str(numpy.percentile(means), 99))
##        outfile.write('\n')
            

def percentile(dataset, k):
    if type(dataset) is dict:
        data = [x for x in dataset.values() if x is not None]
    else:
        data = [x for x in dataset if x is not None]
    dataset = sorted(data)
    k = float(k)/100.0
    if k == 1.0:
        return max(dataset)
    elif k == 0:
        return min(dataset)
    else:
        i = (len(dataset)-1)*k
        f = math.floor(i)
        c = math.ceil(i)
        if f == c:
            return dataset[int(f)]
        v1 = dataset[int(f)]*(c-i)
        v2 = dataset[int(c)]*(i-f)
        return v1+v2

# NEEDS A LIST
def tail(fcts):
    return percentile(fcts, 95), percentile(fcts, 99)
