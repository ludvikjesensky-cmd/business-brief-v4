from __future__ import annotations
import time, logging
class EventLogger:
    def __init__(self,client,component="TECHNICIAN"): self.db=client; self.component=component
    def emit(self,event,*,stage=None,severity="INFO",status=None,message=None,duration_ms=None,run_id=None,edition_id=None,source_id=None,job_id=None,metadata=None):
        row={"component":self.component,"event":event,"severity":severity,"metadata":metadata or {}}
        for k,v in {"stage":stage,"status":status,"message":message,"duration_ms":duration_ms,"run_id":run_id,"edition_id":edition_id,"source_id":source_id,"job_id":job_id}.items():
            if v is not None: row[k]=v
        try:
            self.db.table("pipeline_events").insert(row).execute()
        except Exception:
            logging.getLogger(__name__).exception("Pipeline event logging failed: %s", event)
    def timed(self,event,**base): return _Timer(self,event,base)
class _Timer:
    def __init__(self,logger,event,base): self.logger=logger;self.event=event;self.base=base
    def __enter__(self): self.t=time.perf_counter();return self
    def __exit__(self,typ,val,tb):
        ms=round((time.perf_counter()-self.t)*1000)
        base = dict(self.base)
        severity = base.pop("severity", "INFO")
        status = base.pop("status", None)
        message = base.pop("message", None)
        self.logger.emit(self.event,duration_ms=ms,severity="ERROR" if typ else severity,status="FAILED" if typ else status,message=str(val) if typ else message,**base)
        return False
