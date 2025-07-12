from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from backend.database import get_db
from backend.logging.config import LOG_DIR
import os
import json

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str
    context: dict

class PerformanceMetric(BaseModel):
    timestamp: str
    component: str
    metric: str
    value: float
    message: str

class AuditEntry(BaseModel):
    timestamp: str
    user: str
    action: str
    resource: str
    status: str
    message: str

def parse_log_file(file_path: str) -> List[LogEntry]:
    entries = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    entries.append(LogEntry(**entry))
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return entries

@router.get("/logs", response_model=List[LogEntry])
def get_logs(
    db: Session = Depends(get_db),
    level: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100
):
    """Get application logs."""
    logs = []
    for file in os.listdir(LOG_DIR):
        if file.endswith(".log"):
            file_path = os.path.join(LOG_DIR, file)
            entries = parse_log_file(file_path)
            logs.extend(entries)
    
    if level:
        logs = [l for l in logs if l.level == level.upper()]
    
    if start_date:
        start = datetime.fromisoformat(start_date)
        logs = [l for l in logs if datetime.fromisoformat(l.timestamp) >= start]
    
    if end_date:
        end = datetime.fromisoformat(end_date)
        logs = [l for l in logs if datetime.fromisoformat(l.timestamp) <= end]
    
    return logs[-limit:]

@router.get("/performance", response_model=List[PerformanceMetric])
def get_performance_metrics(
    db: Session = Depends(get_db),
    component: Optional[str] = None,
    metric: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100
):
    """Get performance metrics."""
    metrics = []
    file_path = os.path.join(LOG_DIR, "performance.log")
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if component and entry["component"] != component:
                        continue
                    if metric and entry["metric"] != metric:
                        continue
                    metrics.append(PerformanceMetric(**entry))
                except json.JSONDecodeError:
                    continue
    
    if start_date:
        start = datetime.fromisoformat(start_date)
        metrics = [m for m in metrics if datetime.fromisoformat(m.timestamp) >= start]
    
    if end_date:
        end = datetime.fromisoformat(end_date)
        metrics = [m for m in metrics if datetime.fromisoformat(m.timestamp) <= end]
    
    return metrics[-limit:]

@router.get("/audit", response_model=List[AuditEntry])
def get_audit_logs(
    db: Session = Depends(get_db),
    user: Optional[str] = None,
    action: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100
):
    """Get audit logs."""
    logs = []
    file_path = os.path.join(LOG_DIR, "audit.log")
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if user and entry["user"] != user:
                        continue
                    if action and entry["action"] != action:
                        continue
                    logs.append(AuditEntry(**entry))
                except json.JSONDecodeError:
                    continue
    
    if start_date:
        start = datetime.fromisoformat(start_date)
        logs = [l for l in logs if datetime.fromisoformat(l.timestamp) >= start]
    
    if end_date:
        end = datetime.fromisoformat(end_date)
        logs = [l for l in logs if datetime.fromisoformat(l.timestamp) <= end]
    
    return logs[-limit:]
