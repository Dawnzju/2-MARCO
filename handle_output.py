from libs import init,Get_detailed_data
import numpy as np
import json
import os
import datetime


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

#MapResults里task的编号从0开始，包含路由的task_graph的编号从1开始
def handle_my_output(tg_file_name,MapResults,task_graph,computation_ability,num_of_rows,output_file_name):
    hyperperiod,num_of_tasks,edges,comp_cost=init(tg_file_name)
    adj_matrix,total_needSend,total_needReceive,execution=Get_detailed_data(num_of_tasks,edges,comp_cost)
    ret_task_graph={}#任务编号从0开始，包括key和out_links
    for i in task_graph.keys():
        ret_task_graph.update({})
        task_graph[i].update({'input_links':[]})
        task_graph[i].update({'start_time':0})
        task_graph[i].update({'visited':0})
        task_graph[i].update({'total_needSend':total_needSend[int(i)]})
        task_graph[i].update({'end_time':0})
        task_graph[i].update({'total_needReceive':total_needReceive[int(i)]})
        mapto=MapResults[int(i)-1]
        task_graph[i].update({'mapto':mapto})
        task_graph[i].update({'exe_time':computation_ability[int(i)-1][mapto]})
        #处理out_link
        for j in range(len(task_graph[i]['out_links'])):
            task_graph[i]['out_links'][j][0]=int(task_graph[i]['out_links'][j][0])
            task_graph[i]['out_links'][j].insert(2,[])
            # task_graph[i]['out_links'][j][3]=[ task_graph[i]['out_links'][j][3] ]
            task_graph[i]['out_links'][j][-2]=mapto
            dest_position=MapResults[task_graph[i]['out_links'][j][0]-1]
            task_graph[i]['out_links'][j][-1]=dest_position
            task_graph[i]['out_links'][j]=[ task_graph[i]['out_links'][j] ]
            #task_graph[i]['out_links'][j].append(0)
    
    #将task的编号改成从0开始，包括key和out_link里的task
    for i in task_graph.keys():
        cur_key=str(int(i)-1)
        ret_task_graph.update({cur_key:task_graph[i]})
        for j in range(len(ret_task_graph[cur_key]['out_links'])):
            ret_task_graph[cur_key]['out_links'][j][0][0]-=1
    
    with open(output_file_name,"w") as f:
        f.write(json.dumps(ret_task_graph,cls=MyEncoder))
    print("write done")

def handle_others_output(input_json,computation_ability,num_of_rows,output_file_name):
    task_graph={}
    with open(input_json,'r') as f1:
        task_graph=json.load(f1)

    for i in task_graph.keys():
        mapto=task_graph[i]['mapto']
        task_graph[i]['exe_time']=computation_ability[int(i)][mapto]
    
    with open(output_file_name,"w") as f2:
        f2.write(json.dumps(task_graph,cls=MyEncoder))
    print("write done")


def read_NoC(NoC_file_name):
    ret=[]
    f=open(NoC_file_name)
    for line in f:
        tmp=[]
        for i in line[1:-2].split(','):
            tmp.append(int(i))
        ret.append(tmp)
    return ret


if __name__ == '__main__':

    MapResults={0: 50, 1: 13, 2: 37, 3: 30, 4: 18, 5: 46, 6: 50, 7: 17, 8: 51, 9: 47, 10: 26, 11: 2}
    task_graph={'1': {'out_links': [['2', 190, [[50, 'N'], [42, 'N'], [34, 'N'], [26, 'E'], [27, 'N'], [19, 'E'], [20, 'E'], [21, 'N']], 0, 0, -1]]}, '2': {'out_links': [['4', 70, [[13, 'S'], [21, 'E'], [22, 'S']], 0, 0, -1], ['5', 140, [[13, 'W'], [12, 'W'], [11, 'S'], [19, 'W']], 0, 0, -1], ['6', 130, [[13, 'E'], [14, 'S'], [22, 'S'], [30, 'S'], [38, 'S']], 0, 0, -1], ['7', 70, [[13, 'S'], [21, 'W'], [20, 'W'], [19, 'W'], [18, 'S'], [26, 'S'], [34, 'S'], [42, 'S']], 0, 0, -1], ['8', 60, [[13, 'S'], [21, 'W'], [20, 'W'], [19, 'W'], [18, 'W']], 0, 0, -1], ['9', 100, [[13, 'W'], [12, 'W'], [11, 'S'], [19, 'S'], [27, 'S'], [35, 'S'], [43, 'S']], 0, 0, -1], ['10', 80, [[13, 'E'], [14, 'E'], [15, 'S'], [23, 'S'], [31, 'S'], [39, 'S']], 0, 0, -1], ['11', 100, [[13, 'S'], [21, 'S'], [29, 'W'], [28, 'W'], [27, 'W']], 0, 0, -1]]}, '4': {'out_links': [['3', 70, [[30, 'W'], [29, 'S']], 0, 0, -1]]}, '5': {'out_links': [['3', 70, [[18, 'S'], [26, 'S'], [34, 'E'], [35, 'E'], [36, 'E']], 0, 0, -1]]}, '6': {'out_links': [['3', 40, [[46, 'W'], [45, 'N']], 0, 0, -1]]}, '7': {'out_links': [['3', 90, [[50, 'E'], [51, 'E'], [52, 'E'], [53, 'N'], [45, 'N']], 0, 0, -1]]}, '8': {'out_links': [['3', 50, [[17, 'E'], [18, 'E'], [19, 'E'], [20, 'E'], [21, 'S'], [29, 'S']], 0, 0, -1]]}, '9': {'out_links': [['3', 100, [[51, 'N'], [43, 'N'], [35, 'E'], [36, 'E']], 0, 0, -1]]}, '10': {'out_links': [['3', 40, [[47, 'W'], [46, 'N'], [38, 'W']], 0, 0, -1]]}, '11': {'out_links': [['3', 80, [[26, 'E'], [27, 'S'], [35, 'E'], [36, 'E']], 0, 0, -1]]}, '3': {'out_links': [['12', 210, [[37, 'W'], [36, 'W'], [35, 'W'], [34, 'N'], [26, 'N'], [18, 'N'], [10, 'N']], 0, 0, -1]]}, '12': {'out_links': []}}

    computation_ability=read_NoC('N12_autocor_Mesh8x8_NoCdescription.txt')
    
    handle_my_output('N12_autocor.tgff',MapResults,task_graph,computation_ability,num_of_rows=8,output_file_name='autocor_Mesh8x8_AIR1_coopti.json')
   

