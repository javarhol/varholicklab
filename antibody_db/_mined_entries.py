#!/usr/bin/env python3
"""Antibodies extracted (curated, reviewed) from Acomys Library full text during
the mining pass. Consumed by _merge_mined.py, which dedupes against the existing
database and appends. Primary antibodies only (secondaries/conjugated anti-IgG
reagents are not informative for cross-reactivity and are excluded).

Each SOURCES entry documents a newly mined paper; each ENTRIES entry is one
antibody product. `result` defaults to "works" (the paper used it successfully in
Acomys tissue) unless the paper explicitly reports a failure.
"""

DATE = "2026-07-11"
CONTRIB = "Acomys Library"


def E(target, category, application, source, doi, catalog, vendor, host, clon,
      rrid="", dilution="", tissue="", notes="", result="works"):
    """Compact antibody-entry constructor (keeps ENTRIES readable)."""
    return dict(target=target, category=category, application=application, result=result,
                source_publication=source, doi=doi, catalog_number=catalog, vendor=vendor,
                host_species=host, clonality=clon, rrid=rrid, dilution=dilution,
                tissue_tested=tissue, notes=notes)

# --- newly mined source publications --------------------------------------
SOURCES = [
    {"short_citation": "Nogueira-Rodrigues et al. 2022",
     "full_reference": "Nogueira-Rodrigues J et al. Rewired glycosylation activity promotes scarless regeneration and functional recovery in spiny mice after complete spinal cord transection. Dev Cell. 2022;57(4):440-450.",
     "doi": "10.1016/j.devcel.2021.12.008", "pmid": "", "pmc_id": "",
     "tissue_focus": "Spinal cord (regeneration)", "antibody_count": "13"},
    {"short_citation": "Brewer et al. 2021",
     "full_reference": "Brewer CM et al. Adaptations in Hippo-Yap signaling and myofibroblast fate underlie scar-free ear appendage wound healing in spiny mice. Dev Cell. 2021;56(19):2722-2740.",
     "doi": "10.1016/j.devcel.2021.09.008", "pmid": "", "pmc_id": "",
     "tissue_focus": "Ear (wound healing), dermal fibroblasts", "antibody_count": "24"},
    {"short_citation": "Simkin et al. 2017",
     "full_reference": "Simkin J et al. Macrophages are necessary for epimorphic regeneration in African spiny mice. eLife. 2017;6:e24623.",
     "doi": "10.7554/elife.24623", "pmid": "", "pmc_id": "",
     "tissue_focus": "Ear (macrophages/immune)", "antibody_count": "10"},
    {"short_citation": "Okamura et al. 2021",
     "full_reference": "Okamura DM et al. Spiny mice activate unique transcriptional programs after severe kidney injury regenerating organ function without fibrosis. iScience. 2021;24(11):103269.",
     "doi": "10.1016/j.isci.2021.103269", "pmid": "", "pmc_id": "",
     "tissue_focus": "Kidney (regeneration)", "antibody_count": "6"},
    {"short_citation": "Gawriluk et al. 2020",
     "full_reference": "Gawriluk TR et al. Mammalian musculoskeletal regeneration is associated with reduced inflammatory cytokines and an influx of T cells. bioRxiv 723783 (2019).",
     "doi": "10.1101/723783", "pmid": "", "pmc_id": "",
     "tissue_focus": "Ear/musculoskeletal (T cells, inflammation)", "antibody_count": "3"},
    {"short_citation": "Ko et al. 2026",
     "full_reference": "Ko D et al. A novel fracture lattice in spiny mouse skin facilitates tissue autotomy and regeneration. bioRxiv (2026).",
     "doi": "10.64898/2026.03.23.713756", "pmid": "", "pmc_id": "",
     "tissue_focus": "Skin (autotomy/regeneration)", "antibody_count": "13"},
    {"short_citation": "Chung et al. 2026",
     "full_reference": "Chung JH et al. AAV tools enable functional modulation and readout of central and peripheral nervous systems in spiny mice. bioRxiv (2026).",
     "doi": "10.64898/2026.05.08.723863", "pmid": "", "pmc_id": "",
     "tissue_focus": "Brain, colon (nervous system)", "antibody_count": "4"},
    {"short_citation": "Oviedo Rivadeneira et al. 2025",
     "full_reference": "Oviedo Rivadeneira E, Allen RS, Adam M, Seifert AW. Specific cell states underlie complex tissue regeneration in spiny mice. bioRxiv (2025).",
     "doi": "10.1101/2025.02.10.637521", "pmid": "", "pmc_id": "",
     "tissue_focus": "Ear (regeneration, cell states)", "antibody_count": "2"},
    {"short_citation": "Gaire et al. 2022",
     "full_reference": "Gaire J, Dill MN, Supper VM, Simmons CS. Attenuated foreign body response to subcutaneous implant in regenerative spiny mice (Acomys). bioRxiv (2022).",
     "doi": "10.1101/2022.08.12.503776", "pmid": "", "pmc_id": "",
     "tissue_focus": "Skin (subcutaneous implant / foreign body response)", "antibody_count": "3"},
    {"short_citation": "Harn et al. 2021",
     "full_reference": "Harn HI-C et al. Symmetry breaking of tissue mechanics in wound induced hair follicle regeneration of laboratory and spiny mice. Nat Commun. 2021;12:2595.",
     "doi": "10.1038/s41467-021-22822-9", "pmid": "", "pmc_id": "",
     "tissue_focus": "Skin (wound-induced hair follicle regeneration)", "antibody_count": "8"},
    {"short_citation": "Saxena et al. 2019",
     "full_reference": "Saxena S, Vekaria HJ, Sullivan PG, Seifert AW. Connective tissue fibroblasts from highly regenerative mammals are refractory to ROS-induced cellular senescence. Nat Commun. 2019;10:4400.",
     "doi": "10.1038/s41467-019-12398-w", "pmid": "", "pmc_id": "",
     "tissue_focus": "Fibroblasts (senescence)", "antibody_count": "5"},
    {"short_citation": "Dutta et al. 2025",
     "full_reference": "Dutta S et al. Parkinson's disease modeling in regenerative spiny mice (Acomys dimidiatus) captures key disease-relevant behavioral, histological, and molecular signatures. bioRxiv (2025).",
     "doi": "10.1101/2025.11.06.687049", "pmid": "", "pmc_id": "",
     "tissue_focus": "Brain (Parkinson's model)", "antibody_count": "7"},
    {"short_citation": "Morassut et al. 2026",
     "full_reference": "Morassut I et al. Prenatal assembly of functional cortical circuits. bioRxiv (2026).",
     "doi": "10.64898/2026.06.01.729224", "pmid": "", "pmc_id": "",
     "tissue_focus": "Brain (prenatal cortex)", "antibody_count": "7"},
    {"short_citation": "Merkulyeva et al. 2025",
     "full_reference": "Merkulyeva N, Veshchitskii AS, Mikhalkin AA, Beljajev A. Structure and cytoarchitecture of the retrosplenial cortex in the Cairo spiny mouse (Acomys cahirinus). Anat Rec. 2025.",
     "doi": "10.1002/ar.70119", "pmid": "", "pmc_id": "",
     "tissue_focus": "Brain (retrosplenial cortex)", "antibody_count": "3"},
    {"short_citation": "Qi et al. 2021",
     "full_reference": "Qi Y et al. Functional heart recovery in an adult mammal, the spiny mouse. Int J Cardiol. 2021;338:196-203.",
     "doi": "10.1016/j.ijcard.2021.06.015", "pmid": "", "pmc_id": "",
     "tissue_focus": "Heart (functional recovery)", "antibody_count": "4"},
    {"short_citation": "Gonzalez Abreu et al. 2022",
     "full_reference": "Gonzalez Abreu JA et al. Species-typical group size differentially influences social reward neural circuitry during nonreproductive social interactions. iScience. 2022;25(5):104230.",
     "doi": "10.1016/j.isci.2022.104230", "pmid": "", "pmc_id": "",
     "tissue_focus": "Brain (social circuitry); antibodies auto-western validated in spiny mouse", "antibody_count": "4"},
    {"short_citation": "Maden et al. 2023",
     "full_reference": "Maden M, Polvadore T, Polanco A, Barbazuk WB, Stanley EL. Osteoderms in a mammal the spiny mouse Acomys and the independent evolution of dermal armor. iScience. 2023;26(5):106779.",
     "doi": "10.1016/j.isci.2023.106779", "pmid": "", "pmc_id": "",
     "tissue_focus": "Skin/dermal (osteoderms)", "antibody_count": "1"},
    {"short_citation": "Ellery et al. 2018",
     "full_reference": "Ellery SJ et al. Evaluation of 3K3A-Activated Protein C to Treat Neonatal Hypoxic Ischemic Brain Injury in the Spiny Mouse. Dev Neurosci. 2018.",
     "doi": "10.1159/000493696", "pmid": "", "pmc_id": "",
     "tissue_focus": "Brain (neonatal hypoxic-ischemic injury)", "antibody_count": "1"},
]

_S_MAD = "Maden et al. 2023"
_D_MAD = "10.1016/j.isci.2023.106779"
_S_ELL = "Ellery et al. 2018"
_D_ELL = "10.1159/000493696"

_S_QI = "Qi et al. 2021"
_D_QI = "10.1016/j.ijcard.2021.06.015"
_S_ABREU = "Gonzalez Abreu et al. 2022"
_D_ABREU = "10.1016/j.isci.2022.104230"
_S_DUT = "Dutta et al. 2025"
_D_DUT = "10.1101/2025.11.06.687049"
_S_MOR = "Morassut et al. 2026"
_D_MOR = "10.64898/2026.06.01.729224"
_S_MERK = "Merkulyeva et al. 2025"
_D_MERK = "10.1002/ar.70119"
_S_HARN = "Harn et al. 2021"
_D_HARN = "10.1038/s41467-021-22822-9"
_S_SAX = "Saxena et al. 2019"
_D_SAX = "10.1038/s41467-019-12398-w"
_S_OVI = "Oviedo Rivadeneira et al. 2025"
_D_OVI = "10.1101/2025.02.10.637521"
_S_GAIRE = "Gaire et al. 2022"
_D_GAIRE = "10.1101/2022.08.12.503776"
_S_KO = "Ko et al. 2026"
_D_KO = "10.64898/2026.03.23.713756"
_S_CHUNG = "Chung et al. 2026"
_D_CHUNG = "10.64898/2026.05.08.723863"

_S_BREWER = "Brewer et al. 2021"
_D_BREWER = "10.1016/j.devcel.2021.09.008"
_S_SIMKIN = "Simkin et al. 2017"
_D_SIMKIN = "10.7554/elife.24623"
_S_OKA = "Okamura et al. 2021"
_D_OKA = "10.1016/j.isci.2021.103269"
_S_GAW = "Gawriluk et al. 2020"
_D_GAW = "10.1101/723783"

# --- newly mined antibodies -----------------------------------------------
ENTRIES = [
    # ---- Nogueira-Rodrigues et al. 2022 (Dev Cell) — Acomys spinal cord, IF ----
    dict(target="5-HT (Serotonin)", category="Neural", application="ICC/IHC", result="works",
         source_publication="Nogueira-Rodrigues et al. 2022", doi="10.1016/j.devcel.2021.12.008",
         catalog_number="20080", vendor="ImmunoStar", host_species="Rabbit", clonality="polyclonal",
         rrid="AB_572263", dilution="", tissue_tested="Spinal cord", notes="Serotonergic axons"),
    dict(target="Collagen I", category="ECM/Adhesion", application="ICC/IHC", result="works",
         source_publication="Nogueira-Rodrigues et al. 2022", doi="10.1016/j.devcel.2021.12.008",
         catalog_number="600-401-103-0.1", vendor="Rockland", host_species="Rabbit", clonality="polyclonal",
         rrid="AB_2074625", dilution="", tissue_tested="Spinal cord", notes=""),
    dict(target="GFAP", category="Neural", application="ICC/IHC", result="works",
         source_publication="Nogueira-Rodrigues et al. 2022", doi="10.1016/j.devcel.2021.12.008",
         catalog_number="Z0334", vendor="Agilent (Dako)", host_species="Rabbit", clonality="polyclonal",
         rrid="AB_10013382", dilution="", tissue_tested="Spinal cord", notes="Astrocytes"),
    dict(target="MBP (Myelin basic protein)", category="Neural", application="ICC/IHC", result="works",
         source_publication="Nogueira-Rodrigues et al. 2022", doi="10.1016/j.devcel.2021.12.008",
         catalog_number="10458-1-AP", vendor="Proteintech", host_species="Rabbit", clonality="polyclonal",
         rrid="AB_2250289", dilution="", tissue_tested="Spinal cord", notes=""),
    dict(target="Ndst3", category="Enzyme", application="ICC/IHC", result="works",
         source_publication="Nogueira-Rodrigues et al. 2022", doi="10.1016/j.devcel.2021.12.008",
         catalog_number="PA5-63262", vendor="Thermo Fisher", host_species="Rabbit", clonality="polyclonal",
         rrid="AB_2644540", dilution="1:200", tissue_tested="Spinal cord", notes=""),
    dict(target="NGAL (LCN2)", category="Immune", application="ICC/IHC", result="works",
         source_publication="Nogueira-Rodrigues et al. 2022", doi="10.1016/j.devcel.2021.12.008",
         catalog_number="PA5-88079", vendor="Thermo Fisher", host_species="Rabbit", clonality="polyclonal",
         rrid="AB_2804634", dilution="1:200", tissue_tested="Spinal cord", notes=""),
    dict(target="SCG10 (Stathmin-2)", category="Neural", application="ICC/IHC", result="works",
         source_publication="Nogueira-Rodrigues et al. 2022", doi="10.1016/j.devcel.2021.12.008",
         catalog_number="NBP1-49461", vendor="Novus", host_species="Rabbit", clonality="polyclonal",
         rrid="AB_10011569", dilution="", tissue_tested="Spinal cord", notes="Regenerating sensory axon marker"),
    dict(target="VGLUT1", category="Neural", application="ICC/IHC", result="works",
         source_publication="Nogueira-Rodrigues et al. 2022", doi="10.1016/j.devcel.2021.12.008",
         catalog_number="135 303", vendor="Synaptic Systems", host_species="Rabbit", clonality="polyclonal",
         rrid="AB_887875", dilution="", tissue_tested="Spinal cord", notes=""),
    dict(target="B3gnt7", category="Enzyme", application="ICC/IHC", result="works",
         source_publication="Nogueira-Rodrigues et al. 2022", doi="10.1016/j.devcel.2021.12.008",
         catalog_number="PA5-57342", vendor="Thermo Fisher", host_species="Rabbit", clonality="polyclonal",
         rrid="AB_2638427", dilution="1:100", tissue_tested="Spinal cord", notes=""),
    dict(target="beta-III tubulin (TUJ1)", category="Neural", application="ICC/IHC", result="works",
         source_publication="Nogueira-Rodrigues et al. 2022", doi="10.1016/j.devcel.2021.12.008",
         catalog_number="302 302", vendor="Synaptic Systems", host_species="Rabbit", clonality="polyclonal",
         rrid="AB_10637424", dilution="", tissue_tested="Spinal cord", notes=""),
    dict(target="beta-III tubulin (TUJ1)", category="Neural", application="ICC/IHC", result="works",
         source_publication="Nogueira-Rodrigues et al. 2022", doi="10.1016/j.devcel.2021.12.008",
         catalog_number="G7121", vendor="Promega", host_species="Mouse", clonality="monoclonal",
         rrid="AB_430874", dilution="", tissue_tested="Spinal cord", notes=""),
    dict(target="Heparan Sulfate", category="ECM/Adhesion", application="ICC/IHC", result="works",
         source_publication="Nogueira-Rodrigues et al. 2022", doi="10.1016/j.devcel.2021.12.008",
         catalog_number="370255-1", vendor="AMSBIO", host_species="Mouse", clonality="monoclonal",
         rrid="AB_10891554", dilution="", tissue_tested="Spinal cord", notes="Clone F58-10E4"),
    dict(target="Keratan Sulfate", category="ECM/Adhesion", application="ICC/IHC", result="works",
         source_publication="Nogueira-Rodrigues et al. 2022", doi="10.1016/j.devcel.2021.12.008",
         catalog_number="270427-1", vendor="AMSBIO", host_species="Mouse", clonality="monoclonal",
         rrid="AB_10920069", dilution="", tissue_tested="Spinal cord", notes="Clone 5D4"),

    # ---- Brewer et al. 2021 (Dev Cell) — Acomys ear + dermal fibroblasts; IHC/ICC + WB ----
    # Cross-species recognition validated by WB single-band + immunostaining in Mus and Acomys.
    E("Cleaved Caspase-3", "Enzyme", "ICC/IHC", _S_BREWER, _D_BREWER, "9661", "Cell Signaling", "Rabbit", "polyclonal", dilution="1:200", tissue="Ear, dermal fibroblasts"),
    E("EDA-Fibronectin", "ECM/Adhesion", "ICC/IHC", _S_BREWER, _D_BREWER, "ab6328", "Abcam", "Mouse", "monoclonal", dilution="1:200", tissue="Ear, dermal fibroblasts"),
    E("Smooth Muscle Myosin Heavy Chain (MYH11)", "Muscle", "ICC/IHC", _S_BREWER, _D_BREWER, "BT562", "Biomedical Technologies", "Rabbit", "polyclonal", dilution="1:500", tissue="Ear, dermal fibroblasts", notes="Cross-species recognition validated"),
    E("Alpha-Smooth Muscle Actin (ACTA2)", "Muscle", "ICC/IHC, WB", _S_BREWER, _D_BREWER, "A2547", "Sigma", "Mouse", "monoclonal", dilution="1:2000", tissue="Ear, dermal fibroblasts", notes="Cross-species recognition validated"),
    E("PCNA", "Proliferation/Cell Cycle", "ICC/IHC", _S_BREWER, _D_BREWER, "2586", "Cell Signaling", "Mouse", "monoclonal", dilution="1:100", tissue="Ear, dermal fibroblasts"),
    E("Vimentin", "Cytoplasmic", "ICC/IHC", _S_BREWER, _D_BREWER, "V5255", "Sigma", "Mouse", "monoclonal", dilution="1:500", tissue="Ear, dermal fibroblasts"),
    E("Vinculin", "Cytoplasmic", "ICC/IHC, WB", _S_BREWER, _D_BREWER, "V9131", "Sigma", "Mouse", "monoclonal", dilution="1:200 (IHC), 1:5000 (WB)", tissue="Ear, dermal fibroblasts"),
    E("YAP", "Signaling/TF", "ICC/IHC", _S_BREWER, _D_BREWER, "sc-15407", "Santa Cruz", "Rabbit", "polyclonal", dilution="1:500", tissue="Ear, dermal fibroblasts"),
    E("CTGF (CCN2)", "Signaling/TF", "ICC/IHC", _S_BREWER, _D_BREWER, "86641T", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:100", tissue="Ear, dermal fibroblasts"),
    E("p44/42 MAPK (ERK1/2)", "Signaling/TF", "ICC/IHC", _S_BREWER, _D_BREWER, "4695", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:400", tissue="Ear, dermal fibroblasts"),
    E("Phospho-AKT (Thr308)", "Signaling/TF", "ICC/IHC", _S_BREWER, _D_BREWER, "", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:2000", tissue="Dermal fibroblasts", notes="Clone 244F9"),
    E("Phospho-AKT (Ser473)", "Signaling/TF", "ICC/IHC", _S_BREWER, _D_BREWER, "4060", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:2000", tissue="Dermal fibroblasts", notes="Clone D9E XP"),
    E("AKT", "Signaling/TF", "ICC/IHC", _S_BREWER, _D_BREWER, "2920", "Cell Signaling", "Mouse", "monoclonal", dilution="1:1000", tissue="Dermal fibroblasts", notes="Clone 40D4"),
    E("Beta-Tubulin", "Cytoplasmic", "WB", _S_BREWER, _D_BREWER, "BT7R", "Sigma", "Mouse", "monoclonal", dilution="1:5000", tissue="Dermal fibroblasts", notes="Loading control"),
    E("GAPDH", "Cytoplasmic", "WB", _S_BREWER, _D_BREWER, "5174", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:5000", tissue="Dermal fibroblasts", notes="Loading control"),
    E("Phospho-LATS1 (Thr1079)", "Signaling/TF", "WB", _S_BREWER, _D_BREWER, "9159", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:1000", tissue="Dermal fibroblasts"),
    E("SMAD2", "Signaling/TF", "WB", _S_BREWER, _D_BREWER, "5339", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:2000", tissue="Dermal fibroblasts"),
    E("Phospho-SMAD2 (Ser465/467)", "Signaling/TF", "WB", _S_BREWER, _D_BREWER, "3108", "Cell Signaling", "Rabbit", "polyclonal", dilution="1:1000", tissue="Dermal fibroblasts"),
    E("SMAD3", "Signaling/TF", "WB", _S_BREWER, _D_BREWER, "9523", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:2000", tissue="Dermal fibroblasts"),
    E("Phospho-SMAD3 (Ser423/425)", "Signaling/TF", "WB", _S_BREWER, _D_BREWER, "9520", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:1000", tissue="Dermal fibroblasts"),
    E("TAZ (WWTR1)", "Signaling/TF", "WB", _S_BREWER, _D_BREWER, "4883", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:1000", tissue="Dermal fibroblasts"),
    E("YAP", "Signaling/TF", "WB", _S_BREWER, _D_BREWER, "ab5670", "Abcam", "Mouse", "monoclonal", dilution="1:1000", tissue="Dermal fibroblasts"),
    E("Phospho-YAP (Ser127)", "Signaling/TF", "WB", _S_BREWER, _D_BREWER, "4911", "Cell Signaling", "Rabbit", "polyclonal", dilution="1:1000", tissue="Dermal fibroblasts"),
    E("Phospho-YAP (Ser381)", "Signaling/TF", "WB", _S_BREWER, _D_BREWER, "13619", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:1000", tissue="Dermal fibroblasts"),

    # ---- Simkin et al. 2017 (eLife) — Acomys ear macrophages; Flow + IHC/ICC ----
    E("Ly6G", "Immune", "Flow", _S_SIMKIN, _D_SIMKIN, "560599", "BD Pharmingen", "Rat", "monoclonal", dilution="3 ug/mL", tissue="Ear", notes="APC-conjugated; clone 1A8"),
    E("CD11b", "Immune", "Flow", _S_SIMKIN, _D_SIMKIN, "557397", "BD Pharmingen", "Rat", "monoclonal", dilution="3 ug/mL", tissue="Ear", notes="PE-conjugated"),
    E("MPO (Myeloperoxidase)", "Immune", "ICC/IHC", _S_SIMKIN, _D_SIMKIN, "A0398", "Dako", "Rabbit", "polyclonal", dilution="", tissue="Ear", notes="Anti-human; neutrophils"),
    E("CD86", "Immune", "ICC/IHC", _S_SIMKIN, _D_SIMKIN, "553698", "BD Biosciences", "Rat", "monoclonal", dilution="1:100", tissue="Ear", notes="Also cat #553689"),
    E("CD206 (MRC1)", "Immune", "ICC/IHC", _S_SIMKIN, _D_SIMKIN, "AF2535", "R&D Systems", "Goat", "polyclonal", dilution="1:1000", tissue="Ear", notes="M2 macrophage marker"),
    E("CD3", "Immune", "ICC/IHC", _S_SIMKIN, _D_SIMKIN, "A0452", "Dako", "Rabbit", "polyclonal", dilution="1:400", tissue="Ear", notes="Anti-human; T cells"),
    E("IBA1 (AIF1)", "Immune", "ICC/IHC", _S_SIMKIN, _D_SIMKIN, "019-19741", "Wako", "Rabbit", "polyclonal", dilution="1:1000", tissue="Ear", notes="Macrophage/microglia"),
    E("Arginase-1 (ARG1)", "Immune", "ICC/IHC", _S_SIMKIN, _D_SIMKIN, "113131", "GeneTex", "Rabbit", "polyclonal", dilution="1:500", tissue="Ear", notes="M2 macrophage marker"),
    E("CD11b", "Immune", "ICC/IHC", _S_SIMKIN, _D_SIMKIN, "MCA74G", "Bio-Rad (AbD Serotec)", "Rat", "monoclonal", dilution="1:500", tissue="Ear"),
    E("F4/80", "Immune", "ICC/IHC", _S_SIMKIN, _D_SIMKIN, "14-4801-82", "eBioscience", "Rat", "monoclonal", dilution="1:400", tissue="Ear", notes="Clone BM8"),

    # ---- Okamura et al. 2021 (iScience) — Acomys kidney; IHC (STAR resources table) ----
    E("Alpha-Smooth Muscle Actin (ACTA2)", "Muscle", "ICC/IHC", _S_OKA, _D_OKA, "A2547", "Sigma", "Mouse", "monoclonal", rrid="AB_476701", tissue="Kidney", notes="Clone 1A4"),
    E("pan-Laminin", "ECM/Adhesion", "ICC/IHC", _S_OKA, _D_OKA, "ab11575", "Abcam", "Rabbit", "polyclonal", rrid="AB_298179", tissue="Kidney"),
    E("F4/80", "Immune", "ICC/IHC", _S_OKA, _D_OKA, "MF48000", "Thermo Fisher", "Rat", "monoclonal", rrid="AB_10376289", tissue="Kidney"),
    E("E-cadherin (CDH1)", "Cell Surface/Membrane", "ICC/IHC", _S_OKA, _D_OKA, "610181", "BD Biosciences", "Mouse", "monoclonal", rrid="AB_397581", tissue="Kidney"),
    E("ZO-1 (TJP1)", "Cell Surface/Membrane", "ICC/IHC", _S_OKA, _D_OKA, "ab221547", "Abcam", "Rabbit", "monoclonal", rrid="AB_2892660", tissue="Kidney"),
    E("Vinculin", "Cytoplasmic", "ICC/IHC", _S_OKA, _D_OKA, "V9131", "Sigma", "Mouse", "monoclonal", rrid="AB_477629", tissue="Kidney"),

    # ---- Gawriluk et al. 2020 (bioRxiv 723783) — Acomys ear/musculoskeletal; WB + Flow ----
    E("Phospho-STAT3 (pSTAT3)", "Signaling/TF", "WB", _S_GAW, _D_GAW, "9145", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:2000", tissue="Ear/limb muscle"),
    E("Beta-Actin (ACTB)", "Cytoplasmic", "WB", _S_GAW, _D_GAW, "4967", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:5000", tissue="Ear/limb muscle", notes="Loading control"),
    E("CD3", "Immune", "Flow", _S_GAW, _D_GAW, "", "BioLegend", "Rat", "monoclonal", dilution="1 ug/1e6 cells", tissue="Ear/limb (T cells)", notes="PE-conjugated; clone 17A2. Paper reports many other T-cell antibodies FAILED cross-reactivity in Acomys."),

    # ---- Ko et al. 2026 (bioRxiv) — Acomys skin; IHC ----
    E("Perilipin-1 (PLIN1)", "Cytoplasmic", "ICC/IHC", _S_KO, _D_KO, "ab3526", "Abcam", "Rabbit", "polyclonal", dilution="1:200", tissue="Skin", notes="Adipocyte marker"),
    E("Collagen I", "ECM/Adhesion", "ICC/IHC", _S_KO, _D_KO, "ab34710", "Abcam", "Rabbit", "polyclonal", dilution="1:1000", tissue="Skin"),
    E("Collagen VI", "ECM/Adhesion", "ICC/IHC", _S_KO, _D_KO, "ab182744", "Abcam", "Rabbit", "polyclonal", dilution="1:200", tissue="Skin"),
    E("PECAM-1 (CD31)", "Cell Surface/Membrane", "ICC/IHC", _S_KO, _D_KO, "AF3628", "R&D Systems", "Goat", "polyclonal", dilution="1:200", tissue="Skin", notes="Endothelial"),
    E("Keratin 14 (K14)", "Cytokeratin/Epidermis", "ICC/IHC", _S_KO, _D_KO, "906004", "BioLegend", "Chicken", "polyclonal", dilution="1:1000", tissue="Skin"),
    E("Collagen III", "ECM/Adhesion", "ICC/IHC", _S_KO, _D_KO, "ab7778", "Abcam", "Rabbit", "polyclonal", dilution="1:200", tissue="Skin"),
    E("Collagen XVII", "ECM/Adhesion", "ICC/IHC", _S_KO, _D_KO, "ab184996", "Abcam", "Rabbit", "polyclonal", dilution="1:200", tissue="Skin"),
    E("Alpha-Smooth Muscle Actin (ACTA2)", "Muscle", "ICC/IHC", _S_KO, _D_KO, "ab5694", "Abcam", "Rabbit", "polyclonal", dilution="1:500", tissue="Skin"),
    E("LYVE-1", "Cell Surface/Membrane", "ICC/IHC", _S_KO, _D_KO, "11-034", "AngioBio", "Rabbit", "polyclonal", dilution="1:200", tissue="Skin", notes="Lymphatic endothelium"),
    E("beta-III tubulin (TUJ1)", "Neural", "ICC/IHC", _S_KO, _D_KO, "ab18207", "Abcam", "Rabbit", "polyclonal", dilution="1:200", tissue="Skin"),
    E("PDGFRalpha", "Cell Surface/Membrane", "ICC/IHC", _S_KO, _D_KO, "ab203491", "Abcam", "Rabbit", "monoclonal", dilution="1:200", tissue="Skin"),
    E("CUX1", "Signaling/TF", "ICC/IHC", _S_KO, _D_KO, "11733-1-AP", "Proteintech", "Rabbit", "polyclonal", dilution="1:100", tissue="Skin"),
    E("Neurofilament Heavy (NF-H)", "Neural", "ICC/IHC", _S_KO, _D_KO, "ab207176", "Abcam", "Rabbit", "monoclonal", dilution="1:1000", tissue="Skin", notes="Clone EPR20020"),

    # ---- Chung et al. 2026 (bioRxiv) — Acomys brain/colon nervous system; IHC ----
    E("NeuN (RBFOX3)", "Neural", "ICC/IHC", _S_CHUNG, _D_CHUNG, "ab177487", "Abcam", "Rabbit", "monoclonal", rrid="AB_2532109", dilution="1:500", tissue="Brain"),
    E("GLUT1 (SLC2A1)", "Cell Surface/Membrane", "ICC/IHC", _S_CHUNG, _D_CHUNG, "07-1401", "Millipore", "Rabbit", "polyclonal", rrid="AB_1587074", dilution="1:500", tissue="Brain"),
    E("Alpha-Smooth Muscle Actin (ACTA2)", "Muscle", "ICC/IHC", _S_CHUNG, _D_CHUNG, "NB300-978", "Novus", "Rabbit", "polyclonal", rrid="AB_2273628", dilution="1:400", tissue="Brain, colon"),
    E("beta-III tubulin (TUJ1)", "Neural", "ICC/IHC", _S_CHUNG, _D_CHUNG, "801202", "BioLegend", "Mouse", "monoclonal", rrid="AB_2313773", dilution="1:200", tissue="Brain, colon"),

    # ---- Oviedo Rivadeneira et al. 2025 (bioRxiv) — Acomys ear; IHC ----
    E("SOX9", "Signaling/TF", "ICC/IHC", _S_OVI, _D_OVI, "ab185230", "Abcam", "Rabbit", "monoclonal", rrid="AB_2715497", dilution="1:1000", tissue="Ear"),
    E("CD206 (MRC1)", "Immune", "ICC/IHC", _S_OVI, _D_OVI, "AF2535", "R&D Systems", "Goat", "polyclonal", rrid="AB_2063012", dilution="1:500", tissue="Ear", notes="Macrophage mannose receptor"),

    # ---- Gaire et al. 2022 (bioRxiv) — Acomys skin/implant; IHC ----
    E("Alpha-Smooth Muscle Actin (ACTA2)", "Muscle", "ICC/IHC", _S_GAIRE, _D_GAIRE, "ab7817", "Abcam", "Mouse", "monoclonal", dilution="1:500", tissue="Skin (implant)"),
    E("IBA1 (AIF1)", "Immune", "ICC/IHC", _S_GAIRE, _D_GAIRE, "019-19741", "Wako", "Rabbit", "polyclonal", dilution="1:400", tissue="Skin (implant)"),
    E("MPO (Myeloperoxidase)", "Immune", "ICC/IHC", _S_GAIRE, _D_GAIRE, "A0398", "Agilent (Dako)", "Rabbit", "polyclonal", dilution="1:400", tissue="Skin (implant)"),

    # ---- Harn et al. 2021 (Nat Commun) — Mus + Acomys skin/hair follicle; IHC ----
    E("Twist1", "Signaling/TF", "ICC/IHC", _S_HARN, _D_HARN, "ab50887", "Abcam", "Rabbit", "monoclonal", tissue="Skin (hair follicle)"),
    E("MMP9", "Enzyme", "ICC/IHC", _S_HARN, _D_HARN, "GTX100458", "GeneTex", "Rabbit", "polyclonal", tissue="Skin (hair follicle)", notes="Clone N2C1"),
    E("Snai1 (SNAIL)", "Signaling/TF", "ICC/IHC", _S_HARN, _D_HARN, "13099-1-AP", "Proteintech", "Rabbit", "polyclonal", tissue="Skin (hair follicle)"),
    E("P-cadherin (CDH3)", "Cell Surface/Membrane", "ICC/IHC", _S_HARN, _D_HARN, "13773-1-AP", "Proteintech", "Rabbit", "polyclonal", tissue="Skin (hair follicle)"),
    E("E-cadherin (CDH1)", "Cell Surface/Membrane", "ICC/IHC", _S_HARN, _D_HARN, "20874-1-AP", "Proteintech", "Rabbit", "polyclonal", tissue="Skin (hair follicle)"),
    E("Zeb2", "Signaling/TF", "ICC/IHC", _S_HARN, _D_HARN, "14026-1-AP", "Proteintech", "Rabbit", "polyclonal", tissue="Skin (hair follicle)"),
    E("Collagen I", "ECM/Adhesion", "ICC/IHC", _S_HARN, _D_HARN, "ab34710", "Abcam", "Rabbit", "polyclonal", tissue="Skin (hair follicle)"),
    E("Collagen III", "ECM/Adhesion", "ICC/IHC", _S_HARN, _D_HARN, "ab7778", "Abcam", "Rabbit", "polyclonal", tissue="Skin (hair follicle)"),

    # ---- Saxena et al. 2019 (Nat Commun) — Acomys fibroblasts, senescence; ICC ----
    E("p16 (CDKN2A / p16INK4A)", "Proliferation/Cell Cycle", "ICC/IHC", _S_SAX, _D_SAX, "10883-1-AP", "Proteintech", "Rabbit", "polyclonal", dilution="1:100", tissue="Fibroblasts"),
    E("p19ARF", "Proliferation/Cell Cycle", "ICC/IHC", _S_SAX, _D_SAX, "sc-32748", "Santa Cruz", "Rat", "monoclonal", dilution="1:100", tissue="Fibroblasts"),
    E("p53", "Proliferation/Cell Cycle", "ICC/IHC", _S_SAX, _D_SAX, "NCL-P53-CM5P", "Leica (Novocastra)", "Rabbit", "polyclonal", dilution="1:500", tissue="Fibroblasts"),
    E("gamma-H2AX (Ser139)", "Proliferation/Cell Cycle", "ICC/IHC", _S_SAX, _D_SAX, "", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:500", tissue="Fibroblasts", notes="Clone 20E3"),
    E("Vimentin", "Cytoplasmic", "ICC/IHC", _S_SAX, _D_SAX, "5741S", "Cell Signaling", "Rabbit", "monoclonal", dilution="1:100", tissue="Fibroblasts"),

    # ---- Dutta et al. 2025 (bioRxiv) — Acomys dimidiatus brain (Parkinson's); IHC ----
    E("Tyrosine Hydroxylase (TH)", "Enzyme", "ICC/IHC", _S_DUT, _D_DUT, "AB152", "Millipore", "Rabbit", "polyclonal", rrid="AB_390204", dilution="1:1000", tissue="Brain"),
    E("GFAP", "Neural", "ICC/IHC", _S_DUT, _D_DUT, "ab4674", "Abcam", "Chicken", "polyclonal", rrid="AB_304558", dilution="1:1000", tissue="Brain"),
    E("IBA1 (AIF1)", "Immune", "ICC/IHC", _S_DUT, _D_DUT, "019-19741", "Wako", "Rabbit", "polyclonal", rrid="AB_839504", dilution="1:1000", tissue="Brain"),
    E("pS129 alpha-Synuclein", "Neural", "ICC/IHC", _S_DUT, _D_DUT, "ab51253", "Abcam", "Rabbit", "monoclonal", rrid="AB_869973", dilution="1:500", tissue="Brain", notes="Clone EP1536Y"),
    E("pS129 alpha-Synuclein", "Neural", "ICC/IHC", _S_DUT, _D_DUT, "825701", "BioLegend", "Mouse", "monoclonal", rrid="AB_2564891", dilution="1:500", tissue="Brain", notes="Clone 81a"),
    E("Ubiquitin", "Cytoplasmic", "ICC/IHC", _S_DUT, _D_DUT, "80992-1-RR", "Proteintech", "Rabbit", "monoclonal", rrid="AB_2923694", dilution="1:500", tissue="Brain"),
    E("p62 / SQSTM1", "Cytoplasmic", "ICC/IHC", _S_DUT, _D_DUT, "18420-1-AP", "Proteintech", "Rabbit", "polyclonal", rrid="AB_10694431", dilution="1:500", tissue="Brain", notes="Autophagy"),

    # ---- Morassut et al. 2026 (bioRxiv) — brain cortex (comparative, incl. Acomys); IHC ----
    E("CTIP2 (BCL11B)", "Neural", "ICC/IHC", _S_MOR, _D_MOR, "ab18465", "Abcam", "Rat", "monoclonal", tissue="Brain (cortex)"),
    E("MBP (Myelin basic protein)", "Neural", "ICC/IHC", _S_MOR, _D_MOR, "ab7349", "Abcam", "Rat", "monoclonal", tissue="Brain (cortex)"),
    E("L1CAM", "Cell Surface/Membrane", "ICC/IHC", _S_MOR, _D_MOR, "MAB5272", "Merck Millipore", "Mouse", "monoclonal", tissue="Brain (cortex)"),
    E("RORB", "Signaling/TF", "ICC/IHC", _S_MOR, _D_MOR, "PP-N7927-00", "Bio-Techne", "Mouse", "monoclonal", tissue="Brain (cortex)"),
    E("VGLUT2 (SLC17A6)", "Neural", "ICC/IHC", _S_MOR, _D_MOR, "AB2251", "Merck Millipore", "Guinea pig", "polyclonal", tissue="Brain (cortex)"),
    E("S100beta", "Neural", "ICC/IHC", _S_MOR, _D_MOR, "ab41548", "Abcam", "Rabbit", "monoclonal", tissue="Brain (cortex)", notes="Astrocyte marker"),
    E("BrdU", "Proliferation/Cell Cycle", "ICC/IHC", _S_MOR, _D_MOR, "B35128", "Life Technologies", "Mouse", "monoclonal", tissue="Brain (cortex)", notes="Clone MoBU-1"),

    # ---- Merkulyeva et al. 2025 (Anat Rec) — Acomys cahirinus brain; IHC (catalog #s not reported) ----
    E("SMI-32 (non-phospho Neurofilament H)", "Neural", "ICC/IHC", _S_MERK, _D_MERK, "", "BioLegend (Covance)", "Mouse", "monoclonal", dilution="1:15000", tissue="Brain (retrosplenial cortex)", notes="Clone SMI-32"),
    E("NeuN (RBFOX3)", "Neural", "ICC/IHC", _S_MERK, _D_MERK, "", "Millipore", "Mouse", "monoclonal", dilution="1:3000", tissue="Brain (retrosplenial cortex)"),
    E("Calbindin (CB, 28 kDa)", "Neural", "ICC/IHC", _S_MERK, _D_MERK, "", "Sigma-Aldrich", "Mouse", "monoclonal", tissue="Brain (retrosplenial cortex)"),

    # ---- Qi et al. 2021 (Int J Cardiol) — Acomys heart; IHC ----
    E("BrdU", "Proliferation/Cell Cycle", "ICC/IHC", _S_QI, _D_QI, "ab6326", "Abcam", "Rat", "monoclonal", dilution="1:200", tissue="Heart", notes="Clone BU1/75"),
    E("Ki67", "Proliferation/Cell Cycle", "ICC/IHC", _S_QI, _D_QI, "ab16667", "Abcam", "Rabbit", "monoclonal", dilution="1:500", tissue="Heart"),
    E("Sarcomeric alpha-actinin", "Muscle", "ICC/IHC", _S_QI, _D_QI, "ab68167", "Abcam", "Rabbit", "polyclonal", dilution="1:200", tissue="Heart", notes="Cardiomyocyte marker"),
    E("PCM-1", "Cytoplasmic", "ICC/IHC", _S_QI, _D_QI, "ab72443", "Abcam", "Rabbit", "polyclonal", dilution="1:200", tissue="Heart", notes="Cardiomyocyte nuclei marker"),

    # ---- Gonzalez Abreu et al. 2022 (iScience) — Acomys brain; IHC (auto-western validated in spiny mouse) ----
    E("Oxytocin (OT)", "Hormone/Receptor", "ICC/IHC", _S_ABREU, _D_ABREU, "MAB5296", "Millipore", "Mouse", "monoclonal", rrid="AB_2157626", dilution="1:1000", tissue="Brain", notes="Validated in spiny mouse brain (auto-western; preadsorption)"),
    E("Tyrosine Hydroxylase (TH)", "Enzyme", "ICC/IHC", _S_ABREU, _D_ABREU, "MAB318", "Millipore", "Mouse", "monoclonal", rrid="AB_2201528", dilution="1:1000", tissue="Brain", notes="Validated in spiny mouse brain (auto-western; preadsorption)"),
    E("c-Fos (FOS)", "Signaling/TF", "ICC/IHC", _S_ABREU, _D_ABREU, "226 003", "Synaptic Systems", "Rabbit", "polyclonal", rrid="AB_2231974", dilution="1:500", tissue="Brain", notes="Validated in spiny mouse brain (auto-western; preadsorption)"),
    E("AADC (DDC)", "Enzyme", "ICC/IHC", _S_ABREU, _D_ABREU, "AB1569", "Millipore", "Rabbit", "polyclonal", rrid="", dilution="", tissue="Brain", notes="Validated in spiny mouse brain (auto-western; preadsorption)"),

    # ---- Maden et al. 2023 (iScience) — Acomys skin/osteoderms; IHC ----
    E("Sp7 / Osterix", "Signaling/TF", "ICC/IHC", _S_MAD, _D_MAD, "ab227820", "Abcam", "Rabbit", "monoclonal", dilution="1:500", tissue="Skin (osteoderms)", notes="Osteoblast transcription factor"),

    # ---- Ellery et al. 2018 (Dev Neurosci) — Acomys neonatal brain; IHC ----
    E("CD11b (ITGAM)", "Immune", "ICC/IHC", _S_ELL, _D_ELL, "ab62817", "Abcam", "Rabbit", "polyclonal", dilution="1:1000", tissue="Brain (neonatal)", notes="Activated microglia"),
]
