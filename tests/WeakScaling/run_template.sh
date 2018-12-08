python ../../ppmd/sample_inputs.py 'globally_uniform'
rm *nbody.ppmd
rm *.hdf5
python plot_scaling.py
rm *.profile
