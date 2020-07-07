# Structural Analysis
Only a set of modules and classes that helps in the structural analysis of linear systems.
## structural.py
This module performs structural analysis of linear time invariant system such as:

  ## The Structural controllability test and the Structural observability test.
  This test are made with the functios `sc(A,B)` or `so(A,C)`. They are both based on the followig conditions:
  
   1. Every node in the graph generated by A, is acessible for a path from a node that recives inputs.**(No isolation condition)**
   2. For $A \in R^n$. The generic rank of the matrix [A B]=n (structural controllabiliry) or [A' C']=n (structural observability). **(Dilation free condition)**
 
  ## Minimum driver node selection and Minimum sensor node selection
  The minimum driver node selection and the minimum sensor selection are based on the 2 condition presented in the structural     
  controlability and observability test.
  
   1. MDNS(A) selects the minimum number of driver nodes of the system to be structural controllable.
   2. MSNS(A) selects the minimum number of sensor nodes of the system to be structural observable.
   
   This two previous sections are based on [[1]](#1).
   
  ## Control profile of the network.
  The control profile of the network is a statistic propriety of the network associated with how the edge distribution affect the driver nodes distribution:  
  1. External dilations: arises when the number of sink of the graph are greater then the number of source nodes. **Ne** 
  2. Internal dilatons:  arises due the nuances of the network, such as diferent edges from the same node. **Ni** 
  3. Number of sources:  the number of source nodes of the system. **Ns**
  
  The sum of these three element is equal to the number of the minum driver nodes selection **Nc**. The control profile is a vector (Ns/Nc,Ns/Nc,Ne/Nc). The      
  function ``control_profile(A)`` returns this vector.
  All this section is based on the work of [[2]](#2).
    
  ## Shows the input-output degree for each node.
  [[1]](#1) Showed that there is a relation between the number of driver nodes and the input output degree of a node of the graph. So a simple function was 
  created to show the degree of each node. The function is `degree(A)`.

  ## structuralsystem.py
  This class creates the structured version of the system based on the matrix A,B,C,D of the state space. For example
  ```python
  A = np.matrix([[-0.0144,0.0144,0],[0.0144,-0.0287,0.0144],[0,0.0144,-0.0206]])
  B = B_three_tank = np.matrix([[6.4935,0],[0,0],[0,6.4935]])
  sys = StructuralSystem(A,B)
  ```
  So you can get the matrix A and B: `sys.A`,`sys.B`. You can use this function with the other matrices of the state space model, and also with only one matrix.
  using `sys.show_A_stru()` we get a spy plot of the matrix A.
  
  ## ssc.py
  It's model that cotains the 2 tests to verify strong structural controllability, these two test were based on the algorithm presented here [[3]](#3) and also in the [SALS toolbox](https://www.mathworks.com/matlabcentral/fileexchange/72648-sals-toolbox) functions ssc1, ssc2.
  1. `ssc1(A,B)` performs the first test.
  2. `ssc2(A,B)` performs the second test.
  3. `ssc(A,B)` use the two privious test to check the strong structural controllability of the system.

# Bibliography:
<a id="1">[1]</a> **Liu, Yang-Yu & Barabasi, Albert-Laszlo. (2016). Control principles of complex systems. Reviews of Modern Physics. 88. 10.1103/RevModPhys.88.035006.**<br>
<a id="2">[2]</a>  **Justin Ruths and Derek Ruths. “Control Profiles of Complex Networks”. In:Science343.6177 (2014), pp. 1373–1376.issn: 0036-8075.doi:10.1126/science.1242063.** <br>
<a id="3">[3]</a> **K. J. Reinschke, F. Svaricek and H. -. Wend, "On strong structural controllability of linear systems," [1992] Proceedings of the 31st IEEE Conference on Decision and Control, Tucson, AZ, USA, 1992, pp. 203-208 vol.1, doi: 10.1109/CDC.1992.371757**. 

If you have any suggestions for another test to be implemented feel free to send an email: emmanuelsampaio@alu.ufc.br<br>
*If you find any issue be free to communicate.*
