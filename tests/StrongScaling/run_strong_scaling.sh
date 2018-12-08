python ../../ppmd/sample_inputs.py 'globally_uniform' 1000
mpirun -np 1 python -m cProfile -o 1ranks_t0.profile nbody_test.py 1ranks_t0_nbody.ppmd
mpirun -np 1 python -m cProfile -o 1ranks_t1.profile nbody_test.py 1ranks_t1_nbody.ppmd
mpirun -np 1 python -m cProfile -o 1ranks_t2.profile nbody_test.py 1ranks_t2_nbody.ppmd
mpirun -np 1 python -m cProfile -o 1ranks_t3.profile nbody_test.py 1ranks_t3_nbody.ppmd
mpirun -np 1 python -m cProfile -o 1ranks_t4.profile nbody_test.py 1ranks_t4_nbody.ppmd
mpirun -np 2 python -m cProfile -o 2ranks_t0.profile nbody_test.py 2ranks_t0_nbody.ppmd
mpirun -np 2 python -m cProfile -o 2ranks_t1.profile nbody_test.py 2ranks_t1_nbody.ppmd
mpirun -np 2 python -m cProfile -o 2ranks_t2.profile nbody_test.py 2ranks_t2_nbody.ppmd
mpirun -np 2 python -m cProfile -o 2ranks_t3.profile nbody_test.py 2ranks_t3_nbody.ppmd
mpirun -np 2 python -m cProfile -o 2ranks_t4.profile nbody_test.py 2ranks_t4_nbody.ppmd
mpirun -np 3 python -m cProfile -o 3ranks_t0.profile nbody_test.py 3ranks_t0_nbody.ppmd
mpirun -np 3 python -m cProfile -o 3ranks_t1.profile nbody_test.py 3ranks_t1_nbody.ppmd
mpirun -np 3 python -m cProfile -o 3ranks_t2.profile nbody_test.py 3ranks_t2_nbody.ppmd
mpirun -np 3 python -m cProfile -o 3ranks_t3.profile nbody_test.py 3ranks_t3_nbody.ppmd
mpirun -np 3 python -m cProfile -o 3ranks_t4.profile nbody_test.py 3ranks_t4_nbody.ppmd
mpirun -np 4 python -m cProfile -o 4ranks_t0.profile nbody_test.py 4ranks_t0_nbody.ppmd
mpirun -np 4 python -m cProfile -o 4ranks_t1.profile nbody_test.py 4ranks_t1_nbody.ppmd
mpirun -np 4 python -m cProfile -o 4ranks_t2.profile nbody_test.py 4ranks_t2_nbody.ppmd
mpirun -np 4 python -m cProfile -o 4ranks_t3.profile nbody_test.py 4ranks_t3_nbody.ppmd
mpirun -np 4 python -m cProfile -o 4ranks_t4.profile nbody_test.py 4ranks_t4_nbody.ppmd
mpirun -np 5 python -m cProfile -o 5ranks_t0.profile nbody_test.py 5ranks_t0_nbody.ppmd
mpirun -np 5 python -m cProfile -o 5ranks_t1.profile nbody_test.py 5ranks_t1_nbody.ppmd
mpirun -np 5 python -m cProfile -o 5ranks_t2.profile nbody_test.py 5ranks_t2_nbody.ppmd
mpirun -np 5 python -m cProfile -o 5ranks_t3.profile nbody_test.py 5ranks_t3_nbody.ppmd
mpirun -np 5 python -m cProfile -o 5ranks_t4.profile nbody_test.py 5ranks_t4_nbody.ppmd
mpirun -np 6 python -m cProfile -o 6ranks_t0.profile nbody_test.py 6ranks_t0_nbody.ppmd
mpirun -np 6 python -m cProfile -o 6ranks_t1.profile nbody_test.py 6ranks_t1_nbody.ppmd
mpirun -np 6 python -m cProfile -o 6ranks_t2.profile nbody_test.py 6ranks_t2_nbody.ppmd
mpirun -np 6 python -m cProfile -o 6ranks_t3.profile nbody_test.py 6ranks_t3_nbody.ppmd
mpirun -np 6 python -m cProfile -o 6ranks_t4.profile nbody_test.py 6ranks_t4_nbody.ppmd
mpirun -np 7 python -m cProfile -o 7ranks_t0.profile nbody_test.py 7ranks_t0_nbody.ppmd
mpirun -np 7 python -m cProfile -o 7ranks_t1.profile nbody_test.py 7ranks_t1_nbody.ppmd
mpirun -np 7 python -m cProfile -o 7ranks_t2.profile nbody_test.py 7ranks_t2_nbody.ppmd
mpirun -np 7 python -m cProfile -o 7ranks_t3.profile nbody_test.py 7ranks_t3_nbody.ppmd
mpirun -np 7 python -m cProfile -o 7ranks_t4.profile nbody_test.py 7ranks_t4_nbody.ppmd
mpirun -np 8 python -m cProfile -o 8ranks_t0.profile nbody_test.py 8ranks_t0_nbody.ppmd
mpirun -np 8 python -m cProfile -o 8ranks_t1.profile nbody_test.py 8ranks_t1_nbody.ppmd
mpirun -np 8 python -m cProfile -o 8ranks_t2.profile nbody_test.py 8ranks_t2_nbody.ppmd
mpirun -np 8 python -m cProfile -o 8ranks_t3.profile nbody_test.py 8ranks_t3_nbody.ppmd
mpirun -np 8 python -m cProfile -o 8ranks_t4.profile nbody_test.py 8ranks_t4_nbody.ppmd
mpirun -np 9 python -m cProfile -o 9ranks_t0.profile nbody_test.py 9ranks_t0_nbody.ppmd
mpirun -np 9 python -m cProfile -o 9ranks_t1.profile nbody_test.py 9ranks_t1_nbody.ppmd
mpirun -np 9 python -m cProfile -o 9ranks_t2.profile nbody_test.py 9ranks_t2_nbody.ppmd
mpirun -np 9 python -m cProfile -o 9ranks_t3.profile nbody_test.py 9ranks_t3_nbody.ppmd
mpirun -np 9 python -m cProfile -o 9ranks_t4.profile nbody_test.py 9ranks_t4_nbody.ppmd
mpirun -np 10 python -m cProfile -o 10ranks_t0.profile nbody_test.py 10ranks_t0_nbody.ppmd
mpirun -np 10 python -m cProfile -o 10ranks_t1.profile nbody_test.py 10ranks_t1_nbody.ppmd
mpirun -np 10 python -m cProfile -o 10ranks_t2.profile nbody_test.py 10ranks_t2_nbody.ppmd
mpirun -np 10 python -m cProfile -o 10ranks_t3.profile nbody_test.py 10ranks_t3_nbody.ppmd
mpirun -np 10 python -m cProfile -o 10ranks_t4.profile nbody_test.py 10ranks_t4_nbody.ppmd
python plot_scaling.py
rm *nbody.ppmd
rm *.hdf5
rm *.profile
