import json

file_path = "perfmon/SPR/events/sapphirerapids_uncore.json"
cxl_file_path = "perfmon/SPR/events/sapphirerapids_uncore_experimental.json"
# file_path = "perfmon/scripts/perf/sapphirerapids/uncore-cache.json"

# UNC_PMON_CTL_EVENT(0x35) + UNC_PMON_CTL_UMASK(0x01) + UNC_PMON_CTL_UMASK_EXT(0x10C80B82)


def calculate_config_args(event):
    print("-" * 50)
    print(f"[{event['EventName']}]")
    event_code = int(event["EventCode"], 16)
    umask = int(event["UMask"], 16)
    umask_ext = int(event["UMaskExt"], 16)
    counter = event["Counter"]
    # 16 进制输出
    print(f"Event Code: 0x{event_code:0x} UMask: 0x{umask:0x} Counter: {counter}")
    # 模拟C代码的位操作,并限制结果到64位
    config_val = (event_code + (umask << 8) + (umask_ext << 32)) & 0xFFFFFFFFFFFFFFFF  # 限制结果为64位
    print(f"Config Value: {config_val}")
    print("-" * 50)

    config_args = f'cha/config={config_val},name={event["EventName"]}\n'
    return config_args


def main():

    with open(file_path) as f:
        data = json.load(f)

    with open(cxl_file_path) as f:
        cxl_data = json.load(f)
    
    data = [*data["Events"], *cxl_data["Events"]]
    # event_name = input("Enter the event name: ")

    local_ddr_events = [
        "UNC_CHA_TOR_OCCUPANCY.IA_MISS_DRD_LOCAL",
        "UNC_CHA_TOR_INSERTS.IA_MISS_DRD_LOCAL",
        "UNC_CHA_CLOCKTICKS",
    ]
    # remote_ddr_events = [
    #     "UNC_CHA_TOR_OCCUPANCY.IA_MISS_DRD_REMOTE",
    #     "UNC_CHA_TOR_INSERTS.IA_MISS_DRD_REMOTE",
    #     "UNC_CHA_CLOCKTICKS",
    # ]
    
    cxl_events = [
        "UNC_CHA_TOR_OCCUPANCY.IA_MISS_CXL_ACC",
        "UNC_CHA_TOR_INSERTS.IA_MISS_CXL_ACC",
        "UNC_CXLDP_CLOCKTICKS"
    ]
    needed_events = local_ddr_events + cxl_events

    config_args = ["sudo", "./bin/pcm-raw", "-csv=1.csv", "-el", "event_file.txt", "-tr"]
    event_file_data = []
    for needed_event in needed_events:
        for event in data:
            if event["EventName"] == needed_event:
                event_file_data.append(calculate_config_args(event))
                break

    event_file_data = " ".join(event_file_data)
    print(event_file_data)


if __name__ == "__main__":
    main()
