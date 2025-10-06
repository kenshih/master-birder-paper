select a.avibase_id, n.ncbi_taxon_id, n.scientific_name
FROM AvibaseID a
JOIN NCBITaxonID n on a.concept_label = n.scientific_name
