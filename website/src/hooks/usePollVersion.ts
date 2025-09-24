import { useEffect, useRef } from "react";
import { fetchVersion } from "../lib/api";

export function usePollVersion(onChange: () => void, intervalMs = 10000) {
  const last = useRef<string | null>(null);

  useEffect(() => {
    let timer: any;
    async function tick() {
      try {
        const v = await fetchVersion();
        if (last.current && v.version !== last.current) onChange();
        last.current = v.version;
      } catch {}
      timer = setTimeout(tick, intervalMs);
    }
    tick();
    return () => clearTimeout(timer);
  }, [onChange, intervalMs]);
}
