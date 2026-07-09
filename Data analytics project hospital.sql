
use Hospitaldb;
/* View the Data*/
select top 10 * from healthcare_dataset;

/*Count Total Patients*/
 select count(*) as total_patients
 from healthcare_dataset;

 /* find Unique medical conditions*/

 select distinct medical_condition
 from healthcare_dataset;
 
 /* Counts Patients by gender*/

 select gender,count(*) as total_patients
 from healthcare_dataset group by gender;

 /* Average Age*/

 select avg(age) as average_age
 from healthcare_dataset;

 /* Youngest patient*/
 select min(age) as young_age
 from healthcare_dataset;

 /* Oldest Patient*/

  select max(age) as old_age
  from healthcare_dataset;

  /* total billing amount*/ 
  select sum(billing_amount) as total_billing
  from healthcare_dataset;


  /* Average billing amount*/
  select avg(billing_amount) as avg_billing
  from healthcare_dataset;

  /* min billing amount*/
  select min(billing_amount) as min_billing
  from healthcare_dataset;

  /* Highest billing amount*/
  select max(billing_amount) as max_billing
  from healthcare_dataset;

  /* Top 10 Hospitals*/
  select top 10 hospital 
  from healthcare_dataset;
  
  /* top 10 doctors*/
  select top 10 doctor
  from healthcare_dataset;
  
  /* number of patients treated by each doctor*/

  select doctor,count(*) as Total_patients
  from healthcare_dataset group by doctor
  order by Total_patients desc;

  /* number of patients in each hospital*/

  select hospital, count(*) as total_patients
  from healthcare_dataset group by Hospital
  order by total_patients desc;
  
  /* medication usage count*/

  select medication,count(*) as total
  from healthcare_dataset group by medication;

  /* test result distribution*/

  select test_results,count(*) as total_results
  from healthcare_dataset group by Test_Results;


  /* monthly admissions*/

  select month(date_of_admission) as month,
  count(*) as total_admissions from
  healthcare_dataset group by(Date_of_Admission)
  order by month;

  /* yearly admissions*/

  select year(date_of_admission) as year,
  count(*) as total from healthcare_dataset
  group by(Date_of_Admission) order by year;

  /* top 5 hospitals by billind*/

  select top 5 hospital, sum(billing_amount) as total_billing
  from healthcare_dataset group by Hospital
  order by total_billing desc;

  /* top 5 doctors by patient count*/

  select top 5 doctor,count(*) as patient 
  from healthcare_dataset group by doctor
  order by patient;

  /* female patients with diabetes*/

  select name,age from healthcare_dataset
  where gender='female' and medical_condition='diabetes';

  /* emergency admissions*/

  select * from healthcare_dataset 
  where Admission_Type='emergency';

  /* patients whose billing is above average*/

  select name, billing_amount from healthcare_dataset
  where Billing_Amount > ( select avg(billing_amount)
  from healthcare_dataset);
