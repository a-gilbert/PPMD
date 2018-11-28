python ../../ppmd/sample_inputs.py 'two_body'

mpirun -np 1 python two_body_test.py singlecore_two_body.ppmd
mpirun -np 3 python two_body_test.py multicore_two_body.ppmd

python plot_energies.py

rm *.hdf5
