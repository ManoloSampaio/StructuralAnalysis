import numpy as np

def ssc1(A,B):
    """ 
      This function performs the algorithm 1 from the paper:
      Reinschke, Svaricek and Wend:K. J. Reinschke, F. Svaricek, H. D. Wend: On strong structural 
      controllability of linear systems. Proceedings of the 31. IEEE 
      Conference on Decision and Control, pp. 203-208, vol 1 1992.
      This algorithm checks a full rank condition defined on the paper.

    Args:
        A (np.matrix): The structured version of the state matrix. 
        B (np.matrix): The structured version of the input matrix.

    Returns:
        boolean: Return True if the condition was respect and False otherwise.
    """
    n_line = len(A)
    m_col = len(B[0][:])
    # M = [A B]
    M = np.concatenate((A,B),axis=1)
    i = n_line-1 # Index of the lines.
    j = m_col+n_line-1 # Index of the columns
    ending_codiing_cond = False # Condition to finish the code
    while not(ending_codiing_cond):
        submatrix = M[0:i+1,0:j+1] # submatrix of X 
        v,min_col= calculatev(submatrix) 
        # v indicates if the column with the minimum number of non zeros, has more than one element.
        # If it has more than one, so the matrix [A B] is not in the form III and the system is not ssc?.
        if v!=1:
            return False
        else:
        # Else I going to change the position of the 
            min_line = np.nonzero(submatrix[:,min_col])[0]
            if min_line!=i:
                aux_matrix = M[i,:]
                M[i,:] = M[min_line,:]
                M[min_line,:] = aux_matrix
            if min_col!=j:
                aux_matrix = M[:,j]
                M[:,j]=M[:,min_col]
                M[:,min_col]=aux_matrix
        i = i-1
        j = j-1
        if i==0:
            return True

def ssc2(A,B):
    """
    This function performs the algorithm 1 from the paper:
      Reinschke, Svaricek and Wend:K. J. Reinschke, F. Svaricek, H. D. Wend: On strong structural 
      controllability of linear systems. Proceedings of the 31. IEEE 
      Conference on Decision and Control, pp. 203-208, vol 1 1992.
      This algorithm checks the second condition for strong structural controllability defined on the paper.

    Args:
        A ([type]): [description]
        B ([type]): [description]

    Returns:
        [type]: [description]
    """
    n_line = len(A)
    m_col = len(B[0][:])
    M_bar,X= create_M_bar(A,B)
    i = n_line-1
    j = m_col+n_line-1
    ending_codiing_cond = False
    while not(ending_codiing_cond):
        submatrix = M_bar[0:i+1,0:j+1]
        v,min_col = calculatev_mod(submatrix,X)
        if v!=1:
            return False
        else:
            min_line = np.nonzero(submatrix[:,min_col])[0]
            if min_line!=i:
                aux_X = X[i,:]
                aux_matrix = M_bar[i,:]
                M_bar[i][:] = M_bar[min_line,:]
                X[i][:] = X[min_line,:]
                M_bar[min_line,:] = aux_matrix
                X[min_line,:] = aux_X
            if min_col!=j:
                aux_X = X[:,j]
                aux_matrix = M_bar[:,j]
                M_bar[:,j]=M_bar[:,min_col]
                X[:,j] = X[:,min_col]
                M_bar[:,min_col]=aux_matrix
                X[:,min_col] = aux_X
        i = i-1
        j = j-1
        if i==0:
            return True    

def calculatev(submatrix):
    dict_aux = {}
    for j in range(len(submatrix[0,:])):
        non_zero = np.count_nonzero(submatrix[:,j])
        if non_zero!=0:
            dict_aux[j]=non_zero
    index_and_value=min(dict_aux.items(), key=lambda x: x[1])
    min_col = index_and_value[0]
    v = index_and_value[1]  
    return v,min_col

def calculatev_mod(submatrix,X):
    dict_aux = {}
    for j in range(len(submatrix[0,:])):
        non_zero = np.count_nonzero(submatrix[:,j])
        if non_zero!=0:
            dict_aux[j]=non_zero
            if np.count_nonzero(X[:,j])!=0:
                dict_aux[j]=dict_aux[j]+1
    index_and_value=min(dict_aux.items(), key=lambda x: x[1])
    min_col = index_and_value[0]
    v = index_and_value[1]  
    return v,min_col

def create_M_bar(A,B):
    """ Creates a concatenate matrix [A' B], where A' is a matrix
    with allmost all values equal to A, despite:
        A_{ii}=0 -> A'_{ii}=1
    This function also returns X, which is a matrix. X is a diagonal matrix  it going to be usefull to verify
    the second condition of structural controllablity.
    Args:
        A ([type]): [description]
        B ([type]): [description]

    Returns:
        [type]: [description]
    """
    n = len(A)
    m = len(B[0][:])
    A_new = A
    X = np.zeros((n,n+m))
    for i in range(0,len(A)):
        if A[i][i]!=0:
            X[i][i]=1
        else:
            A_new[i][i]=1
    M_bar = np.concatenate((A_new,B),axis=1)
    return M_bar,X
def ssc(A,B):
    """ 
    This fuction verify if the pair (A,B) is approved
    In the first and the second condition defined by the paper:
    Reinschke, Svaricek and Wend:K. J. Reinschke, F. Svaricek, H. D. Wend: On strong structural 
    controllability of linear systems. Proceedings of the 31. IEEE 
    Conference on Decision and Control, pp. 203-208, vol 1 1992. 
    If it pass, so the system is strong structural controllable.
    Otherwise, the system is not strong structural controllable.

    Args:
        A (np.matrix): The structured version of the state matrix.
        B (np.matrix): The structured version of the input matrix.

    Returns:
        [type]: [description]
    """
    if ssc1(A,B) and ssc2(A,B):
        return True
    else:
        return False