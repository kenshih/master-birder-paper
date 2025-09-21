select * 
from AvibaseID aid
join TaxanomicConcepts tc on aid.avibase_id = tc.avibase_id
where tc.concept_id like 'SPECIES-%'
limit 10
/*
-- enable this:
-- select *
-- from OriginalConcepts oc
-- join TaxanomicConcepts tc on oc.concept_id = tc.concept_id
-- where higher_classification = 'Galliformes'
-- limit 10;
*/