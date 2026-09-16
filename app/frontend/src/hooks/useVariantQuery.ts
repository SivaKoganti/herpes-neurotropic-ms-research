import { useState } from "react";
import { apiUrl } from "../api";

export function useVariantQuery() {
  const [variants, setVariants] = useState<Array<Record<string, string | number>>>([]);

  const search = async (gene?: string) => {
    const params = gene ? `?gene=${encodeURIComponent(gene)}` : "";
    const res = await fetch(apiUrl(`/api/variant-info${params}`));
    setVariants((await res.json()) as Array<Record<string, string | number>>);
  };

  return { variants, search };
}
