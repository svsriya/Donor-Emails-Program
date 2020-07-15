from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import xlrd
import smtplib

# email login info
your_email = 'savmaplz@pseudo.org'

# open the excel file
excel_loc = "/Users/svsriya/Documents/PythonPrograms/EmailProgram/Practice.xlsx"

class Person:

	numEmails = 0
	# this makes it easier to handle people's names who appear multiple times on the excel
	def __init__( self, email, causes ):
		self.email = email
		self.causes = []

	def add_cause( self, cause ):
		self.causes.append( cause )

	def __repr__( self ):
		return 'email: ' + self.email + ', causes: ' + str( self.causes )

	def __str__( self ):
		return self.__repr__()


def create_donor_list( file_loc ):

	# variables taken from the excel sheet
	workbook = xlrd.open_workbook( file_loc )
	sheet = workbook.sheet_by_index( 0 )

	num_rows = sheet.nrows
	num_cols = sheet.ncols
	people_dict = dict()

	for row in range ( 1, num_rows ):
		name = sheet.cell_value( row, 0 )
		cause = sheet.cell_value( row, 1 )
		email = sheet.cell_value( row, 2 )

		if name in people_dict.keys():
			if cause in people_dict[name].causes:
				continue
			else:
				people_dict[name].add_cause( cause )

		elif email.strip():
			causes_list = []
			new_entry = Person( email, causes_list )
			new_entry.add_cause( cause )
			people_dict[name] = new_entry

	return people_dict

def custom_ty_note( name, causes_list ):

	thankyou_note = """O:m Asmad Gurubhyo:namaha!                                                                      Sri:mathe:Ra:ma:nuja:yanamaha!

Jai Srimannarayana!

Dear Sriman / Smt. """ + name + """,

\tThank you for your generous donations and support in our service activities! His Holiness Sri Chinna Jeeyar Swamiji offers His Mangala:sa:sanam to you and your family. You have donated to the cause(s) below:\n"""

	for i in range( len(causes_list)):
		thankyou_note += "\n\t\t" + causes_list[i]

	thankyou_note += """\n\n\tYour donations are being put to good use. These activities have been successfully growing with the support of philanthropists like you. Construction of the current mega project, the Statue of Equality, has been progressing very well. His Holiness invites you and your family to participate in the upcoming inauguration function, tentatively in February 2019.

	Want to know how your contributions made a difference in the community?
	Here are the annual highlights of 2017 on all our activities:
	\thttps://chinnajeeyar.guru/chinnajeeyar/wp-content/uploads/2018/03/2017-Highlights.pdf
	
	We would love to hear back from you! Please provide us with your valuable feedback here:
	\thttps://docs.google.com/forms/d/e/1FAIpQLScX0RQKV9JsxXWBcPuq0XXdIlVi5rMon2k213XrRj8QSTNljw/viewform?usp=sf_link

	Please contact me for any questions.

	With Gratitude,
	In service of His Holiness' Devotees
	Padma Vudata, DRO (Donors Relation Officer)
	
	Contact info:
	Email: DRO@chinnajeeyar.guru
	Phone Number: 203-564-0279
	
	https://www.statueofequality.org                                                                                                         
	https://chinnajeeyar.guru
	
	Jai Srimannarayana!"""

	return thankyou_note


def send_email( to_email, from_email, password, body ):

	# create message object instance
	msg = MIMEMultipart()

	# parameters of message
	msg['From'] = "His Holiness Chinna Jeeyar - Donor Relations Officer <dro@chinnajeeyar.guru>"
	msg['To'] = to_email
	msg['Subject'] = "Thank You for Your Support - Your Contributions are Valued "

	# add in the html message body
	msg.attach(MIMEText(body, 'plain'))

	# server for whatever email platform 
	mail = smtplib.SMTP( 'smtp.gmail.com:587' )
	mail.ehlo()
	mail.starttls()

	# login credentials
	mail.login( from_email, password )

	# send message via server
	mail.sendmail( from_email, msg['To'], msg.as_string() )

	mail.close()

	return "email sent to %s" % msg['To']

def main():

	# create list of donors
	data = create_donor_list( excel_loc ) 	

	# cycles through each row in the spreadsheet to get necessary info for email and sends email to each donor
	
	for key in data:
		name = key
		email = data[key].email
		causes_list = data[key].causes

		email_body = custom_ty_note( name, causes_list )
		# print email_body + "\n"
		print send_email( email, your_email, temp_pwd, email_body )
		######
		Person.numEmails += 1
		print "Number of emails sent: " + str(Person.numEmails)
		if Person.numEmails == 3:
			print "\nToday's limit has been reached. Take some rest mom!!!\n"
			break
		######

if __name__ == '__main__':
	 main()		

