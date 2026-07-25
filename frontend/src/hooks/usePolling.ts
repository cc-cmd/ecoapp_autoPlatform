import { useEffect, useRef } from 'react';

/**
 * Generic polling hook that invokes a callback at a given interval.
 * Automatically cleans up on unmount or when disabled.
 *
 * @param callback - Function to call on each tick.
 * @param intervalMs - Polling interval in milliseconds.
 * @param enabled - Whether polling is active (default true).
 */
export function usePolling(
  callback: () => void,
  intervalMs: number,
  enabled: boolean = true,
): void {
  const savedCallback = useRef(callback);

  // Update ref when callback changes
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (!enabled) return;

    const tick = () => {
      savedCallback.current();
    };

    const id = setInterval(tick, intervalMs);
    return () => clearInterval(id);
  }, [intervalMs, enabled]);
}
