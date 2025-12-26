from pydantic import BaseModel, HttpUrl, field_validator, Field
import socket
from urllib.parse import urlparse
from datetime import datetime
from typing import Optional
from app.models.mission import MissionStatus

class MissionCreate(BaseModel):
    brand_name: str = Field(..., min_length=1, max_length=100)
    target_url: HttpUrl = Field(..., max_length=2048)

    @field_validator('target_url')
    @classmethod
    def prevent_ssrf(cls, v: HttpUrl) -> HttpUrl:
        url_str = str(v)
        hostname = urlparse(url_str).hostname
        if not hostname:
            raise ValueError("Invalid URL")
        forbidden_prefixes = ('127.', '10.', '172.16.', '172.31.', '192.168.', '0.', '169.254.')
        try:
            ip = socket.gethostbyname(hostname)
            if any(ip.startswith(prefix) for prefix in forbidden_prefixes):
                raise ValueError("Accès aux réseaux privés interdit (Anti-SSRF)")
        except socket.gaierror:
            pass
        return v

class MissionResponse(BaseModel):
    id: int
    brand_name: str
    target_url: str
    status: MissionStatus
    evidence_path: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None
    class Config:
        from_attributes = True
