python ../../ppmd/sample_inputs.py 'two_body' 2

mpirun -np 1 python two_body_test.py singlecore_two_body.ppmd
mpirun -np 2 python two_body_test.py multicore_two_body.ppmd

python make_plots.py

rm *.hdf5
