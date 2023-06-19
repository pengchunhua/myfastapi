import logging

from auth.check_permission import check_perm
from config.router_config import RouterTag
from fastapi import APIRouter, Depends, Query
from models.admin import Admin
from models.response import ResponseModel
from common import (
    db_construct_detail_filter_condition,
    db_get_csv_data,
    insert_picture_to_excel3,
)
from fastapi.responses import StreamingResponse

router = APIRouter()
logger = logging.getLogger("web")
router_name = RouterTag.HISTORY.value  # 路由名称

@router.get("/download", name=f"download history data - {1 << 2}")
async def download(
    start_time: int = Query(..., ge=0, le=7990329600000, description="开始时间"),
    end_time: int = Query(..., ge=0, le=7990329600000, description="结束时间"),
    channel_id: int = Query(..., ge=1, le=7990329600000, description="通道号"),
    file_id: str = Query(None, description="流程文件ID"),
    cell_id: str = Query(None, description="电芯条码"),
    tray_id: str = Query(None, description="托盘ID"),
    admin: Admin = Depends(check_perm(router_name, 1 << 2)),
):
    from io import BytesIO
    condition = db_construct_detail_filter_condition(
        start_time, end_time, file_id, channel_id, cell_id, tray_id
    )
    # 获取历史数据
    workbook, worksheet, max_row = await db_get_csv_data(condition)
    if workbook:
        worksheet = insert_picture_to_excel3(worksheet, max_row)
        output = BytesIO()
        workbook.save(output)
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="application/vnd.ms-excel",
            headers={
                "Content-Disposition": "attachment; filename=history_detail_data.xlsx"
            },
        )
    return ResponseModel(success=False, message="导出文件失败，不存在对应的历史数据", detail={})
