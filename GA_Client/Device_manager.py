from wmi import WMI

##########################################
# 参数：dev_type
# 0: 所有设备
# 1：usb设备
# 2：显示设备
# 3：音频设备
# ....
# 返回值(字符串列表)："设备标题:设备ID"，以冒号分隔
##########################################
def get_device_id(dev_type):
    devices = []
    dev_id  = []

    if dev_type == 0:
        for dev in WMI().Win32_USBControllerDevice():   # USB设备
            devices.append(dev.Dependent) 
        for dev in WMI().Win32_DesktopMonitor():        # (监视器)显示器
            devices.append(dev)
        for dev in WMI().Win32_SoundDevice():           # 声卡
            devices.append(dev)
    # 以下为单独读取，提高效率
    elif dev_type == 1:
        for dev in WMI().Win32_USBControllerDevice():
            devices.append(dev.Dependent) 
        #print("usb设备：", devices[0].Caption)
    elif dev_type == 2:
        for dev in WMI().Win32_DesktopMonitor():
            devices.append(dev)
        #print("显示器：", devices)
    elif dev_type == 3:
        for dev in WMI().Win32_SoundDevice():
            devices.append(dev)
        #print("声卡: ", devices[0].Caption)
    else:
        print("非法参数")
        return dev_id
    for num in range(len(devices)):
        temp = devices[num].Caption + ":" + devices[num].PNPDeviceID
        dev_id.append(temp)

    return dev_id

# 返回未连接设备
def check_device(dev_dict, dev_type):
    cgf_devID    = []
    disconn_list = []
    #device_all = get_usb_id() + get_serial_id()
    device_all = get_device_id(dev_type)

    for key, val in dev_dict.items():    # 把配置文件里的设备ID读出来
        cgf_devID.append(val)

    for id in range(0, len(cgf_devID)):      # 遍历配置文件ID
        connect_flag = False
        for num in range(len(device_all)-1, -1, -1):   # 在所有设备中找,从后往前找
            if cgf_devID[id] in device_all[num]:
                print("已接入设备：",cgf_devID[id])
                connect_flag = True
                break
        if connect_flag is False:
            #print("该设备没有接入：",cgf_devID[id])
            disconn_list.append(cgf_devID[id])
    return disconn_list