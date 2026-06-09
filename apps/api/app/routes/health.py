from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """服务健康检查接口。

    前端、部署平台或监控系统可以通过这个接口判断后端是否可用。
    """

    return {"status": "ok"}
