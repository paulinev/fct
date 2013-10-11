#l = "Thread-9  Flow # 1  size:  2507  bytes syn_fct:  109  get_fct:  46"

import sys

#sort = sys.argv[0]
#flowreq = sys.argv[1]

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
        for flowsize in syn_fcts:
            syn_fcts[flowsize] = float(sum(syn_fcts[flowsize]))/len(syn_fcts[flowsize])
            get_fcts[flowsize] = float(sum(get_fcts[flowsize]))/len(get_fcts[flowsize])
        return syn_fcts, get_fcts

# Sort types: all returns combined mean of all syn_ and get_fcts, ignoring type and flow
#         flow returns combined mean of all fcts sorted by flow
#         type returns mean of all syn_ and get_ fcts individually, ignoring flow
#         flow+type returns mean of all syn_ and get_ fcts individually, sorted by flow
def mean_fct(sort, *args):
    if sort == 'all':
        mean = sum(enumerate(args))/len(enumerate(args))
        return mean
    elif sort == 'flow':
        means_by_flow = {}
        for flow in args:
            mean = sum(args[flow])/len(args[flow])
            means_by_flow[flow] = mean
        return means_by_flow
    elif sort == 'type':
        syn_fcts, get_fcts = args
        all_syn_fcts = [l for l in sum(syn_fcts.values(), [])]
        all_get_fcts = [l for l in sum(get_fcts.values(), [])]
    
        mean_syn = sum(all_syn_fcts)/len(all_syn_fcts)
        mean_get = sum(all_get_fcts)/len(all_get_fcts)

        return mean_syn, mean_get
    else:
        mean_syn = {}
        mean_get = {}
        for flow in syn_fcts:
            mean_syn[flow] = sum(syn_fcts[flow])/len(syn_fcts[flow])
        for flow in get_fcts:
            mean_get[flow] = sum(get_fcts[flow])/len(get_fcts[flow])
        return mean_syn, mean_get

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
    print "95th percentile: ", percentile(fcts, 95)
    print "99th percentile: ", percentile(fcts, 99)
    return
