import sys

use_cprofiler = False
max_nranks = int(sys.argv[1])
#number of trials to run for each rank. 
ntrials = int(sys.argv[2])
npart_per_rank = int(sys.argv[3])
if sys.argv[4] == "True":
    use_cprofiler = True
    

standard_template = open('nbody_template.ppmd', 'r')
standard_template = standard_template.readlines()

#generate input scripts
ins = []

for i in range(1, max_nranks):
    for k in range(ntrials):
        s = "%dranks_t%d_nbody.ppmd" % (i, k)
        ins.append((i, k, s))
        f = open(s, 'w')
        for j in range(len(standard_template)):
            line = standard_template[j]
            if j == 9:
                line = line.split()
                fn = " uniform_random_2types_%spart.hdf5\n" % str(npart_per_rank*i)
                line = line[0] + ' ' + line[1] + ' ' + line[2] + fn
            if j == 13:
                line = line.split()
                line[2] = '%dr_t%d_DD' % (i,k)
                line = line[0] + ' ' + line[1] + ' ' + line[2] + '\n'
            f.write(line)
        f.close()

#generate run script
rscript_template = open('run_template.sh', 'r')
rscript_template = rscript_template.readlines()

rscript = open('run_weak_scaling.sh', 'w')

l = len(rscript_template[0])
command = rscript_template[0][0:l-1] + ' '
for i in range(1, max_nranks):
    rscript.write(command + str(npart_per_rank*i) + '\n')
for t in ins:
    if use_cprofiler:
        s = 'mpirun -np %d python -m cProfile -o %dranks_t%d.profile nbody_test.py %s\n' % (t[0], t[0], t[1], t[2])
    else:
        s = 'mpirun -np %d python nbody_test.py %s\n' % (t[0], t[2])
    rscript.write(s)

for i in range(1, len(rscript_template)):
    rscript.write(rscript_template[i])

rscript.close()
quit()
