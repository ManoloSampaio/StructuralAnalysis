import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class StructuredSystem:
    def __init__(self,A=0,B=0,C=0,D=0):
        self.A = self.struversion(A)
        self.B = self.struversion(B)
        self.C = self.struversion(C)
        self.D = self.struversion(D)
    
    def show_A_stru(self,line_width=0.2,squareform=True,
                    color_map="YlGnBu",v_min=0,v_max=3,
                    color_bar=False,x_size=10,y_size=10,savefig=False,path_to='A_structure.eps'):
        
        plt.figure(figsize=(x_size,y_size))
        state_ticks_labels = self.set_ticks_name(len(self.A),1)
        sns.heatmap(self.A,linewidth=line_width,
                    square=squareform,cmap=color_map,
                    vmin=v_min, vmax=v_max,cbar=color_bar,
                    xticklabels=state_ticks_labels,
                    yticklabels=state_ticks_labels)
        if savefig:
            plt.savefig(path,format='eps')
        plt.show()

    def show_B_stru(self,line_width=0.2,squareform=True,
                    color_map="YlGnBu",v_min=0,v_max=3,
                    color_bar=False,x_size=10,y_size=10,savefig=False,path_to='B_structure.eps'):
        
        state_ticks_labels = self.set_ticks_name(len(self.A),1)
        inputs_ticks_labels = self.set_ticks_name(len(self.B[0,:]),2)

        plt.figure(figsize=(x_size,y_size))
        
        sns.heatmap(self.B,linewidth=line_width,
                    square=squareform,cmap=color_map,
                    vmin=v_min, vmax=v_max,cbar=color_bar,
                    xticklabels=inputs_ticks_labels,
                    yticklabels=state_ticks_labels)

        if savefig:
            plt.savefig(path,format='eps')
        plt.show()
    
    def show_C_stru(self,line_width=0.2,squareform=True,
                    color_map="YlGnBu",v_min=0,v_max=3,
                    color_bar=False,x_size=10,y_size=10,savefig=False):
        
        state_ticks_labels = set_ticks_name(self.A,1)
        sensor_ticks_labels = set_ticks_name(self.C,2)

        plt.figure(figsize=(x_size,y_size))
        
        sns.heatmap(self.C,linewidth=line_width,
                    square=squareform,cmap=color_map,
                    vmin=v_min, vmax=v_max,cbar=color_bar,
                    xticklabels=state_ticks_labels,
                    yticklabels=sensor_ticks_labels)
        
        if savefig:
            plt.savefig("C_structure",format='eps')
        
        plt.show()
    
    def show_D_stru(self,line_width=0.2,squareform=True,
                    color_map="YlGnBu",v_min=0,v_max=3,
                    color_bar=False,x_size=10,y_size=10,savefig=False):
        
        state_ticks_labels  = set_ticks_name(len(self.A),1)
        inputs_ticks_labels = set_ticks_name(len(self.D),2)
        
        plt.figure(figsize=(x_size,y_size))
        
       
        

        sns.heatmap(self.D,linewidth=line_width,
                    square=squareform,cmap=color_map,
                    vmin=v_min, vmax=v_max,cbar=color_bar,
                    xticklabels=state_ticks_labels,
                    yticklabels=state_ticks_labels)
        
        if savefig:
            plt.savefig("D_structure",format='eps')
        
        plt.show()
    
    def set_ticks_name(self,number_elements,variable_type):
        answer = []
        
        if variable_type==1:
            for i in range(0,number_elements):
                answer.append(f"x_{i+1}")
        
        if variable_type==2:
            for i in range(0,number_elements):
                answer.append(f"u_{i+1}")
        
        return answer
    
    def struversion(self,matrix):
        matrix = np.matrix(matrix)
        matrix = np.where(matrix!=0,1,matrix)
        return matrix
    
