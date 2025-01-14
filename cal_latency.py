import sys
import os
from typing import List

data: List[str] = []
num_sockets = 0
num_cores = 0
dram_nodes = []
cxl_nodes = []

event_name_match = {
    'IA_MISS_DRD_LOCAL': 'dram',
    'IA_MISS_CXL_ACC': 'cxl',
}

def cal_sockets_cores(header_line: str):
    global num_sockets
    global num_cores
    headers = header_line.split(",")
    valid_entries = [entry for entry in headers if "SKT" in entry]
    # 提取 Socket 和 Core
    sockets = {entry.split("C")[0] for entry in valid_entries}  # 提取唯一的 Socket 标识
    cores = {entry.split("C")[1] for entry in valid_entries}  # 提取唯一的 Core 标识
    # 结果
    num_sockets = len(sockets)
    num_cores = len(cores)
    print(f"num_sockets: {num_sockets}, num_cores: {num_cores}")


def cal_latency():

    # group 1
    # cha/config=56320275519635766,name=UNC_CHA_TOR_OCCUPANCY.IA_MISS_DRD_LOCAL
    # cha/config=56320275519635765,name=UNC_CHA_TOR_INSERTS.IA_MISS_DRD_LOCAL
    # cha/config=1,name=UNC_CHA_CLOCKTICKS
    # ;
    # # group 2
    # cha/config=56320825275449654,name=UNC_CHA_TOR_OCCUPANCY.IA_MISS_DRD_REMOTE
    # cha/config=56320825275449653,name=UNC_CHA_TOR_INSERTS.IA_MISS_DRD_REMOTE
    # cha/config=1,name=UNC_CHA_CLOCKTICKS
    # ;
    # # group 3
    # cha/config=1206966357992669494,name=UNC_CHA_TOR_OCCUPANCY.IA_MISS_CXL_ACC
    # cha/config=1206966357992669493,name=UNC_CHA_TOR_INSERTS.IA_MISS_CXL_ACC
    # cha/config=257,name=UNC_CXLDP_CLOCKTICKS
    # ;
    latency_type = data[0].split(",")[2].split(".")[1]
    latency_type = event_name_match[latency_type] # dram or cxl
    occupancy_data = data[0].split(",")[5:]
    insert_data = data[1].split(",")[5:]
    clock_data = data[2].split(",")[5:]

    latencys = [0 for _ in range(num_sockets)]

    for socket in range(num_sockets):
        # 确保行长度足够,避免索引错误
        core_latencys = []
        for core in range(num_cores):
            index = socket * num_cores + core
            if index >= len(occupancy_data):
                print(len(occupancy_data))
                break
            occupancy_val = int(occupancy_data[index])
            insert_val = int(insert_data[index])
            clock_val = int(clock_data[index])
            if insert_val == 0 or clock_val == 0:
                continue
            latency = 1000000000 * occupancy_val / insert_val / clock_val
            core_latencys.append(latency)

        latencys[socket] = int(sum(core_latencys) / len(core_latencys))

    print(f"{latency_type:<5} Latency:", end=" ")
    for socket in range(num_sockets):
        print(f"Socket {socket} {latencys[socket]:>4}(ns) | ", end=" ")
    print("")
    
    write_vtism_interface(latency_type, latencys)

split_line_counter = 0

def insert_line(line: str):
    global data, split_line_counter
    if split_line_counter == 0:
        print('-' * 50)
    split_line_counter += 1
    
    data.append(line)
    if len(data) == 3:
        cal_latency()
        data = []
    
    if split_line_counter == 6:
        split_line_counter = 0

def check_node_resources():
    # 定义节点路径
    base_path = "/sys/devices/system/node/"
    global cxl_nodes, dram_nodes
    
    # 遍历所有节点
    for node_dir in os.listdir(base_path):
        if node_dir.startswith("node"):  # 筛选节点目录,例如 node0, node1...
            node_path = os.path.join(base_path, node_dir)
            has_cpu = os.path.exists(os.path.join(node_path, "cpulist"))
            
            # 读取 CPU 和内存信息
            cpu_list = None
            if has_cpu:
                cpu_list_file = os.path.join(node_path, "cpulist")
                with open(cpu_list_file, "r") as f:
                    cpu_list = f.read().strip()
                    if cpu_list == "":
                        has_cpu = False
                        cxl_nodes.append(int(node_dir[4:]))
            
            if has_cpu:
                dram_nodes.append(int(node_dir[4:]))
                        
    # print(f"cpu_nodes: {dram_nodes}")
    # print(f"cxl_nodes: {cxl_nodes}")

def write_vtism_interface(node_type, latencys):
    
    for i, node in enumerate(dram_nodes):
        if node_type == "dram":
            with open(f"/sys/kernel/mm/vtism/pcm/node{node}/latency", "w") as f:
                f.write(str(latencys[i]))
        elif node_type == "cxl":
            with open(f"/sys/kernel/mm/vtism/pcm/node{node}/to_cxl_latency", "w") as f:
                f.write(str(latencys[i]))

def main():
    if not os.path.exists("/sys/kernel/mm/vtism/pcm"):
        print("VTISM not supported")
        exit()
        
    check_node_resources()
        
    try:
        line1 = sys.stdin.readline()[:-1]
        cal_sockets_cores(line1)
        line2 = sys.stdin.readline()
        # print(line2)
        for line in sys.stdin:
            insert_line(line)
    except KeyboardInterrupt:
        # 用户中断程序时的处理
        print("Program interrupted.")
    except Exception as e:
        # 捕获其他可能的异常
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
