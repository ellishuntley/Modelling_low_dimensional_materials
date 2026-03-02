for psi_cut in 10 20 30 40 50 60; do 
    # calculate rho_cut
    rho_cut=$(($psi_cut * 10))
    # replace psi_cut and rho_cut in template
    sed "s/psi_cut/${psi_cut}/g; s/rho_cut/${rho_cut}/g" scf.in.template > scf.in
    # execute with pw.x 
    pw.x < scf.in > scf.out
    # read total energy 
    energy=$(grep "!" scf.out | tail -1 | awk '{print $5}')
    # write psi_cut and energy to energy_pw.dat
    echo "$psi_cut $energy" >> energy_pw.dat
done