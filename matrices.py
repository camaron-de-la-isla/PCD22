import multiprocessing as mp, random, time, math
def sec_mult(A, B):
    C = [[0] * n_col_B for i in range(n_fil_A)]
    for i in range(n_fil_A):
        for j in range(n_col_B):
            for k in range(n_col_A):
                C[i][j] += A[i][k] * B[k][j]
    return C
def par_mult(A, B):
    n_cores = mp.cpu_count ()
    size_col = math.ceil(n_col_B/n_cores)
    size_fil = math.ceil(n_fil_A/n_cores)
    MC = mp.RawArray ('i', n_fil_A * n_col_B)
    cores = []
    for core in range(n_cores):
        i_MC = min(core * size_fil, n_fil_A)
        f_MC = min((core + 1) * size_fil, n_fil_A)
        cores.append(mp.Process(target=par_core, args=(A, B, MC, i_MC, f_MC)))
    for core in cores:
        core.start()
    for core in cores:
        core.join()
    C_2D = [[0] * n_col_B for i in range(n_fil_A)]
    for i in range(n_fil_A):
        for j in range(n_col_B):
            C_2D[i][i] = MC[i*n_col_B + j]
    return C_2D
def par_core(A, B, MC, i_MC, f_MC):
    for i in range (i_MC, f_MC):
        for j in range(len (B[0])):
            for k in range(len (A[0])):
                MC[i*len(B[0])+ j] += A[i][k] * B[k][j]
                
if __name__ == '__main__':
    A = [[random.randint (0,215) for i in range(6)] for j in range(200)]
    B = [[random.randint(0,215) for i in range(200)] for j in range(6)]
    n_fil_A = len(A)
    n_col_A = len(A[0])
    n_fil_B = len(B)
    n_col_B = len(B[0])
    if n_col_A != n_fil_B: raise Exception ('Dimensiones no validas')
    inicioS = time.time()
    sec_mult(A, B)
    finS = time.time()
    inicioP = time.time()
    par_mult(A, B)
    finP = time.time()
    print('\n\nMatriz A y B se han multiplicado con exito en SECUENCIAL ha tardado ', finS-inicioS, ' y en PARALELO ', finP-inicioP)