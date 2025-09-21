-- select * 
-- from AvibaseID aid
-- join TaxanomicConcepts tc on aid.avibase_id = tc.avibase_id
-- limit 10;

select *
from OriginalConcepts oc
join TaxanomicConcepts tc on oc.concept_id = tc.concept_id
limit 10;