
from ..Models.security_model import SL
import json

def gip(rq):
    xff = rq.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0]
    return rq.META.get('REMOTE_ADDR')

class SecMid:
    def __init__(self, get_response):
        self.gr = get_response

    def __call__(self, rq):
        # procesamos la request
        resp = self.gr(rq)

        # solo logueamos si cambia algo o es importante
        if rq.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            # nos saltamos el login y security para no meter ruido
            if '/login/' in rq.path or '/security/' in rq.path:
                return resp

            u = rq.user if rq.user.is_authenticated else None
            ip = gip(rq)
            
            # intentamos guardar info util
            dt = f"Method: {rq.method} | Path: {rq.path} | Status: {resp.status_code}"
            
            # creamos el log
            try:
                SL.objects.create(
                    us=u,
                    et='API_MOD', # modificacion api
                    ip=ip,
                    dt=dt,
                    ua=rq.META.get('HTTP_USER_AGENT', '')[:255]
                )
            except Exception as e:
                print(f"Log Err: {e}")

        return resp
