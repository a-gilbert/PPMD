"""Module for a number of different force calculations"""
import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

mod = SourceModule("""
 #include <stdio.h>

 __device__ void calc_force_w_en(float4* force, float* r1, float* r2, float k) {
     (*force).x = *r1 - *r2;
     r1++;
     r2++;
     (*force).y = *r1 - *r2;
     r1++;
     r2++;
     (*force).z = *r1 - *r2;
     (*force).w = 1.0/sqrtf((*force).x*(*force).x + (*force).y*(*force).y + (*force).z*(*force).z);
     (*force).x = (*force).x * (*force).w * (*force).w;
     (*force).y = (*force).y * (*force).w * (*force).w;
     (*force).z = (*force).z * (*force).w * (*force).w;
     (*force).w = (*force).w*k;
     (*force).x = (*force).x*(*force).w;
     (*force).y = (*force).y*(*force).w;
     (*force).z = (*force).z*(*force).w;
 }

 __global__ void calc_loc_force3d_w_energy(float* qs, float* k, float* rs, float* fs, 
 int* ts, float* en, int npart) {
     int i = blockIdx.x * blockDim.x + threadIdx.x;
     int my_part;
     if(npart % 2 == 0) {
         my_part = npart - 1 - i;
     } else {
         my_part = npart - i;
     }

     if(my_part >= 0) {
         float my_r[3] = {rs[i], rs[i+1], rs[i+2]};
         float my_q = qs[ts[my_part]];
         float my_en = 0;
         float my_force[3] = {0, 0, 0};
         float4 force;
         float c;
         for(int a = my_part + 1; a < npart; a++) {
             c = my_q*qs[ts[a]]*k[0];
             calc_force_w_en(&force, my_r, rs + 3*a, c);
             printf("energy is %.4g for interaction %d, %d\\n", force.w, my_part, a);
             my_en += force.w;
             my_force[0] += force.x;
             fs[a] -= force.x;
             my_force[1] += force.y;
             fs[a+1] -= force.y;
             my_force[2] += force.z;
             fs[a+2] -= force.z;
         }
         for(int b=0; b<3; b++) {
             fs[my_part + b] += my_force[b];
         }

        my_part = i;
        for(int a = 0; a<3; a++) {
            my_force[a] = 0;
        }
        if(my_part < npart) {
            my_q = qs[ts[i]];
            for(int a = my_part+1; a<npart; a++) {
                c = my_q*qs[ts[a]]*k[0];
                calc_force_w_en(&force, my_r, rs + 3*a, c);
                my_en += force.w;
                my_force[0] += force.x;
                fs[a] -= force.x;
                my_force[1] += force.y;
                fs[a+1] -= force.y;
                my_force[2] += force.z;
                fs[a+2] -= force.z;
            }
            for(int b=0; b<3; b++) {
                fs[my_part + b] += my_force[b];
            }
        }
     en[i] = my_en;
    }
 }

 __global__ void calc_nloc_force3d_w_energy(float* qs, float* k, float* rs1, float* fs1, float* rs2,
 float* fs2, int* ts1, int* ts2, float* en, int nlpart, int npart)
 {
     int i = blockIdx.x * blockDim.x + threadIdx.x;

     if(i < npart) {
         float my_r[3] = {rs1[i], rs1[i+1], rs1[i+2]};
         float my_q = qs[ts1[i]];
         float my_en = 0;
         float my_force[3] = {0, 0, 0};
         float4 force;
         float c;
         for(int a = 0; a < nlpart; a++) {
             c = my_q*qs[ts2[a]]*k[0];
             calc_force_w_en(&force, my_r, rs2 + 3*a, c);
             my_en += force.w;
             my_force[0] += force.x;
             fs2[a] -= force.x;
             my_force[1] += force.y;
             fs2[a+1] -= force.y;
             my_force[2] += force.z;
             fs2[a+2] -= force.z;
         }
        for(int b=0; b<3; b++) {
            fs1[i + b] += my_force[b];
        }
        en[i] = my_en;
     }
 }

 __device__ void calc_force_wo_en(float3* force, float* r1, float* r2, float k){
     (*force).x = *r1 - *r2;
     r1++;
     r2++;
     (*force).y = *r1 - *r2;
     r1++;
     r2++;
     (*force).z = *r1 - *r2;
     float rinv3 = 1.0/sqrtf((*force).x*(*force).x + (*force).y*(*force).y + (*force).z*(*force).z);
     rinv3 = rinv3*rinv3*rinv3;
     (*force).x = k*(*force).x*rinv3;
     (*force).y = k*(*force).y*rinv3;
     (*force).z = k*(*force).z*rinv3;
 }

 __global__ void calc_loc_force3d_wo_energy(float* qs, float* k, float* rs, float* fs, 
 int* ts, int npart)
 {
     int i = blockIdx.x * blockDim.x + threadIdx.x;
     int my_part;
     if(npart % 2 == 0) {
         my_part = npart - 1 - i;
     } else {
         my_part = npart - i;
     }

     if(my_part >= 0) {
         float my_r[3] = {rs[i], rs[i+1], rs[i+2]};
         float my_q = qs[ts[my_part]];
         float my_force[3] = {0, 0, 0};
         float3 force;
         float c;
     //should make this a device function 
        for(int a = my_part + 1; a < npart; a++) {
            c = my_q*qs[ts[a]]*k[0];
            calc_force_wo_en(&force, my_r, rs + 3*a, c);
            my_force[0] += force.x;
            fs[a] -= force.x;
            my_force[1] += force.y;
            fs[a+1] -= force.y;
            my_force[2] += force.z;
            fs[a+2] -= force.z;
        }
        for(int b=0; b<3; b++) {
            fs[my_part + b] += my_force[b];
        }
    
         my_part = i;
         for(int a = 0; a<3; a++) {
             my_force[a] = 0;
         }
        if(my_part < npart) {
            my_q = qs[ts[i]];
            for(int a = my_part+1; a<npart; a++) {
                c = my_q*qs[ts[a]]*k[0];
                calc_force_wo_en(&force, my_r, rs + 3*a, c);
                my_force[0] += force.x;
                fs[a] -= force.x;
                my_force[1] += force.y;
                fs[a+1] -= force.y;
                my_force[2] += force.z;
                fs[a+2] -= force.z;
            }
        
            for(int b=0; b<3; b++) {
                fs[my_part + b] += my_force[b];
            }
        }
    }
 }


  __global__ void calc_nloc_force3d_wo_energy(float* qs, float* k, float* rs1, float* fs1, 
  float* rs2, float* fs2, int* ts1, int* ts2, int nlpart, int npart)
 {
     int i = blockIdx.x * blockDim.x + threadIdx.x;

     if(i < npart) {
         float my_r[3] = {rs1[i], rs1[i+1], rs1[i+2]}; ;
         float my_q = qs[ts1[i]];
         float my_force[3] = {0, 0, 0};
         float3 force;
         float c;
        for(int a = 0; a < nlpart; a++) {
            c = my_q*qs[ts2[a]]*k[0];
            calc_force_wo_en(&force, my_r, rs2 + 3*a, c);
            my_force[0] += force.x;
            fs2[a] -= force.x;
            my_force[1] += force.y;
            fs2[a+1] -= force.y;
            my_force[2] += force.z;
            fs2[a+2] -= force.z;
            my_force[1] += force.y;
        }
        for(int b=0; b<3; b++) {
            fs1[i + b] += my_force[b];
        }
     }
 }
""")


class CPUFrBExactForceCalculator(object):

    @classmethod
    def run(cls, gcomm, lpart, units, calc_energy):
        lpart.fs[:, :] = 0.0
        if calc_energy:
            lpart.energy = 0.0
        CPUFrBExactForceCalculator.get_loc_force_ls(lpart, units, calc_energy)
        if gcomm.Get_size() > 1:
            r = gcomm.Get_rank()
            s = gcomm.Get_size()
            lim = 0
            if (s-1)%2 == 0:
                lim = int((s-1)/2)
            else:
                lim = int(s/2)
            for j in range(1, lim+1):
                gcomm.barrier()
                ur = (r + j)%s
                lr = (r-j)%s
                if ur==lr:
                    CPUFrBExactForceCalculator.get_nloc_force_sr1(gcomm, ur, lr, 
                    lpart, units, calc_energy)
                else:
                    CPUFrBExactForceCalculator.get_nloc_force_sr2(gcomm, ur, lr, lpart, 
                    units, calc_energy)

    #get local force from ls
    @classmethod
    def get_loc_force_ls(cls, lpart, units, calc_energy):
        c = units['k']
        for j in range(len(lpart.ids)):
            for i in range(0, j):
                dr = lpart.rs[i] - lpart.rs[j]
                rinv = 1.0/np.sqrt(np.sum(dr**2))
                en = c*lpart.qs[lpart.types[i]]*lpart.qs[lpart.types[j]]*rinv
                if calc_energy:
                    lpart.energy += en
                en = en*rinv*rinv*dr
                lpart.fs[i] += en
                lpart.fs[j] -= en

    #get local and non-local force from non-local source.
    @classmethod
    def get_lnl_force_nls(cls, lpart, nltypes, nlrs, units, calc_energy):
        c = units['k']
        for i in range(len(nltypes)):
            netf = np.zeros(nlrs.shape[1])
            for j in range(len(lpart.ids)):
                dr = nlrs[i] - lpart.rs[j]
                rinv = 1.0/np.sqrt(np.sum(dr**2))
                en = c*lpart.qs[nltypes[i]]*lpart.qs[lpart.types[j]]*rinv
                if calc_energy:
                    lpart.energy += en
                en = en*rinv*rinv*dr
                netf += en
                lpart.fs[j, :] -= en
            nlrs[i, :] = netf


    #get only local force from non-local source.
    @classmethod
    def get_l_force_nls(cls, lpart, nltypes, nlrs, units, calc_energy):
        c = units['k']
        for i in range(len(nltypes)):
            for j in range(len(lpart.ids)):
                dr = nlrs[i] - lpart.rs[j]
                rinv = 1.0/np.sqrt(np.sum(dr**2))
                en = c*lpart.qs[nltypes[i]]*lpart.qs[lpart.types[j]]*rinv
                if calc_energy:
                    lpart.energy += en
                en = en*rinv*rinv*dr
                lpart.fs[j, :] -= en


    @classmethod
    def get_nloc_force_sr2(cls, gcomm, urank, lrank, lpart, units, calc_energy):
        #number of particles im about to get
        npart = CPUFrBExactForceCalculator.get_npart(gcomm, urank, lrank, len(lpart.ids))
        npart = npart[0]
        nltypes_buf = np.zeros(npart, dtype=int)
        nlrs_buf = np.zeros((npart, lpart.rs.shape[1]), dtype=np.float64)
        #send types to urank, recv types from lrank
        gcomm.Sendrecv(lpart.types, urank, recvbuf=nltypes_buf)
        #send positions and receive positions as above
        gcomm.Sendrecv(lpart.rs, urank, recvbuf=nlrs_buf)
        #calc forces
        CPUFrBExactForceCalculator.get_lnl_force_nls(lpart, nltypes_buf, nlrs_buf, units, calc_energy)
        #buf to get force from higher rank
        nlforce_buf = np.zeros(lpart.fs.shape)
        gcomm.Sendrecv(nlrs_buf, lrank, recvbuf=nlforce_buf)
        lpart.fs[:, :] += nlforce_buf


    @classmethod
    def get_nloc_force_sr1(cls, gcomm, urank, lrank, lpart, units, calc_energy):
        #number of particles im about to get
        npart = CPUFrBExactForceCalculator.get_npart(gcomm, urank, lrank, len(lpart.ids))
        npart = npart[0]
        nltypes_buf = np.zeros(npart, dtype=int)
        nlrs_buf = np.zeros((npart, lpart.rs.shape[1]))
        #send types to urank, recv types from lrank
        gcomm.Sendrecv(lpart.types, urank, recvbuf=nltypes_buf)
        #send positions and receive positions as above
        gcomm.Sendrecv(lpart.rs, urank, recvbuf=nlrs_buf)
        #calc forces
        calc_energy = calc_energy and gcomm.Get_rank() > urank
        CPUFrBExactForceCalculator.get_l_force_nls(lpart, nltypes_buf, nlrs_buf, units, calc_energy)


    @classmethod
    def get_npart(cls, gcomm, urank, lrank, npart):
        sbuf = np.array([npart], dtype=int)
        rbuf = np.array([npart], dtype=int)
        gcomm.Sendrecv(sbuf, urank, recvbuf=rbuf, source=lrank)
        return rbuf