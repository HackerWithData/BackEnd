DELETE FROM django_migrations where app = 'contracotrs';
/*where app = "contractors";
/*Drop Table django_migrations;

 */

/*SELECT * FROM django_migrations limit 1;
 */

DELETE FROM professionals_professional;

INSERT INTO professionals_professional(lic_num, name, entity_type, state, postal_code,type)
    SELECT lic_num, bus_name, entity, state, pos_code,lic_type
    FROM contractors_contractor where lic_status ='Cuurent and Active' or lic_expire_date>'2016-09-16';

INSERT INTO professionals_professional(lic_num, name, entity_type, state, postal_code)
    SELECT lic_num, bus_name, entity, state, pos_code
    FROM contractors_contractor where lic_status ='Cuurent and Active' or lic_expire_date>'2017-09-16';