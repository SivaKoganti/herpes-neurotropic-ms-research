from app.models.schemas import VariantInfoResponse

CLINVAR_VARIANTS = {
    ("TLR2", "rs5743708"): VariantInfoResponse(gene="TLR2", variant="rs5743708", pathogenicity="likely-pathogenic", effect_size=1.25),
    ("TLR3", "rs3775291"): VariantInfoResponse(gene="TLR3", variant="rs3775291", pathogenicity="VUS", effect_size=1.10),
    ("TLR9", "rs5743836"): VariantInfoResponse(gene="TLR9", variant="rs5743836", pathogenicity="likely-benign", effect_size=0.95),
    ("IL6", "rs1800795"): VariantInfoResponse(gene="IL6", variant="rs1800795", pathogenicity="pathogenic", effect_size=1.30),
    ("IL23A", "rs11171806"): VariantInfoResponse(gene="IL23A", variant="rs11171806", pathogenicity="VUS", effect_size=1.08),
    ("STAT3", "rs744166"): VariantInfoResponse(gene="STAT3", variant="rs744166", pathogenicity="likely-pathogenic", effect_size=1.22),
}


def find_variant(gene: str, variant: str) -> VariantInfoResponse | None:
    return CLINVAR_VARIANTS.get((gene.upper(), variant))


def search_variants(gene: str | None = None) -> list[VariantInfoResponse]:
    values = list(CLINVAR_VARIANTS.values())
    if not gene:
        return values
    gene_upper = gene.upper()
    return [entry for entry in values if entry.gene.upper() == gene_upper]
