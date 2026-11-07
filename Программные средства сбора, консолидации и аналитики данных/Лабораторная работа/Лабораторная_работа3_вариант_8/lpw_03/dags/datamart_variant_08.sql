CREATE OR REPLACE VIEW student_datamart AS
SELECT row_id, school,
 studytime AS study_time_order,
 CASE studytime WHEN 1 THEN '1. Less than 2 h' WHEN 2 THEN '2. 2 to 5 h'
 WHEN 3 THEN '3. 5 to 10 h' WHEN 4 THEN '4. More than 10 h' END AS study_time_group,
 absences,
 GREATEST(medu, fedu) AS parent_education_order,
 CASE GREATEST(medu, fedu) WHEN 0 THEN '0. None' WHEN 1 THEN '1. Primary (4th grade)'
 WHEN 2 THEN '2. Grades 5 to 9' WHEN 3 THEN '3. Secondary' WHEN 4 THEN '4. Higher' END AS parent_education_level,
 g3 AS final_grade
FROM stg_students;
