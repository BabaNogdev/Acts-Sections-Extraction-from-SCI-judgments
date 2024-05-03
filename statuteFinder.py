import pandas as pd
import re
import csv
import matplotlib.pyplot as plt

# Import data
path = "C:/Users/Anurag/Documents/Datasets/ILDC Dataset/ILDC_single.csv"

# Convert it into a Pandas dataframe
data = pd.read_csv(path)
judgments = []

# Extracting judgment text
for t in data['text']:
	# print(t, end="\n---------------------------------\n")
	judgments.append(t)

print("Total number of judgments:", len(judgments))

# Function to find the Acts in the judgment text which are followed by the year of their enactment
def findActWithYear(text, l):
	# print(text, end="\n----------------------------\n")

	tempList = []
	act = ""
	acts = set()

	# To check whether the word "Act" exists within the text
	if re.search(r"\bAct\b", text):
		for match in re.finditer("Act", text):
			tempList.append(text[match.start()-l:match.end()+6]) # Storing the l characters preceding "Act" and 6 characters succeeding "Act"

		# print(tempList)
		pattern = re.compile(r'\d{4}$') # To check for the existence of a 4-digit number at the end of the string in tempList[i]

		for s in tempList:
			if pattern.findall(s):
				firstCap = re.finditer('[A-Z][a-z]{1,30}[^(A-Za-z)]', s) # Getting the first word starting with a capital letter

				for m in firstCap:
					act = s[m.start():]
					acts.add(act)
					break

	# print(acts)
	# Send the set of acts for post-processing and return a list of post-processed acts
	return postProcessing(acts)

# Function to find the Acts in the judgment text which are not followed by the year of their enactment
def findActWithoutYear(text, l):
	# print(text, end="\n----------------------------\n")

	tempList = []
	act = ""
	acts = set()

	# To check whether the word "Act" exists within the text
	if re.search(r"\bAct\b", text):
		for match in re.finditer("Act", text):
			tempList.append(text[match.start()-l:match.end()]) # Storing the l characters preceding "Act" and 6 characters succeeding "Act"

		# print(tempList)
		
		for s in tempList:
			firstCap = re.finditer('[A-Z][a-z]{1,30}[^(A-Za-z)]', s) # Getting the first word starting with a capital letter

			for m in firstCap:
				act = s[m.start():]
				acts.add(act)
				break

	# print(acts)
	# Send the set of acts for post-processing and return a list of post-processed acts
	return postProcessing(acts)

# Function for post-processing the acts
def postProcessing(acts):
	actsList = list(acts)
	popSet = set()
	popList = []
	t = dict()

	# Removes periods, and spurious commas and spaces
	for i, act in enumerate(actsList):
		actsList[i] = act.replace(".", "")
		actsList[i] = act.replace(" , ", "")
		actsList[i] = act.replace("  ", " ")
		# print(act)
		# actsList[i] = act
		# print(actsList[i])

	# Check for repetition of an act in the list by finding whether one list item is a substring of another or not
	if len(actsList) > 1:
		for i in range(len(actsList)):
			for j in range(len(actsList)):
				if i == j:
					continue

				if actsList[j][-4:] == actsList[i][-4:]: # Matching years enactment of acts
					# print(actsList[i], "||", actsList[j])
					if actsList[j][3:] in actsList[i]:
						# print(j, actsList[j])
						popSet.add(j)

					elif actsList[i][3:] in actsList[j]:
						# print(i, actsList[i])
						popSet.add(i)

	# print(popSet)
	popList = sorted(popSet, reverse=True)
	# print(popList)

	for i in popList:
		actsList.pop(i)

	# Return a list of post-processed acts
	return actsList

# Function to find the Acts which do not follow the standard of writing in the judgment text
def findact(text, l):
	# print(text, end="\n----------------------------\n")

	tempList = []
	act = ""
	acts = set()

	# Checking for text not containing the word "Act", but containing the word "act"
	if re.search(r"\bact\b", text):
		for match in re.finditer("act", text):
			tempList.append(text[match.start()-l:match.end()+5])

		# print(tempList)
		pattern = re.compile(r'\d{4}$')

		for s in tempList:
			if pattern.findall(s):
				index = (s.find("the"))

				act = s[index:]
				act = act.replace("\n", " ")
				acts.add(act.title())
				break

			else: # For case text with the Act not being followed by its year of enactment
				firstCap = re.finditer('[A-Z][a-z]{1,30}[^(A-Za-z)]', s)
				
				for m in firstCap:
					act = s[m.start():-6]
					acts.add(act)
					break

	# print(acts)
	# Returns a list of acts
	return list(acts)

# Function to check for the value of Section Code
def findCode(tL):
	IPC = set()
	CrPC = set()
	output = list()

	# First 2 check for IPC, the next 3 check for CrPC
	for s in tL:
		# print(s)
		if "Indian Penal Code" in s:
			temp = re.findall(r'[0-9]+[-][A-Z]|[0-9]+', s)
			for n in temp:
				IPC.add(n)
			# print("Indian Penal Code:", IPC)

		elif "IPC" in s:
			temp = re.findall(r'[0-9]+[-][A-Z]|[0-9]+', s)
			for n in temp:
				IPC.add(n)
			# print("IPC:", IPC)

		elif "Code of Criminal Procedure" in s:
			temp = re.findall(r'[0-9]+[-][A-Z]|[0-9]+', s)
			for n in temp:
				CrPC.add(n)
			# print("Code of Criminal Procedure:", CrPC)

		elif "CrPC" in s:
			temp = re.findall(r'[0-9]+[-][A-Z]|[0-9]+', s)
			for n in temp:
				CrPC.add(n)
			# print("CrPC:", CrPC)

		elif "Cr.P.C." in s:
			temp = re.findall(r'[0-9]+[-][A-Z]|[0-9]+', s)
			for n in temp:
				CrPC.add(n)
			# print("Cr.P.C.:", CrPC)

		elif "C.P.C." in s:
			temp = re.findall(r'[0-9]+[-][A-Z]|[0-9]+', s)
			for n in temp:
				CrPC.add(n)
			# print("C.P.C.:", CrPC)

	# Append IPC and CrPC at 0th and 1st index of a list
	output.append(IPC)
	output.append(CrPC)

	return output

# Function to find the Section of IPC/CrPC
def findSection(text, l):
	tempList = []
	IPC = set()
	CrPC = set()
	section = ""
	sections = set()

	# For case text with the word Section starting with 'S'
	if re.search(r"\bSection\b", text):
		for match in re.finditer("Section", text):
			tempList.append(text[match.start():match.end()+l])

		# print(tempList)

		# To individually search for an IPC Section and a CrPC section
		IPC = findCode(tempList)[0]
		CrPC = findCode(tempList)[1]

	# For case text with the word Section not starting with 'S'
	elif re.search(r"\bsection\b", text):
		for match in re.finditer("section", text):
			tempList.append(text[match.start():match.end()+l])

		# print(tempList)
		IPC = findCode(tempList)[0]
		CrPC = findCode(tempList)[1]

	# print("Final IPC List:", IPC)
	# print("Final CrPC List:", CrPC)

	# Post-processing to make the type of Section clear
	for s in IPC:
		section = "Section " + s + " IPC"
		sections.add(section)

	for s in CrPC:
		section = "Section " + s + " CrPC"
		sections.add(section)

	# print(sections)
	return list(sections)

def plotting(data, name, empty, extraneous, erroneous, flag=0):
	fig, axs = plt.subplots(2, 2, figsize=(30, 20))
	i = 0

	for key, d in data.items():
		ax = axs[i // 2, i % 2]
		i += 1
		
		ax.bar(range(len(d.iloc[:, 0])), d.iloc[:, 1])
		ax.set_xlabel("Case index")
		ax.set_ylabel(f"Number of {name} cited")
		ax.set_title(f"Number of {name} per case for length = {key}")
		ax.set_ylim(0, 30)

		if flag == 0:
			continue

		elif flag == 1:
			errorText = f"Number of extraneous outputs: {len(extraneous[key])}"
			ax.text(0.95, 0.95, errorText, ha='right', va='top', transform=ax.transAxes, fontsize=8, bbox=dict(facecolor='white', alpha=0.5))

		elif flag == 3:
			errorText = f"Number of empty outputs: {len(empty[key])}\nNumber of erroneous outputs: {len(erroneous[key])}\nNumber of extraneous outputs: {len(extraneous[key])}"
			ax.text(0.95, 0.95, errorText, ha='right', va='top', transform=ax.transAxes, fontsize=8, bbox=dict(facecolor='white', alpha=0.5))

	plt.subplots_adjust(left=0.05, right=0.99, bottom=0.1, top=0.95, wspace=0.15, hspace=0.25)
	plt.show()

def extraneousPlot(data, name):
	for key, df in data.items():
		ax = data[key].plot(kind='bar', figsize=(30, 20), color='#1F77B4', zorder=2, width=0.35, legend=False)

		ax.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on", rotation=90)

		vals = ax.get_xticks()
		for tick in vals:
			ax.axvline(x=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

		ax.set_xlabel(f"Number of {name} cited")
		ax.set_ylabel("Case index")
		ax.set_title(f"Case indices with number of {name} greater than 10 for length = {key}")

		plt.subplots_adjust(left=0.05, right=0.99, bottom=0.1, top=0.95, wspace=0.15, hspace=0.25)
		plt.show()

def makeStylishCSV(data, name):
	dataDf = pd.DataFrame()

	for key, dataList in data.items():
		rows = []

		for i, item in enumerate(dataList):
			if item == "Empty":
				rows.append({"Index":i, f"{name} number":"0 of 0", f"{name}":item})

			else:
				for j, s in enumerate(item):
					if j == 0:
						rows.append({"Index":i, f"{name} number":f"{j+1} of {len(item)}", f"{name}":s})
					else:
						rows.append({"Index":"", f"{name} number":f"{j+1} of {len(item)}", f"{name}":s})

		dataDf = pd.DataFrame(rows)
		with open(f'{name}{key}chars.csv', 'w') as file:
			dataDf.to_csv(file, index=False)

# Driver code to initiate procedure and generate final outputs
def main():
	acts = {}
	sections = {}
	charLengths = [30, 45, 60, 75]

	# Function calls to generate output dataframes of Acts and Sections cited in each judgment
	# Sequence followed: findActWithYear() -> findActsWithoutYear() -> findSection() -> findact()
	for l in charLengths:
		actsTemp = []
		sectionsTemp = []
		for j in range(len(judgments)):
			actsTemp.append("Empty")
			sectionsTemp.append("Empty")

		for i in range(0, len(judgments)):
			retVal = []
			# print(i)
			retVal = findActWithYear(judgments[i], l)
			if retVal != []:
				actsTemp[i] = retVal
			else:
				retVal = findActWithoutYear(judgments[i], l)
				if retVal != []:
					actsTemp[i] = retVal
				else:
					actsTemp[i] = "Empty"

			retVal = findSection(judgments[i], l)
			if retVal != []:
				sectionsTemp[i] = retVal
			else:
				sectionsTemp[i] = "Empty"

			if actsTemp[i] == "Empty" and sectionsTemp[i] == "Empty":
				retVal = findact(judgments[i], l)
				if retVal != []:
					actsTemp[i] = retVal
				else:
					actsTemp[i] = "Empty"

			acts[l] = actsTemp
			sections[l] = sectionsTemp

			# if i % 500 == 0:
			# 	print("Acts & Sections from text at index", i, ":", actsTemp, "\n", sectionsTemp, end="\n-----------------\n")
	# print(acts, "\n", sections)

	# Creating separate dictionaries with keys = 30, 45, 60, 75 of dataframes for storing Acts and Sections
	actsDfDict = {}
	sectionsDfDict = {}

	for key, actsList in acts.items():
		rows = []
		tempDf = pd.DataFrame()
		
		for i, l in enumerate(actsList):
			rows.append({"Acts": l})

		tempDf = pd.DataFrame(rows)
		tempDf['Total no. of Acts cited'] = tempDf['Acts'].apply(lambda x: len(x) if x != "Empty" else 0) # Count of acts cited in a judgment
		actsDfDict[key] = tempDf

		with open(f'acts{key}chars.csv', 'w') as f:
			actsDfDict[key].to_csv(f)

	for key, sectionsList in sections.items():
		rows = []
		tempDf = pd.DataFrame()

		for l in sectionsList:
			rows.append({"Sections": l})

		tempDf = pd.DataFrame(rows)
		tempDf['Total no. of Sections cited'] = tempDf['Sections'].apply(lambda x: len(x) if x != "Empty" else 0) # Count of sections cited in a judgment
		sectionsDfDict[key] = tempDf

		with open(f'sections{key}chars.csv', 'w') as f:
			sectionsDfDict[key].to_csv(f)

	# print(actsDfDict, "\n", sectionsDfDict)

	# Finding the average length of an Act per judgment
	actsLength = {}
	for key, df in actsDfDict.items():
		tempDic = {}

		for i, row in df.iterrows():
			tempList = []
			if row[0] == "Empty" or len(row[0]) > 10:
				tempDic[i] = 0
			else:
				tempList = [len(s) for s in row[0]]
				avgLen = sum(tempList) / len(tempList) 
				tempDic[i] = avgLen

		actsLength[key] = tempDic
	# print(actsLength)

	# Joining Acts and Sections dataframes to create the final output
	outputs = {}
	for key in charLengths:
		outputs[key] = pd.concat([actsDfDict[key], sectionsDfDict[key]], axis=1)
	# print(outputs)

	# Count of different kinds of errors that have been observed within the output
	# Storing empty outputs, i.e., indices of judgments in which no Acts and Sections were cited
	empty = [0, 0]
	emptyActs = {}
	emptySections = {}
	for key, output in outputs.items():
		emptyActs[key] = output[(output['Acts'] == "Empty") & (output['Sections'] == "Empty")]
		emptySections[key] = output[(output['Acts'] == "Empty") & (output['Sections'] == "Empty")]
	empty[0] = emptyActs
	empty[1] = emptySections

	# Storing indices of judgments from which only a number was obtained as output
	erroneous = {}
	tempList = []
	for key, output in outputs.items():
		singletons = pd.DataFrame()
		singletons = output[output['Acts'].apply(lambda x: len(x) == 1)]
		tempList = list(zip(singletons.index.tolist(), singletons['Acts'].tolist()))
		err = []
		for s in tempList:
			if s[1][0].isnumeric():
				err.append(s)
		erroneous[key] = pd.DataFrame(err)

	# Storing part of output which had irrelevant content
	extraneous = [0, 0]
	extraneousActs = {}
	extraneousSections = {}
	for key, act in actsDfDict.items():
		extraneousActs[key] = act[act['Total no. of Acts cited'] > 10]
	for key, section in sectionsDfDict.items():
		extraneousSections[key] = section[section['Total no. of Sections cited'] > 10]
	extraneous[0] = extraneousActs
	extraneous[1] = extraneousSections

	# print("Empty outputs:\n", empty)
	# print("Acts with numbers as outputs:\n", erroneous)
	# print("Acts with irrelevant information:\n", extraneous)

	# Graph plotting for number of Acts/Sections cited per case and average length of Acts
	plotting(actsDfDict, "Acts", empty[0], extraneous[0], erroneous, flag = 3)
	plotting(sectionsDfDict, "Sections", empty[1], extraneous[1], erroneous, flag = 1)

	# Graph plotting for cases in which the numbero f Acts/Sections are greater than 10
	extraneousPlot(extraneousActs, "Acts")
	extraneousPlot(extraneousSections, "Sections")

	# Graph plotting for average length of acts per case
	fig, axs = plt.subplots(2, 2, figsize=(12, 8))
	i = 0

	for key, lengthsDict in actsLength.items():
		ax = axs[i//2, i%2]
		i += 1
		x = range(len(lengthsDict))
		y = [aL for key, aL in lengthsDict.items()]
		ax.bar(x, y)
		ax.set_xlabel("Case index")
		ax.set_ylabel("Average length of the Act cited")
		ax.set_title(f"Average length of Acts per case for length = {key}")
		ax.set_ylim(0, 100)

	plt.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.95, wspace=0.15, hspace=0.25)
	plt.show()

	# Preparing the final csv files for acts and sections
	makeStylishCSV(acts, "Acts")
	makeStylishCSV(sections, "Sections")

# Call to the driver function
if __name__ == '__main__':
	main()