import json

with open('categories_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Update General Regeneration & Wound Healing
config["General Regeneration & Wound Healing"] = ["regenerat*", "wound", "scar", "healing", "blastema", "epimorphic", "recovery", "repair"]

# Update Cancer Resistance
config["Cancer Resistance"] = ["cancer", "tumor*", "tumour*", "carcinoma*", "neoplasm*", "oncolog*"]

# Update Tissue: Skin & Hair
config["Tissue: Skin & Hair"] = ["skin", "cutaneous", "hair follicle*", "whisker follicle*", "dermis", "epidermis", "wound bed", "sebaceous"]

# Update Tissue: Nervous System
config["Tissue: Nervous System"] = ["neuro*", "nerve*", "spinal cord", "brain", "innervation", "neuron*", "axon*", "stroke", "central nervous system", "peripheral nervous system"]

# Update Tissue: Retina & Visual System
config["Tissue: Retina & Visual System"] = ["retina*", "visual*", "eye", "eyes", "cornea*", "ocular", "optic"]

# Add Tissue: Liver & Hepatic
config["Tissue: Liver & Hepatic"] = ["liver", "hepatic", "hepatocyte*"]

# Update Neuroscience & Behavior
config["Neuroscience & Behavior"] = ["behavior*", "cognition", "social", "memory", "learning", "circadian", "sleep", "psychobiology", "dominance hierarchy", "startle"]

# Update Tools & Techniques
config["Tools & Techniques"] = ["method*", "protocol*", "apparatus", "assay*", "technique*", "model system*", "t-maze", "water maze", "protocols.io", "stereotaxic"]

# Update Metabolism, Endocrinology & Physiology
config["Metabolism, Endocrinology & Physiology"] = ["metabolism", "endocrin*", "physiolog*", "diabetes", "insulin", "diet", "temperature regulation", "water economy", "glucocorticoid*"]

# Update Immunology & Infection
config["Immunology & Infection"] = ["immun*", "infection*", "macrophage*", "inflammation", "t cell*", "b cell*", "leukocyte*", "pathogen*", "disease*", "virus*", "bacteria*"]

# Update Cell & Molecular Biology
config["Cell & Molecular Biology"] = ["cell biology", "molecular biology", "fibroblast*", "stem cell*", "proliferation", "apoptosis"]

# Update Veterinary & Animal Welfare
config["Veterinary & Animal Welfare"] = ["animal welfare", "veterinary", "housing conditions", "cage enrichment", "husbandry", "bite wounds", "dominance structures", "buprenorphine", "analgesi*", "pharmacokinetics", "efficacy", "sustained-release"]

# Update Taxonomy, Systematics & Evolution
config["Taxonomy, Systematics & Evolution"] = ["sp. nov", "species nova", "phylogen*", "taxonomy", "evolution", "systematics", "new species", "speciation"]

with open('categories_config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2)

