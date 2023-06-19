def db_construct_detail_filter_condition(
    start_time: int,
    end_time: int,
    file_id: str,
    channel_id: int,
    cell_id: str,
    tray_id: str,
):
    """
    构建详情信息的过滤条件
    """
    condition = {
        "computer_time": {"$gte": start_time, "$lte": end_time},
        # "file_id": file_id,
        # "channel_id": channel_id,
    }

    if file_id:
        condition["file_id"] = file_id

    if channel_id:
        condition["channel_id"] = channel_id

    if cell_id:
        condition["cell_id"] = cell_id

    if tray_id:
        condition["tray_id"] = tray_id

    return condition
  
  async def db_get_csv_data(condition: Dict):
    """
    导出csv数据
    """
    from openpyxl import Workbook

    has_data = False
    max_row = 0
    workbook = Workbook()
    worksheet = workbook["Sheet"]
    title = [
        "通道",
        "工步号",
        "文件ID",
        "文件名",
        "工步类型",
        "工步时间",
        "电脑时间",
        "极耳电压",
        "电芯电压",
        "电流",
        "容量",
        "能量",
        "温度",
        "负压",
        "压差",
        "阻抗",
        "电芯条码",
        "托盘号",
        "环境温度",
        "电源效率",
        "PFC温度",
        "DCDC温度",
    ]
    result = await HistoryDetailData.find(condition).to_list()
    for item in result:
        max_row += 1
        del item.id
        del item.revision_id
        if not has_data:
            worksheet.append(title)
            has_data = True
        item.time = time_to_hour(item.time)
        item.computer_time = time_format(item.computer_time/1000)
        item.step_type = convert_step_type(item.step_type)
        worksheet.append(list(dict(item).values()))
    return (workbook, worksheet, max_row + 1) if has_data else (None, None, 0)

def time_to_hour(time: int, fmt: str="%H:%M:%S.%f"):
    """
    时间格式化
    """
    return datetime.utcfromtimestamp(time).strftime(fmt)


def time_format(time: int, fmt: str="%Y-%m-%d %H:%M:%S"):
    """
    时间格式化
    """
    return datetime.fromtimestamp(time).strftime(fmt)

def convert_step_type(step_type: int):
    """将工步类型转换为中文"""
    mapping = {
        1: "恒流充电",
        2: "恒流放电",
        3: "恒压充电",
        4: "恒压放电",
        5: "恒压恒流充电",
        6: "恒压恒流放电",
        7: "恒功率充电",
        8: "恒功率放电",
        9: "搁置",
        10: "循环开始",
        11: "循环结束",
        12: "跳转" 
    }
    return mapping.get(step_type, "未知")


def insert_picture_to_excel3(worksheet, max_row):
    """插入图片到excel中"""
    from openpyxl.chart import LineChart, Reference

    chart = LineChart()
    chart.height = 16
    chart.width = 16 * 2
    chart.title = "voltage and current"
    chart.legend.label = "voltage and current"
    chart.y_axis.title = "voltage(mV)"
    chart.x_axis.title = "time"

    # 设置 X 和 Y 数据的范围
    x_data = Reference(worksheet, min_col=7, min_row=2, max_row=max_row)
    y_data1 = Reference(worksheet, min_col=8, min_row=1, max_row=max_row)
    y_data2 = Reference(worksheet, min_col=9, min_row=1, max_row=max_row)


    # 将端口电压和极耳电压数据添加到曲线图中
    chart.add_data(y_data1, titles_from_data=True)
    chart.add_data(y_data2, titles_from_data=True)
    chart.set_categories(x_data)
    # chart.legend.position= "tr"

    # 将电流添加到图表中
    chart2 = LineChart()
    y_data3 = Reference(worksheet, min_col=10, min_row=1, max_row=max_row)
    chart2.add_data(y_data3, titles_from_data=True)
    chart2.y_axis.title = "current(mA)"

    # 添加次坐标轴
    chart2.y_axis.axId = 200
    chart2.y_axis.crosses = "max"
    chart += chart2

    # 将曲线图插入工作表
    worksheet.add_chart(chart) 
    return worksheet
