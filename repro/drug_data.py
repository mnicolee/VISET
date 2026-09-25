"""Drug target gene sets from Enrichr (https://maayanlab.cloud/Enrichr/#libraries).

Shared by the repro notebook and by the subprocesses that render it under an
older eunoia, so both sides are guaranteed to plot the same data.
"""
A, S, U = 'Atorvastatin', 'Simvastatin', 'Sunitinib'

DATA = {
    A: ['ABCA1', 'ABCB1', 'ACE', 'AGTR1', 'APOA5', 'APOB', 'BDKRB2', 'BGLAP', 'CACNA1S', 'CD40LG',
        'CLMN', 'CXCL10', 'CYP3A4', 'CYP3A7', 'DRD3', 'FAS', 'FGF2', 'HLA-DRB1', 'HMGCR', 'HSPD1',
        'IFNL3', 'IFNL4', 'IL2RA', 'ITGAM', 'LEPR', 'LIPC', 'MAPK10', 'MTHFR', 'MYLIP', 'NOS1',
        'NOS3', 'NR1I2', 'PIK3CG', 'POR', 'PPARD', 'PRDM16', 'RYR1', 'SLCO1B1', 'SOAT1', 'TFPI',
        'TGM2', 'TNF', 'UGT1A1', 'UGT1A10', 'UGT1A3', 'UGT1A4', 'UGT1A5', 'UGT1A6', 'UGT1A7',
        'UGT1A8', 'UGT1A9'],
    S: ['ABCA1', 'ABCB1', 'ABCC2', 'ABCG8', 'APOA5', 'AR', 'BDNF', 'CACNA1S', 'CCR2', 'CEL',
        'CYBA', 'CYP1A2', 'CYP2C19', 'CYP2C8', 'CYP2C9', 'CYP2D6', 'CYP3A4', 'CYP3A5', 'F3',
        'HLA-DRB1', 'HLA-G', 'HMGCR', 'ICMT', 'IDH1', 'IL17A', 'LEPR', 'LIF', 'LIPC', 'MMP2',
        'NFE2L2', 'NR1I2', 'NR2E3', 'PIK3CG', 'PLK1', 'PLTP', 'PON1', 'PRDM16', 'RHOA', 'RYR1',
        'SCAP', 'SLCO2B1', 'THBD', 'THBS1', 'TPM3', 'UGT1A9', 'ZNF542P'],
    U: ['BAP1', 'CA9', 'CSF1R', 'CXCL8', 'CYP3A4', 'EWSR1', 'FGFR1', 'FGFR2', 'FLT1', 'FLT3',
        'FLT4', 'HIF1A', 'HMOX1', 'IL4R', 'KDM5C', 'KDR', 'KIT', 'MKI67', 'NOS3', 'NR1I2',
        'NR1I3', 'PBRM1', 'PDGFA', 'PDGFB', 'PDGFC', 'PDGFD', 'PDGFRA', 'PDGFRB', 'POR', 'PTEN',
        'PTPN12', 'PTPRB', 'RET', 'SLC22A5', 'TP53', 'VEGFA', 'VEGFC', 'VHL', 'YES1'],
}

LABELS = [A, S, U]
