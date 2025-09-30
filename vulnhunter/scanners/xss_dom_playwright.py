*** Begin Patch
*** Update File: requirements.txt
@@
 Jinja2>=3.1
 pytest>=7.0
 httpx>=0.27.0
+playwright>=1.30.0
*** End Patch
*** Begin Patch
*** Add File: vulnhunter/scanners/xss_dom_playwright.py
+"""
+Headless DOM-XSS validation using Playwright (sync API).
+
+Behavior:
+- For each URL, try benign marker injections via query param and via form inputs.
+- Consider validation positive if the marker appears in the final DOM (documentElement.innerHTML).
+- Requires explicit consent flag in CLI before running.
+
+Note: This is an intrusive test. Only use on targets you own/have permission for.
+"""
+from typing import List, Dict, Any
+import logging
+from urllib.parse import urlparse, urlencode, urlunparse, parse_qsl
+
+LOG = logging.getLogger("vulnhunter.scanners.xss_dom_playwright")
+
+DEFAULT_MARKER = "VULNHUNTER_MARKER_3b9f"  # safe, unique string
+
+try:
+    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
+except Exception:
+    sync_playwright = None
+    PlaywrightTimeout = Exception
+
+def _inject_marker_in_url(url: str, param_name: str = "vulnhunter", marker: str = DEFAULT_MARKER) -> str:
+    # add or replace query param
+    p = urlparse(url)
+    q = dict(parse_qsl(p.query))
+    q[param_name] = marker
+    newq = urlencode(q)
+    return urlunparse((p.scheme, p.netloc, p.path, p.params, newq, p.fragment))
+
+def _page_has_marker(page, marker: str) -> bool:
+    try:
+        # Check DOM for marker (innerHTML of document)
+        found = page.evaluate("marker => document.documentElement.innerHTML.includes(marker)", marker)
+        return bool(found)
+    except Exception as e:
+        LOG.debug("page evaluate error: %s", e)
+        return False
+
+def _submit_forms_and_check(page, marker: str) -> bool:
+    # Heuristic: fill text inputs & submit first button
+    try:
+        forms = page.query_selector_all("form")
+        for idx, form in enumerate(forms):
+            inputs = form.query_selector_all("input[type=text], input:not([type]) , textarea")
+            if not inputs:
+                continue
+            for i in inputs:
+                try:
+                    i.fill(marker)
+                except Exception:
+                    # some inputs are read-only etc.
+                    continue
+            # submit via first submit button or form.evaluate
+            submit = form.query_selector("button[type=submit], input[type=submit]")
+            if submit:
+                try:
+                    submit.click()
+                except Exception:
+                    try:
+                        form.evaluate("f => f.submit()")
+                    except Exception:
+                        pass
+            else:
+                try:
+                    form.evaluate("f => f.submit()")
+                except Exception:
+                    pass
+            # after submit, wait a bit and check DOM
+            try:
+                page.wait_for_timeout(800)  # ms
+            except Exception:
+                pass
+            if _page_has_marker(page, marker):
+                return True
+        return False
+    except Exception as e:
+        LOG.debug("form submission heuristic failed: %s", e)
+        return False
+
+def validate_dom_xss(urls: List[str], marker: str = DEFAULT_MARKER, timeout: int = 8000, headless: bool = True) -> Dict[str, Any]:
+    """
+    Validate a list of URLs using Playwright.
+    Returns dict with list of findings: {"url":..., "method":"param"|"form", "marker":...}
+    """
+    if sync_playwright is None:
+        raise RuntimeError("playwright not installed. pip install playwright and run 'playwright install' per docs.")
+
+    findings = []
+    with sync_playwright() as p:
+        browser = p.chromium.launch(headless=headless)
+        for url in urls:
+            LOG.info("Validating %s", url)
+            page = browser.new_page()
+            page.set_default_timeout(timeout)
+            try:
+                # 1) try marker via query param
+                test_url = _inject_marker_in_url(url, marker=marker)
+                try:
+                    page.goto(test_url, wait_until="load")
+                except PlaywrightTimeout:
+                    LOG.debug("timeout loading %s", test_url)
+                if _page_has_marker(page, marker):
+                    findings.append({"url": url, "method": "param", "marker": marker})
+                    page.close()
+                    continue
+
+                # 2) try submitting forms (fill text inputs)
+                try:
+                    page.goto(url, wait_until="load")
+                except PlaywrightTimeout:
+                    LOG.debug("timeout loading %s", url)
+                if _submit_forms_and_check(page, marker):
+                    findings.append({"url": url, "method": "form", "marker": marker})
+                    page.close()
+                    continue
+            except Exception as e:
+                LOG.debug("validation error for %s: %s", url, e)
+            finally:
+                try:
+                    page.close()
+                except Exception:
+                    pass
+        try:
+            browser.close()
+        except Exception:
+            pass
+    return {"checked": len(urls), "findings": findings}
+
*** End Patch
*** Begin Patch
*** Update File: vulnhunter/scanners/xss_dom.py
@@
 def scan_dom_sinks(start_url: str, max_pages: int = 50) -> Dict[str, Any]:
     # simple: fetch start and a few direct links (non-crawl heavy to keep safe by default)
     urls = [start_url]
@@
     findings = asyncio.run(_scan_urls(urls))
     return {"start": start_url, "checked": len(urls), "findings": findings}
+
*** End Patch
*** Begin Patch
*** Update File: vulnhunter/scanners/__init__.py
*** End Patch
*** Begin Patch
*** Update File: vulnhunter/cli.py
@@
 from .crawl.crawler import crawl_site
 from .scanners.xss_dom import scan_dom_sinks
+from .scanners.xss_dom_playwright import validate_dom_xss
@@
 @cli.command(name="xss-dom")
 @click.option("--url", required=True, help="Start URL (include scheme)")
 @click.option("--max-pages", default=50, show_default=True)
 @click.option("--output", default=None, help="Save JSON results")
 def xss_dom(url, max_pages, output):
     """Scan a small set of pages for risky DOM sinks (static).""" 
     res = scan_dom_sinks(url, max_pages=max_pages)
     j = json.dumps(res, indent=2)
     if output:
         import os
         os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
         with open(output, "w") as fh:
             fh.write(j)
         LOG.info("Saved DOM XSS sink results to %s", output)
     else:
         print(j)
+
+@cli.command(name="xss-validate")
+@click.option("--url", required=True, help="Start URL (include scheme) or comma-separated list")
+@click.option("--marker", default=None, help="Marker string to inject (default: autogenerated)")
+@click.option("--headless/--no-headless", default=True)
+@click.option("--consent", is_flag=True, help="I have permission to test this target (required)")
+@click.option("--output", default=None, help="Save JSON validation results")
+def xss_validate(url, marker, headless, consent, output):
+    """Validate DOM-XSS using a headless browser (Playwright). Requires --consent."""
+    if not consent:
+        LOG.error("DOM-XSS validation is intrusive. You must provide --consent to proceed.")
+        raise SystemExit(1)
+    urls = [u.strip() for u in url.split(",") if u.strip()]
+    from uuid import uuid4
+    safe_marker = marker or f"VULNHUNTER_MARKER_{uuid4().hex[:8]}"
+    try:
+        res = validate_dom_xss(urls, marker=safe_marker, headless=headless)
+    except RuntimeError as e:
+        LOG.error(str(e))
+        raise SystemExit(1)
+    # Integrate with scoring by adding tag to enrichment results (caller must merge)
+    j = json.dumps(res, indent=2)
+    if output:
+        import os
+        os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
+        with open(output, "w") as fh:
+            fh.write(j)
+        LOG.info("Saved DOM XSS validation results to %s", output)
+    else:
+        print(j)
*** End Patch
