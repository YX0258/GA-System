from serial.tools import list_ports
from win32com.client import GetObject

# 获取接入到计算机的所有USB设备的ID
def get_usb_id():
    usb_list = []
    wmi = GetObject ("winmgmts:")
    for usb in wmi.InstancesOf ("win32_usbcontrollerdevice"):   # 获取USB设备详细信息
        s = usb.Dependent
        usb_list.append(s[s.find("DeviceID="):])                # 获取USB设备ID
    return usb_list

# 获取接入到计算机的所有串口设备的ID
def get_serial_id():
    serial_ID = []
    serial_info = list(list_ports.comports())   # 获取串口信息，获取端口号、ID等
    for s in serial_info:
        serial_ID.append(s.hwid)                # 获取每个串口ID
    return serial_ID

# 返回未连接设备
def check_device(device_dict):
    cgf_devID    = []
    disconn_list = []
    device_all = get_usb_id() + get_serial_id()

    for key, val in device_dict.items():    # 把配置文件里的设备ID读出来
        cgf_devID.append(val)

    for id in range(0, len(cgf_devID)):      # 遍历配置文件ID
        connect_flag = False
        for num in range(len(device_all)-1, -1, -1):   # 在所有设备中找,从后往前找
            if cgf_devID[id] in device_all[num]:
                #print("已接入设备：",cgf_devID[id])
                connect_flag = True
                break
        if connect_flag is False:
            #print("该设备没有接入：",cgf_devID[id])
            disconn_list.append(cgf_devID[id])
    return disconn_list