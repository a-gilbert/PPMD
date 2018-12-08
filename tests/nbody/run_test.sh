python ../../ppmd/sample_inputs.py 'globally_uniform' 100

mpirun -np 1 python nbody_test.py singlecore_n_body_ts1.ppmd
mpirun -np 1 python nbody_test.py singlecore_n_body_ts2.ppmd
mpirun -np 3 python nbody_test.py multicore_n_body_ts1.ppmd
mpirun -np 3 python nbody_test.py multicore_n_body_ts2.ppmd

python plot_energies.py

rm *.hdf5
