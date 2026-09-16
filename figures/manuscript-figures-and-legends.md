# Manuscript Figures and Legends

This file defines the proposed figure package for `MANUSCRIPT.md`.

## Figure 1. Conceptual overview of the frustrated viral-host landscape

**Biological question:** How can common latent viral exposures generate heterogeneous MS trajectories rather than one uniform disease course?

**Panel content:**
- Panel A: interacting viral nodes for EBV, HHV-6A/6B, HSV-1, and CMV
- Panel B: host susceptibility fields including HLA, interferon, Treg/checkpoint, and BBB integrity classes
- Panel C: metastable clinical states labeled prodrome, remission, relapse, progression
- Panel D: perturbations such as viral reactivation, immune stress, treatment, and environmental cofactors

**Interpretation:** Solid arrows should represent evidence-supported relationships. Dashed arrows should represent hypothesis-level couplings or state transitions that require validation. The figure should visually emphasize that the same viral exposures can lead to different outcomes depending on host context and network history.

**Abbreviations:** BBB, blood-brain barrier; CMV, cytomegalovirus; EBV, Epstein-Barr virus; HHV-6, human herpesvirus 6; HSV-1, herpes simplex virus type 1; MS, multiple sclerosis.

## Figure 2. Compartment-resolved map of viruses, immune cells, BBB, and CNS targets

**Biological question:** In which compartments do viral persistence, immune priming, and tissue injury intersect in MS?

**Panel content:**
- peripheral blood and lymphoid tissue
- BBB/endothelium
- CSF
- neurons
- oligodendrocytes
- astrocytes
- microglia

**Interpretation:** Arrows should distinguish trafficking, latency, reactivation, cytokine signaling, and cell injury. Evidence-based interactions should be separated visually from conceptual links. This figure should reinforce that a patient can occupy distinct viral-host states in different compartments simultaneously.

**Abbreviations:** CNS, central nervous system; CSF, cerebrospinal fluid; GFAP, glial fibrillary acidic protein; OPC, oligodendrocyte progenitor cell; PRR, pattern-recognition receptor.

## Figure 3. Host genetics, viral epitope, and pathway integration workflow

**Biological question:** How can host susceptibility data and viral sequence features be integrated into one systems-biology pipeline?

**Panel content:**
- left block: ClinVar and curated host susceptibility variants
- center block: NCBI Virus and ViPR viral strain/protein features
- right block: IEDB epitope features and pathway/network modules
- output block: subgroup-specific viral-host state classification

**Interpretation:** This figure should show data flow from variant interpretation and viral feature extraction toward pathway-level models, mimicry prioritization, and patient-state inference. Solid arrows should denote implemented or standardizable steps; dashed arrows should denote higher-level inferential steps.

**Abbreviations:** IEDB, Immune Epitope Database; JAK, Janus kinase; NF-kB, nuclear factor kappa-light-chain-enhancer of activated B cells; STAT, signal transducer and activator of transcription.

## Figure 4. State-based therapeutic stratification model

**Biological question:** How might inferred viral-host states change therapeutic logic in MS?

**Panel content:**
- antiviral-dominant state
- autoimmune-dominant state
- mixed chronic inflammatory state
- progressive neurodegenerative state
- example biomarker overlays for each state

**Interpretation:** The goal is to show why treatment by biological state may outperform treatment by diagnosis alone. Arrows should indicate preferred strategy direction, not deterministic treatment mandates. This figure should clearly distinguish current clinical practice from hypothesis-guided stratification.

**Abbreviations:** DMT, disease-modifying therapy; MRI, magnetic resonance imaging; NfL, neurofilament light chain.

## Figure 5. Literature-to-dataset-to-model pipeline

**Biological question:** What operational workflow can turn the repository into a manuscript-supported analysis program?

**Panel content:**
- literature curation
- topic-tagged references
- public omics dataset ingestion
- viral and epitope resource integration
- network construction
- figure/table generation

**Interpretation:** This optional figure should show the repository as a staged research pipeline. It is especially useful if the manuscript is submitted as a translational systems-biology review.

**Abbreviations:** GEO, Gene Expression Omnibus.

## Figure 6. Testable hypotheses and validation roadmap

**Biological question:** Which experiments or analyses could falsify or support the frustrated viral-host model?

**Panel content:**
- relapse prediction models
- host-variant and viral-state interaction tests
- lesion-class and compartment analyses
- epitope burden and autoimmune repertoire tests
- subgroup-guided therapeutic evaluation

**Interpretation:** This optional figure should distinguish short-term analytic tests from longer-term mechanistic validation. It should help reviewers see that the manuscript proposes a falsifiable framework rather than an unfalsifiable synthesis.

**Abbreviations:** CSF, cerebrospinal fluid; HLA, human leukocyte antigen; PBMC, peripheral blood mononuclear cell.
