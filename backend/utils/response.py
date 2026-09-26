from flask import jsonify

def api_response(success=True, message="", data=None, error=None, status_code=200):
    """
    Standardized REST API JSON response builder.
    """
    payload = {
        "success": success,
        "message": message,
        "data": data if data is not None else {},
    }
    if error is not None:
        payload["error"] = error
    return jsonify(payload), status_code
