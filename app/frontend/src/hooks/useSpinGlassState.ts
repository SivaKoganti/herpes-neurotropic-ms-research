import { useState } from "react";
import { apiUrl } from "../api";

export function useSpinGlassState() {
  const [state, setState] = useState<Record<string, string | number> | null>(null);

  const fetchState = async (viralProfile: unknown) => {
    const res = await fetch(apiUrl("/api/coinfection-state"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(viralProfile),
    });
    setState((await res.json()) as Record<string, string | number>);
  };

  return { state, fetchState };
}
