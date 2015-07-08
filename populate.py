


def get_groups() :
	#groups = ['Cholera','Typhoid','Priyanshomania','Loveria','Sadness','Distance','Apology']
	groups = ['Allergies', 'Arthritis' , 'Respiratory Diseases' , 'Cancer']
	return groups

#conditions

def get_conditions():

	conditions = [('Anaphylaxis', 'Allergies', 'MiscDetails'),
				  ('Chronic Rhinitis', 'Allergies', 'MiscDetails'),
				  ('Cold / Flu', 'Allergies', 'MiscDetails'),
				  ('Food Allergy', 'Allergies','MiscDetails'),
				  ('Hives', 'Allergies' , 'MiscDetails'),
				  ('Latex Allergy', 'Allergies', 'MiscDetails'),
				  ('Dementia', 'Alzheimer' , 'MiscDetails'),
				  ('Ostearthiritis', 'Arthritis' , 'MiscDetails'),
				  ('Rheumatoid arthritis', 'Arthritis' , 'MiscDetails'),
				  ('Lupus' , 'Arthritis' , 'MiscDetails'),
				  ('Gout' , 'Arthritis'  , 'MiscDetails'),
				  ('Asthma' , 'Respiratory Diseases' , 'MiscDetails'),
				  ('Cystic Fibrosis', 'Respiratory Diseases', 'MiscDetails'),
				  ('Emphysema', 'Respiratory Diseases', 'MiscDetails'),
				  ('Chronic Obstructive Pulmonary Disorder' , 'Respiratory Diseases' , 'MiscDetails'),
				  ('Sinusitis' , 'Respiratory Diseases', 'MiscDetails'),
				  ('Tonsillitis', 'Respiratory Diseases' , 'MiscDetails'),
				  ('Otitis Madia' , 'Respiratory Diseases', 'MiscDetails'),
				  ('Laryngitis', 'Respiratory Diseases', 'MiscDetails'),
				  ('Pneumonia', 'Respiratory Diseases', 'MiscDetails'),
				  ('Tuberculosis' , 'Respiratory Diseases', 'MiscDetails'),
				  ('Bladder Cancer' , 'Cancer' ,'MiscDetails'),
				  ('Breast Cancer', 'Cancer', 'MiscDetails'),
				  ('Lung Cancer' , 'Cancer' , 'MiscDetails'),
				  ('Skin Cancer' , 'Cancer' , 'MiscDetails'),
				  ('Leukemia' , 'Cancer', 'MiscDetails')]
#treatments

	return conditions

def get_treatments_group():

	treatments_groups = ['Prescription Drugs', 'OTC Drugs' , 'Physical therapy']
	return treatments_groups


def get_treatments():

	treatments = [('Hydrocodone' , 'Prescription Drugs' , 'MiscDetails'),
				  ('Generic Zocor', 'Prescription Drugs' , 'MiscDetails'),
				  ('Lisinopril', 'Prescription Drugs' , 'MiscDetails'),
				  ('Azithromycin', 'Prescription Drugs' , 'MiscDetails'),
				  ('Amoxicillin' , 'Prescription Drugs' , 'MiscDetails')]

	return treatments