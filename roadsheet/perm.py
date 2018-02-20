from .models import Profile


def isOperator(req):
    try:
        p = Profile.objects.get(user=req.user.id)
        if p.role == "operator":
            return True
        else:
            return False
    except Exception:
        return False

def isServiceman(req):
    try:
        p = Profile.objects.get(user=req.user.id)
        if p.role == "serviceman":
            return True
        else:
            return False
    except Exception:
        return False

