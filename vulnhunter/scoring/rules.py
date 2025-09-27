def score_findings(enriched_list):
    """
    Simple additive scoring:
      +3 per login form with password field
      +1 per missing common security header
    """
    scored = []
    for e in enriched_list:
        s = 0
        tags = []
        web = e.get("web", {}) or {}
        forms = web.get("forms") or []
        if any(f.get("has_password") for f in forms):
            s += 3
            tags.append("login_form")
        missing = web.get("missing_headers") or []
        if missing:
            s += len(missing)
            tags.append("missing_headers")
        scored.append({"host": e["host"], "score": s, "tags": list(set(tags)), "meta": e})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored
