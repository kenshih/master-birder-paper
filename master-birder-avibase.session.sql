select count(*) -- count of species in Avibase: 11,125
FROM AvibaseID a
JOIN TaxanomicConcepts tc on a.avibase_id = tc.avibase_id
where tc.concept_id like 'SPECIES-%'
/* 
select a.avibase_id, n.ncbi_taxon_id, n.scientific_name
FROM AvibaseID a
JOIN NCBITaxonID n on a.concept_label = n.scientific_name
where n.scientific_name like 'Anas platyrhynchos'

some discovery and sanity checking queries ran along the way
select a.avibase_id, a.concept_label
FROM AvibaseID a
JOIN TaxanomicConcepts tc on a.avibase_id = tc.avibase_id

select *
FROM AvibaseID a
JOIN TaxanomicConcepts tc on a.avibase_id = tc.avibase_id
WHERE tc.scientific_name like 'Calypte %'
limit 100

where concept_label in ('Myiothlypis griseiceps', 'Aegotheles albertisi')

SELECT *
FROM TaxanomicConcepts
where concept_id in ('SPECIES-5792', 'SPECIES-32087')


select *
FROM OriginalConcepts
where concept_id in ('SPECIES-5792', 'SPECIES-32087');



SELECT *
FROM TaxanomicConcepts
WHERE avibase_id = ''

sanity check for parent child relationships of families to orders
SELECT 
    f.higher_classification,
    f.scientific_name family_name,
    o.scientific_name order_name,
    f.avibase_id,
    'AL25' as version,
    o.avibase_id as parent_id,
    1.0 as fract_weight
FROM TaxanomicConcepts f
JOIN TaxanomicConcepts o ON f.higher_classification = 'Order: ' || o.scientific_name
WHERE f.concept_id LIKE 'FAMILY-%'
  AND o.concept_id LIKE 'ORDER-%'
select *
from ParentChildRelationships
limit 10;

select * 
from AvibaseID aid
join TaxanomicConcepts tc on aid.avibase_id = tc.avibase_id
where tc.concept_id like 'SPECIES-%'
limit 10

-- enable this:
-- select *
-- from OriginalConcepts oc
-- join TaxanomicConcepts tc on oc.concept_id = tc.concept_id
-- where higher_classification = 'Galliformes'
-- limit 10;
*/