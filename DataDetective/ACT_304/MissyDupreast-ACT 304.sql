#Missy Dupreast - Capstone Project

#ACT 304
SELECT p.name AS person_name, l.location_name
FROM persons p
JOIN events e ON p.person_id = e.person_id
JOIN locations l ON e.location_id = l.location_id
WHERE p.status = 'missing';

/* Output: 
person_name, location_name
Jane Smith, Street
Bruce Banner,	Home
*/
