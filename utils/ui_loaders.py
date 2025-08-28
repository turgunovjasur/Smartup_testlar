import time
from selenium.common.exceptions import JavascriptException
from utils.exception import LoaderTimeoutError, JavaScriptError

# ======================================================================================================================

class UILoaders:
    _POLL = 0.1
    _ASYNC_STABLE = 0.5
    _NET_IDLE_CAP = 10.0

    def __init__(self, driver, logger,
                 page_load_timeout=20.0,
                 block_ui_absence_window=0.50,
                 overlay_selectors=None,
                 spinner_selectors=None,
                 screenshot_cb=None):
        self.driver = driver
        self.logger = logger
        self.page_load_timeout = float(page_load_timeout)
        self.block_ui_absence_window = float(block_ui_absence_window)
        self.overlay_selectors = list(overlay_selectors or [
            "div.block-ui-overlay",
            "div.block-ui-message-container",
            ".cs-backdrop.open"
        ])
        self.spinner_selectors = list(spinner_selectors or [
            "div.block-ui-message-container img[src*='loading']",
            "img[src$='loading.svg']",
            "img[src*='loading']",
        ])
        self.screenshot_cb = screenshot_cb

    # ==================================================================================================================

    def wait_for_all_loaders(self, page_load_timeout=None, block_ui_absence_window=None):
        if page_load_timeout is not None:
            self.page_load_timeout = float(page_load_timeout)
        if block_ui_absence_window is not None:
            self.block_ui_absence_window = float(block_ui_absence_window)

        t0 = time.time()
        deadline = t0 + self.page_load_timeout

        self._wait_async_idle(min(deadline, time.time() + self._NET_IDLE_CAP), t0)
        self._wait_block_ui_absent(deadline, t0)
        self._wait_spinner_clear(deadline, t0)
        return True

    # ==================================================================================================================
    # --- Steps ---
    def _wait_async_idle(self, net_deadline, t0):
        js_async_counts = r"""
            (function(){
              try {
                if (!window.__xhrHooked) {
                  window.__xhrHooked = true;
                  window.__openXhrs = 0;
                  const _open = XMLHttpRequest.prototype.open;
                  const _send = XMLHttpRequest.prototype.send;
                  XMLHttpRequest.prototype.open = function(){
                    this.addEventListener('loadend', function(){
                      window.__openXhrs = Math.max(0, window.__openXhrs - 1);
                    });
                    return _open.apply(this, arguments);
                  };
                  XMLHttpRequest.prototype.send = function(){
                    window.__openXhrs += 1;
                    return _send.apply(this, arguments);
                  };
                }
              } catch(e){}

              try {
                if (!window.__fetchHooked && window.fetch) {
                  window.__fetchHooked = true;
                  window.__pendingFetches = 0;
                  const _fetch = window.fetch;
                  window.fetch = function(){
                    window.__pendingFetches += 1;
                    const p = _fetch.apply(this, arguments);
                    if (p && p.finally) {
                      return p.finally(function(){
                        window.__pendingFetches = Math.max(0, window.__pendingFetches - 1);
                      });
                    }
                    if (p && p.then) {
                      p.then(function(){
                        window.__pendingFetches = Math.max(0, window.__pendingFetches - 1);
                      }, function(){
                        window.__pendingFetches = Math.max(0, window.__pendingFetches - 1);
                      });
                    } else {
                      window.__pendingFetches = Math.max(0, window.__pendingFetches - 1);
                    }
                    return p;
                  };
                }
              } catch(e){}

              const c = {jq:0, ng:0, xhr:0, fetch:0};
              try { c.jq = (window.jQuery && typeof window.jQuery.active === 'number') ? window.jQuery.active : 0; } catch(e){}
              try {
                if (window.angular && document.body && window.angular.element(document.body).injector) {
                  const inj = window.angular.element(document.body).injector();
                  if (inj && inj.get) {
                    const $http = inj.get('$http');
                    c.ng = ($http && Array.isArray($http.pendingRequests)) ? $http.pendingRequests.length : 0;
                  }
                }
              } catch(e){}
              try { c.xhr = window.__openXhrs || 0; } catch(e){}
              try { c.fetch = window.__pendingFetches || 0; } catch(e){}
              return c;
            })();
        """
        stable_since = None
        while time.time() < net_deadline:
            try:
                c = self.driver.execute_script(js_async_counts) or {}
            except JavascriptException as e:
                # Bu joyda testni aniq sabab bilan to'xtatish foydali
                raise JavaScriptError("Asinxron tekshiruvda JavaScript xatosi", original_error=e)
            active = int(c.get("jq", 0)) + int(c.get("ng", 0)) + int(c.get("xhr", 0)) + int(c.get("fetch", 0))
            if active == 0:
                if stable_since is None:
                    stable_since = time.time()
                if time.time() - stable_since >= self._ASYNC_STABLE:
                    self.logger.debug(f"Asinxron operatsiyalar yakunlandi ({time.time()-t0:.2f}s)")
                    return
            else:
                stable_since = None
                self.logger.debug(f"Asinxron operatsiyalar davom etmoqda... ({time.time()-t0:.2f}s)")
            time.sleep(self._POLL)
        # davom etamiz

    # ==================================================================================================================

    def _wait_block_ui_absent(self, deadline, t0):
        start = time.time()
        stable_since = None
        while time.time() < deadline:
            info = self._query_blockers()
            if info.get("overlayBlocks"):
                stable_since = None
                self.logger.debug(f"Block UI ko'rinmoqda, kutilyapti... ({time.time()-start:.2f}s)")
            else:
                if stable_since is None:
                    stable_since = time.time()
                if time.time() - stable_since >= self.block_ui_absence_window:
                    if (time.time() - start) > 0.01:
                        self.logger.debug(f"Block UI yo‘qoldi va barqarorlashdi ({time.time()-start:.2f}s).")
                    else:
                        self.logger.debug(f"Block UI topilmadi (barqaror tasdiq {self.block_ui_absence_window:.1f}s). ({time.time()-start:.2f}s)")
                    return
            time.sleep(self._POLL)
        self._fail("Block UI", deadline, t0, locator="block-ui-any")

    # ==================================================================================================================

    def _wait_spinner_clear(self, deadline, t0):
        start = time.time()
        while time.time() < deadline:
            info = self._query_blockers()
            if not info.get("spinnerBlocks", False) and not info.get("overlayBlocks", False):
                if int(info.get("spinnerCount", 0)) > 0:
                    self.logger.debug("Spinner bloklamayapti — bypass.")
                else:
                    self.logger.debug(f"Spinner/overlay yo‘qoldi ({time.time()-start:.2f}s)")
                return
            time.sleep(self._POLL)
        self._fail("Spinner/overlay", deadline, t0)

    # ==================================================================================================================
    # --- Helpers ---
    def _fail(self, what, deadline, t0, locator=None):
        msg = f"{what} {self.page_load_timeout:.0f}s ichida yo‘qolmadi! (Jami: {time.time()-t0:.2f}s)"
        self.logger.error(msg)
        try:
            if self.screenshot_cb:
                self.screenshot_cb("timeout_error")
        except Exception:
            pass
        raise LoaderTimeoutError(msg, locator=locator)

    # ==================================================================================================================

    def _query_blockers(self):
        js_blockers = r"""
            return (function(overSels, spinSels){
              function isXPath(sel){ return /^\/\//.test(sel) || /^xpath\s*=/i.test(sel); }
              function norm(sel){ return sel.replace(/^xpath\s*=/i, ''); }
              function nodes(sels){
                const out=[];
                (sels||[]).forEach(sel=>{
                  if(!sel) return;
                  try{
                    if(isXPath(sel)){
                      const it = document.evaluate(norm(sel), document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                      for(let i=0;i<it.snapshotLength;i++){ out.push(it.snapshotItem(i)); }
                    } else {
                      document.querySelectorAll(sel).forEach(el=>out.push(el));
                    }
                  }catch(e){}
                });
                return out;
              }
              function visible(el){
                if(!el) return false;
                const cs=getComputedStyle(el);
                if(cs.display==='none'||cs.visibility==='hidden'||parseFloat(cs.opacity||'1')<=0.01) return false;
                const r=el.getBoundingClientRect();
                return (r.width>2 && r.height>2);
              }
              function blocks(el){
                if(!visible(el)) return false;
                const cs=getComputedStyle(el);
                if(cs.pointerEvents==='none') return false;
                const r=el.getBoundingClientRect();
                const vw=Math.max(document.documentElement.clientWidth,window.innerWidth||0);
                const vh=Math.max(document.documentElement.clientHeight,window.innerHeight||0);
                const cx=vw/2, cy=vh/2;
                const coversCenter=(r.left<=cx && r.right>=cx && r.top<=cy && r.bottom>=cy);
                const area=r.width*r.height, coverRatio=area/Math.max(1,vw*vh);
                const z=parseInt(cs.zIndex)||0;
                return coversCenter || coverRatio>0.25 || z>=1000;
              }

              const overs = nodes(overSels).filter(visible);
              const spins = nodes(spinSels).filter(visible);

              let overlayBlocks=false;
              for(let i=0;i<overs.length;i++){ if(blocks(overs[i])){ overlayBlocks=true; break; } }

              let spinnerBlocks=false;
              for(let i=0;i<spins.length;i++){ if(blocks(spins[i])){ spinnerBlocks=true; break; } }

              const bodyHas = !!(document.body && document.body.classList.contains('block-ui-active'));

              return {
                overlayBlocks: overlayBlocks || bodyHas,
                spinnerBlocks: spinnerBlocks,
                overlayCount: overs.length,
                spinnerCount: spins.length
              };
            })(arguments[0], arguments[1]);
        """
        try:
            return self.driver.execute_script(js_blockers, list(self.overlay_selectors), list(self.spinner_selectors)) or {}
        except JavascriptException as e:
            raise JavaScriptError("Block UI/spinner tekshirishda JavaScript xatosi", original_error=e)

    # ==================================================================================================================
