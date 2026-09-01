# Evidence-bounded synthesis

## Corpus accounting and query dependence

- Unique OpenAlex corpus: **164 records**.
- Every record shown has a DOI-bearing identifier, but DOI presence does not imply that the abstract directly supports the mechanism.
- The retrieval is **not a systematic review**: it is a frozen, machine-retrieved corpus with broad topical leakage.
- Query-family dependence is strong:
  - The conductivity-degradation query retrieves many general battery-aging, polymer-electrolyte, supercapacitor, fuel-cell, aqueous-battery, and liquid-electrolyte papers.
  - The interfacial-resistance query is the most directly relevant to solid-state battery cycling.
  - The dendrite/space-charge/mechanics query emphasizes lithium penetration, stress, current focusing, and interphase design.
  - The operando-EIS query contains useful diagnostics, but also many unrelated operando catalysis, zinc, aqueous, and conventional Li-ion records.
- Exact family cardinalities and pairwise overlap counts cannot be independently recomputed from the metadata excerpt without an explicit complete family-membership table. The supplied **unique count is 164**; repeated DOI records across query families should be counted once.

Citation counts are reported only as retrieval metadata, not as evidence of correctness.

## Mechanism families

### 1. Interfacial contact loss and mechanically generated transport constriction

Repeated cycling changes solid–solid contact through electrode breathing, lithium removal, pore formation, cracking, roughness evolution, and stack-pressure dependence. The consequence is loss of active area and increased diffusional or charge-transfer resistance.

- Yu et al., DOI [10.1038/s41467-017-01187-y](https://doi.org/10.1038/s41467-017-01187-y): the abstract directly supports a dramatic post-cycling drop in interfacial conductivity attributed to **loss of interfacial contact and increased diffusional barriers** in an argyrodite/sulfide electrode system.
- Zhang et al., DOI [10.1021/acsami.8b05132](https://doi.org/10.1021/acsami.8b05132): supports electrochemically driven mechanical failure at the LiCoO₂/Li₁₀GeP₂S₁₂ cathode interface, increased impedance, and capacity fade.
- Kalnaus et al., DOI [10.1126/science.abg5998](https://doi.org/10.1126/science.abg5998): review-level support that stress, strain, contact mechanics, and stress relief are central failure variables.
- Tu et al., DOI [10.1016/j.xcrp.2020.100106](https://doi.org/10.1016/j.xcrp.2020.100106): models contact loss and fracture as competing outcomes controlled by pressure, roughness, kinetics, and electrolyte conductivity.
- Oh et al., DOI [10.1002/aenm.202101228](https://doi.org/10.1002/aenm.202101228): in sodium cells, supports desodiation-induced contact loss and pore formation, mitigated by a Na–Sn alloy.

Boundary condition: strongest for composite cathodes, pressed pellets, metal-anode interfaces, and systems with substantial volume change. It does not establish that contact loss is the dominant mechanism in every solid electrolyte chemistry.

### 2. Interphase growth or transformation causing ionic/electronic transport changes

Electrolyte decomposition can form spatially heterogeneous interphases. Growth, porosity, composition, or phase redistribution may increase ionic resistance, electronic leakage, or both.

- Wood et al., DOI [10.1038/s41467-018-04762-z](https://doi.org/10.1038/s41467-018-04762-z): operando XPS/Auger supports decomposition of Li₂S–P₂S₅ at Li into Li₂S/Li₃P, with oxygen-related Li₃PO₄ and Li₂O; phase nonuniformity and differing ionic conductivities affect interphase performance.
- Zhang et al., DOI [10.1002/adfm.201909392](https://doi.org/10.1002/adfm.201909392): supports high-voltage PEO decomposition, continuing CEI growth, oxygen release from delithiated LiCoO₂, and cathode-surface destruction.
- Wang et al., DOI [10.1021/jacs.7b09531](https://doi.org/10.1021/jacs.7b09531): supports the importance of interphase ionic/electronic conductivities and dynamic thickness, while linking interphase properties to dendrite growth.
- Davis et al., DOI [10.1149/1945-7111/ac163d](https://doi.org/10.1149/1945-7111/ac163d): contrasts an electronically insulating Li₆PS₅Cl interphase with an electronically conducting interphase in Li₁₀GeP₂S₁₂ and relates this to plating onset and electrolyte decomposition.
- Wenzel et al., DOI [10.1016/j.ssi.2015.06.001](https://doi.org/10.1016/j.ssi.2015.06.001): title indicates an in-situ photoelectron study of interphase formation, but the supplied abstract is empty; it is a lead, not direct abstract evidence.

Boundary condition: composition and function are chemistry-specific. An interphase can initially reduce parasitic reactions yet later become resistive, porous, electronically conductive, or mechanically unstable.

### 3. Lithium or sodium metal penetration, dendrites, and inactive metal

Current focusing, electronic leakage, defects, grain boundaries, interphase properties, and electrochemomechanical stresses can produce internal metal growth. This can consume active electrolyte/electrode area, create inactive metal, raise polarization, or cause short circuit.

- Han et al., DOI [10.1038/s41560-018-0312-z](https://doi.org/10.1038/s41560-018-0312-z): title supports high electronic conductivity as a proposed origin of lithium dendrites, but the abstract is empty.
- Ning et al., DOI [10.1038/s41563-021-00967-8](https://doi.org/10.1038/s41563-021-00967-8): title supports visualization of plating-induced cracking, but the abstract is empty.
- Swamy et al., DOI [10.1149/2.1391814jes](https://doi.org/10.1149/2.1391814jes): directly supports lithium-filled crack initiation near current-collector edges due to enhanced local current density and electrochemomechanical stress.
- Liang et al., DOI [10.1038/s41467-023-35920-7](https://doi.org/10.1038/s41467-023-35920-7): operando NMR supports electronically disconnected lithium in the electrolyte interior and ionically disconnected lithium near the negative-electrode surface.
- Huo et al., DOI [10.1038/s41467-020-20463-y](https://doi.org/10.1038/s41467-020-20463-y): supports high electronic conductivity and uneven fields as dendrite-promoting factors; the shield is reported to preserve interface integrity.
- Barai et al., DOI [10.1149/1945-7111/ab9b08](https://doi.org/10.1149/1945-7111/ab9b08): modeling supports grain-boundary current focusing and eventual dendrite growth, even at low charge rates given sufficient time.

Boundary condition: primarily relevant to metal-anode cells and plating conditions. It cannot explain cathode-side impedance growth in cells using indium, graphite, or other nonmetal anodes without an additional mechanism.

### 4. Bulk electrolyte, grain-boundary, and polymer transport degradation

The apparent “conductivity loss” may be bulk ionic transport loss, grain-boundary resistance, polymer segmental-motion changes, temperature dependence, or transport-pathway disruption rather than a new chemical phase.

- Zhang et al., DOI [10.1039/c8ee01053f](https://doi.org/10.1039/c8ee01053f): review abstract supports conductivity, chemical/electrochemical stability, and solid-state-battery relevance, but not a specific cycling-loss mechanism.
- Agrawal and Pandey, DOI [10.1088/0022-3727/41/22/223001](https://doi.org/10.1088/0022-3727/41/22/223001): supports low room-temperature conductivity of dry polymer electrolytes and the role of mechanical stability and interfacial activity.
- Zhang et al., DOI [10.26599/nre.2023.9120050](https://doi.org/10.26599/nre.2023.9120050): supports polymer ion hopping, segmental motion, carrier concentration, mobility, and fast-ion pathways as determinants of conductivity.
- Yang et al., DOI [10.1021/acsenergylett.0c01432](https://doi.org/10.1021/acsenergylett.0c01432): supports separate bulk and grain-boundary conductivity improvements in NASICON sodium electrolytes, but not cycling-induced loss.
- Wang et al., DOI [10.1038/s41467-023-38037-z](https://doi.org/10.1038/s41467-023-38037-z): supports interfacial superionic conduction in halide nanocomposites.

Boundary condition: must be separated experimentally from contact and interphase resistance. A total-cell impedance increase alone cannot identify this family.

### 5. Cathode-side chemical attack and active-material/interface degradation

At high voltage, reactive cathode surfaces can oxidize or chemically attack the solid electrolyte or polymer, producing a growing CEI and destroying active-material surface transport.

- Zhang et al., DOI [10.1021/acsami.8b05132](https://doi.org/10.1021/acsami.8b05132): supports cathode/solid-electrolyte mechanical and interfacial degradation in LiCoO₂/Li₁₀GeP₂S₁₂.
- Qiu et al., DOI [10.1002/adfm.201909392](https://doi.org/10.1002/adfm.201909392): directly supports high-voltage PEO decomposition accelerated by strongly oxidizing delithiated LiCoO₂ and continuing CEI growth.
- Rinkel et al., DOI [10.1021/jacs.0c06363](https://doi.org/10.1021/jacs.0c06363): in a LiCoO₂/glass-ceramic-separator configuration, supports chemical oxidation associated with reactive oxygen, with an onset near 4.7 V versus Li/Li⁺. This is not a generic proof for all solid-state chemistries.

Boundary condition: voltage, cathode composition, state of charge, surface coating, and electrolyte chemistry are decisive.

## Typed mechanism table

| Mechanism | Causal pathway | Predicted observation | Evidence records | Confounder | Falsifier |
|---|---|---|---|---|---|
| Contact loss / fracture | Cycling strain, pore formation, roughness, or pressure change reduces real contact area | Rising interfacial impedance; microscopy/NMR shows gaps or cracks; pressure or compliant interlayer reverses part of loss | [Yu 2017](https://doi.org/10.1038/s41467-017-01187-y); [Zhang 2018](https://doi.org/10.1021/acsami.8b05132); [Tu 2020](https://doi.org/10.1016/j.xcrp.2020.100106) | Chemical interphase growth can produce the same impedance rise | Stable physical contact under cycling while resistance rises and chemistry changes |
| Resistive interphase growth | Electrolyte/electrode decomposition forms thicker, poorly conducting or heterogeneous phases | Chemical-species evolution correlates with impedance; resistance remains after pressure relaxation | [Wood 2018](https://doi.org/10.1038/s41467-018-04762-z); [Qiu 2020](https://doi.org/10.1002/adfm.201909392) | Sampling artifacts; cathode and anode contributions overlap | No interphase evolution despite reproducible resistance growth |
| Electronically conductive interphase | Partial reduction creates electronic pathways and sustained electrolyte decomposition | Continuous electrolyte consumption, altered plating onset, electronic leakage, low Faradaic efficiency | [Davis 2021](https://doi.org/10.1149/1945-7111/ac163d); [Wang 2017](https://doi.org/10.1021/jacs.7b09531) | Apparent leakage may arise from lithium filaments | Direct electronic isolation with no change in decomposition or plating behavior |
| Dendrite / metal penetration | Current focusing, defects, grain boundaries, electronic leakage, and stress drive internal metal growth | Local shorting, filament imaging, inactive-Li NMR signal, edge-dependent failure | [Swamy 2018](https://doi.org/10.1149/2.1391814jes); [Liang 2023](https://doi.org/10.1038/s41467-023-35920-7); [Barai 2020](https://doi.org/10.1149/1945-7111/ab9b08) | High current density and stack pressure can independently cause failure | No metal growth or inactive metal under conditions where conductivity still falls |
| Bulk/grain-boundary transport loss | Structural, compositional, thermal, or polymer-mobility changes lower ionic conductivity | Symmetric blocking-electrode measurement shows reduced bulk or grain-boundary conductivity, independent of interfaces | [Zhang 2018](https://doi.org/10.1039/c8ee01053f); [Zhang 2023](https://doi.org/10.26599/nre.2023.9120050) | Contact resistance is easily misassigned to bulk resistance | Four-terminal or blocking-electrode measurement shows unchanged bulk transport |
| Cathode chemical attack | High-voltage cathode surface reacts with electrolyte; CEI thickens and active surface degrades | Voltage-dependent gas/chemical signatures, cathode-side impedance growth, surface reconstruction | [Qiu 2020](https://doi.org/10.1002/adfm.201909392); [Rinkel 2020](https://doi.org/10.1021/jacs.0c06363) | Mechanical cathode cracking can produce similar impedance | Stable cathode chemistry and CEI while degradation persists only at the anode |

## Contradictions and unresolved discriminators

1. **Insulating versus electronically conducting interphases.** A conventional intuition is that electronic insulation is protective. The supplied abstracts include a contrary result: [Wang et al. 2017](https://doi.org/10.1021/jacs.7b09531) argues that a chemically stable, electronically insulating interphase can promote dendrites by reducing lithium consumption and increasing tip curvature, whereas [Davis et al. 2021](https://doi.org/10.1149/1945-7111/ac163d) reports different plating behavior for insulating and conducting interphases. These are not necessarily incompatible: they may concern different chemistries, geometries, and anode-free versus lithium-reservoir cells.

2. **Mechanical stability is not equivalent to dendrite suppression.** High modulus, interfacial energy, ionic conductivity, and electronic insulation can have competing effects. [Tu et al. 2020](https://doi.org/10.1016/j.xcrp.2020.100106) also predicts a pressure window in which both contact loss and fracture are avoided.

3. **Resistance is not a mechanism.** EIS can separate approximate time constants, but the supplied EIS reviews emphasize interpretation and validation limits: [Meddings et al. 2020](https://doi.org/10.1016/j.jpowsour.2020.228742), [Gaberšček 2021](https://doi.org/10.1038/s41467-021-26894-5). A growing semicircle cannot by itself distinguish interphase growth, contact loss, bulk transport loss, or charge-transfer kinetics.

4. **Regime mismatch is substantial.** Some records concern liquid electrolytes, conventional Li-ion cells, sodium or zinc aqueous cells, supercapacitors, catalysis, or fuel cells. They may provide methodological or conceptual leads, but they are not direct evidence for cycling degradation in inorganic solid-electrolyte batteries.

## Exactly three discriminating experiments

### Experiment 1 — Operando impedance with independent bulk/interface separation

**Design:** Cycle matched solid-state cells while measuring EIS at fixed states of charge, with blocking-electrode or symmetric-cell controls and temperature normalization. Fit bulk electrolyte, grain-boundary, interfacial, and charge-transfer contributions using validated equivalent/physics-based models.

**Competing outcomes:**

- Bulk/grain-boundary mechanism: bulk or grain-boundary resistance rises in blocking controls.
- Contact/interphase mechanism: bulk remains stable while only interface-related components rise.
- Cathode-side chemical attack: cathode-containing half-cell shows the growth; anode-only control does not.
- Dendrite mechanism: intermittent low-frequency anomalies, electronic leakage, or abrupt shorting accompany the impedance evolution.

**Relevant records:** [Yu 2017](https://doi.org/10.1038/s41467-017-01187-y), [Meddings 2020](https://doi.org/10.1016/j.jpowsour.2020.228742), [Gaberšček 2021](https://doi.org/10.1038/s41467-021-26894-5).

### Experiment 2 — Operando or cryogenic multimodal imaging plus Li NMR

**Design:** Cycle cells under controlled current density, stack pressure, and collector geometry while combining imaging of cracks/filaments with operando NMR quantification of active, ionically disconnected, and electronically disconnected lithium.

**Competing outcomes:**

- Dendrite/metal-penetration mechanism: filament growth, crack initiation, inactive lithium, or edge-localized failure precedes resistance loss or shorting.
- Contact-loss mechanism: gaps, pores, or fracture occur without substantial inactive-metal growth; pressure/compliant-interface changes alter the result.
- Interphase mechanism: resistance and chemical evolution precede morphology changes.
- Cathode degradation: damage is localized to the cathode/solid-electrolyte interface.

**Relevant records:** [Swamy 2018](https://doi.org/10.1149/2.1391814jes), [Liang 2023](https://doi.org/10.1038/s41467-023-35920-7), [Ning 2021](https://doi.org/10.1038/s41563-021-00967-8).

### Experiment 3 — Spatially resolved operando interphase chemistry correlated with resistance

**Design:** Use operando XPS/XAS or a validated post-cycling cryogenic chemical analysis at the anode and cathode separately, synchronized with impedance and gas/pressure measurements. Compare an electronically insulating interphase, an electronically conducting interphase, and a chemically protected control.

**Competing outcomes:**

- Resistive interphase growth: increasing interphase thickness or a new low-ionic-conductivity phase tracks resistance growth.
- Conductive-interphase mechanism: electronic leakage and ongoing electrolyte decomposition track delayed plating or low Faradaic efficiency.
- Cathode chemical attack: high-voltage CEI/oxygen-related products and cathode-surface changes track degradation.
- Mechanical/contact mechanism: chemistry remains comparatively unchanged while impedance changes and physical contact degrades.

**Relevant records:** [Wood 2018](https://doi.org/10.1038/s41467-018-04762-z), [Davis 2021](https://doi.org/10.1149/1945-7111/ac163d), [Qiu 2020](https://doi.org/10.1002/adfm.201909392), [Rinkel 2020](https://doi.org/10.1021/jacs.0c06363).

## Priority human-review set: 12 papers

1. [Yu et al. 2017 — interfacial Li transport after cycling](https://doi.org/10.1038/s41467-017-01187-y)
2. [Zhang et al. 2018 — Li₁₀GeP₂S₁₂/LiCoO₂ degradation](https://doi.org/10.1021/acsami.8b05132)
3. [Wood et al. 2018 — operando sulfide interphase evolution](https://doi.org/10.1038/s41467-018-04762-z)
4. [Tu et al. 2020 — deposition and mechanical stability](https://doi.org/10.1016/j.xcrp.2020.100106)
5. [Swamy et al. 2018 — lithium penetration in garnet](https://doi.org/10.1149/2.1391814jes)
6. [Liang et al. 2023 — inactive lithium by operando NMR](https://doi.org/10.1038/s41467-023-35920-7)
7. [Davis et al. 2021 — interphase electronic conductivity and plating](https://doi.org/10.1149/1945-7111/ac163d)
8. [Qiu et al. 2020 — PEO/high-voltage cathode failure](https://doi.org/10.1002/adfm.201909392)
9. [Kalnaus et al. 2023 — mechanics review](https://doi.org/10.1126/science.abg5998)
10. [Hatzell et al. 2020 — solid-state Li-metal challenges](https://doi.org/10.1021/acsenergylett.9b02668)
11. [Barai et al. 2020 — LLZO inhomogeneity and dendrites](https://doi.org/10.1149/1945-7111/ab9b08)
12. [Meddings et al. 2020 — EIS interpretation and validation](https://doi.org/10.1016/j.jpowsour.2020.228742)

## What this corpus cannot establish

- It cannot identify one universal dominant mechanism across sulfide, oxide, halide, polymer, composite, lithium, sodium, anode-free, and full-cell systems.
- It cannot quantify the relative contribution of bulk transport, grain boundaries, contact loss, interphase growth, cathode attack, and dendrites for a particular cell.
- It cannot establish causality from titles, citation counts, or an impedance increase alone.
- It cannot validate records with empty abstracts beyond their titles and metadata.
- It cannot determine whether reported improvements generalize to practical stack pressure, areal loading, current density, temperature, electrode thickness, or full-cell conditions.
- It cannot support a systematic-review conclusion, publication-bias estimate, or exhaustive coverage claim.