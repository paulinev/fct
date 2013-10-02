
def create_static_link(max_time, step, filename):
    with open(filename, 'w') as f:
        for i in range(0, max_time+1, step):
            f.write(str(i)+'\n')

create_static_link(140000, 10, "static_link_10.ms")
