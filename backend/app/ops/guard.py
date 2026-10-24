"""CR-07 REQ-SEC-012 (OWASP API5:2023, API8:2023): endpoint ที่มีไว้สำหรับ ops ในโหมด production ต้องมี X-Ops-Token
โหมด test และ development เปิดไว้ให้ test และหน้าแอดมินบนเครื่องนักพัฒนาใช้ได้ (AC-00-06)"""
import hmac

from fastapi import Header, HTTPException

from app import config


def require_ops(x_ops_token: str | None = Header(default=None)) -> None:
    if config.app_env() != "production":
        return
    expected = config.ops_token()
    if not expected or not x_ops_token or not hmac.compare_digest(x_ops_token, expected):
        raise HTTPException(403, "ต้องใช้สิทธิ์ของ Ops")
