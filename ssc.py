import numpy as np

def ssc1(A,B):
    """ 
      This function performs the algorithm 1 from the paper:
      Reinschke, Svaricek and Wend:K. J. Reinschke, F. Svaricek, H. D. Wend: 
      On strong structural controllability of linear systems. Proceedings of the 31. IEEE 
      Conference on Decision and Control, pp. 203-208, vol 1 1992.
      This algorithm checks a full rank condition defined in the paper.
    
    Args:
        A (np.matrix): The structured version of the state matrix. 
        B (np.matrix): The structured version of the input matrix.

    Returns:
        boolean: True if the condition has been met and False otherwise.
    """
    n_line = len(A)
    m_col = len(B[0][:])
    # M = [A B]
    M = np.concatenate((A,B),axis=1)
    i = n_line-1 # Index of the lines.
    j = m_col+n_line-1 # Index of the columns
    ending_cond = False # Condition to maintain the loop.
    while not(ending_cond):
        submatrix = M[0:i+1,0:j+1] # submatrix of X 
        v,min_col= calculatev(submatrix) 
        # v is the number of elements in the column with 
        # the minimum number of nonzero values.
        # min_col is the column with the minimum number of nonzeros.
        # If min_col has more than one nonzero element, so the matrix [A B] is not in the form III and the system is not ssc.
        if v!=1:
            return False
        else:
        # Set min_line as the line with the nozero element of the min_col.
            min_line = np.nonzero(submatrix[:,min_col])[0]
            # If the min_line is different from  i so switch these two lines.
            if min_line!=i:
                aux_matrix = M[i,:]
                M[i,:] = M[min_line,:]
                M[min_line,:] = aux_matrix
            # If the min_col is different from j so switch these two columns.
            if min_col!=j:
                aux_matrix = M[:,j]
                M[:,j]=M[:,min_col]
                M[:,min_col]=aux_matrix
        # Reduce the submatrix size:
        i = i-1
        j = j-1
        # If v is equal to 1 after n permutations, so the you pass in the condition.
        if i==0:
            return True

def ssc2(A,B):
    """
      This function performs the modified version of algorithm 1 from the paper:
      Reinschke, Svaricek and Wend:
      K. J. Reinschke, F. Svaricek, H. D. Wend: On strong structural controllability of linear systems. Proceedings of the 31. IEEE 
      Conference on Decision and Control, pp. 203-208, vol 1 1992.
      This algorithm checks the second condition for strong structural controllability defined in the paper.
    
    Args:
        A (np.matrix): The structured version o the state matrix A.
        B (np.matrix): The structured version of the input matrix B.

    Returns:
        boolean: True if the condition has been met and False otherwise.
    """
    n_line = len(A) 
    m_col = len(B[0][:])
    
    # Create the matrix of the second test M_bar = [A_bar B]. 
    # X is a diagonal matrix, with the propriety: x_ii!=0 <=> a_ii!=0. 
    M_bar,X= create_M_bar(A,B)
    i = n_line-1
    j = m_col+n_line-1
    
    ending_cond = False
    while not(ending_cond):
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
    """
    Calculates the number of nonzero elements in the column with the minimum number of nonzero elements.
    This column should no be a null vector.
    
    Args:
    submatrix(np.matrix): The submatrix of M.
    
    Returns:
    v: The minimum number of elements in the column with the minimum number of nonzero values.
    min_col: The column with the minimum number of nonzero elements.
    
    """
    dict_aux = {} 
    # The keys of the dictionary going to be the column value, and the data is the number of nonzero elements of the column.
    for j in range(len(submatrix[0,:])):
        non_zero = np.count_nonzero(submatrix[:,j]) # Checks the number of nonzero elements of a column.
        if non_zero!=0:
            dict_aux[j]=non_zero # Creates a new key on the dictionary.
    index_and_value=min(dict_aux.items(), key=lambda x: x[1])     # Verifies the key associated with the minimum number of elements
    min_col = index_and_value[0] # The Key is the column withe the minimum number of nonzero values.
    v = index_and_value[1]   # Is the number of elements in this column.
    return v,min_col
def calculatev_mod(submatrix,X):
    """
        Summary:
        Calculates the number of nonzero elements in the column with the minimum number of nonzero elements.
        This column should no be a null vector.
        The modification is that if the j column of the matrix A of 
        the system contains a nonzero element, we going to increase by 1 the number of the nonzero element of the submatrix.
    
        Args:
    
        submatrix(np.matrix)= The submatrix of M.
        X(np.matrix)= X is a diagonal matrix, with the propriety: x_ii!=0 <=> a_ii!=0.
    
        Returns:
    
        v: The minimum number of elements in the column with the minimum number of nonzero values.
        min_col: The column with the minimum number of nonzero elements.
    """
    dict_aux = {}
    for j in range(len(submatrix[0,:])):
        non_zero = np.count_nonzero(submatrix[:,j])
        if np.count_nonzero(X[:,j])!=0:
            non_zero=non_zero+1
        if non_zero!=0:
            dict_aux[j]=non_zero
    index_and_value=min(dict_aux.items(), key=lambda x: x[1])
    min_col = index_and_value[0]
    v = index_and_value[1]  
    return v,min_col

def create_M_bar(A,B):
    """ Creates a concatenate matrix [A_bar B], where A_bar is a matrix
    with allmost all values equal to A, but the following are different:
        A_{ii}=0 -> A_bar_{ii}=1
    Args:
        A (np.matrix): The structured version of the state matrix. 
        B (np.matrix): The structured version of the input matrix.

    Returns:
        M_bar = [A_bar B]
        # X: is a diagonal matrix, with the propriety: x_ii!=0 <=> a_ii!=0
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
    This function verifies if the pair (A, B) is approved
    in the first and in the second condition defined by the paper:
    Reinschke, Svaricek, and Wend: K. J. Reinschke, F. Svaricek, H. D. Wend: 
    On strong structural controllability of linear systems. Proceedings of the 31. IEEE 
    Conference on Decision and Control, pp. 203-208, vol 1 1992. 
    If it passes, so the system is strong structural controllable.
    Otherwise, the system is not a strong structural controllable system.

    Args:
        A (np.matrix): The structured version of the state matrix.
        B (np.matrix): The structured version of the input matrix.

    Returns:
        boolean: True if the system is strong structural controllable. Otherwise false.
    """
    if ssc1(A,B) and ssc2(A,B):
        return True
    else:
        return False
