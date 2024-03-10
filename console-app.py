from datetime import datetime
import urllib.request
import json


url = "http://localhost:30000/drivers-licenses/list"


def write_to_excel(filename, licenses):
	with open(filename, 'w') as my_file:
		my_file.write("id,nume,prenume,categorie,data_de_emitere,data_de_expirare,suspedat\n")
		for license_object in licenses:
			my_file.write(f"{license_object.get('id')},{license_object.get('nume')},{license_object.get('prenume')},{license_object.get('categorie')},{license_object.get('data_de_emitere')},{license_object.get('data_de_expirare')},{license_object.get('suspedat')}\n")


def write_to_excel2(filename, licenses):
	with open(filename, 'w') as my_file:
		my_file.write("categorie,total\n")
		for category, count in licenses.items():
			my_file.write(f"{category},{count}\n")
   

def get_all_licenses():
	try:
		with urllib.request.urlopen(url) as response:
			if response.status == 200:
				data = response.read().decode('utf-8')
				return json.loads(data)
			else:
				print("Failed to fetch data. Status code:", response.status)
	except Exception as e:
		print("An error occurred:", str(e))


def get_suspended_licenses(licenses):
	return [license_object for license_object in licenses if license_object.get('suspendat')]


def get_valid_licenses(licenses):
	today = datetime.now()
	return [license for license in licenses if not license.get('suspendat') and datetime.strptime(license.get('dataDeExpirare'), "%d/%m/%Y") >= today]


def get_category_licenses(licenses):
	license_counts = {}
	for license in licenses:
		category = license.get('categorie')
		if category in license_counts:
			license_counts[category] += 1
		else:
			license_counts[category] = 1
	return license_counts

    
if __name__ == "__main__":
	all_licenses = get_all_licenses()
 
	while True:
		print("\nChoose an operation:")
		print("1. Print all licenses")
		print("2. Print suspended licenses")
		print("3. Print valid licenses")
		print("4. Print category by licenses")
		print("Type 'exit' to quit")
		choice = input("Enter your choice: ")
		if choice == '1':
			write_to_excel("all_licenses.csv", all_licenses)
		elif choice == '2':
			suspended_licenses = get_suspended_licenses(all_licenses)
			write_to_excel("suspended_licenses.csv", suspended_licenses)
		elif choice == '3':
			valid_licenses = get_valid_licenses(all_licenses)
			write_to_excel("valid_licenses.csv", valid_licenses)
		elif choice == '4':
			category_licenses = get_category_licenses(all_licenses)
			write_to_excel2("category_licenses.csv", category_licenses)
		elif choice.lower() == 'exit':
			break
		else:
			print("Invalid choice. Please enter a number between 1 and 4.")
