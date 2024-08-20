import time
from datetime import datetime

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

import canvasapi
import os
from canvasapi import Canvas
import json
import requests

from os.path import dirname, abspath

# Json parsing for prefs:
pathToPrefs = dirname(abspath(__file__)) + "/UserPreferences.json"

with (open(pathToPrefs, "r") as userPrefsFile):
	preferences = userPrefsFile.read()

parsed_json = json.loads(preferences)

profile = 1
while profile == 0:
	userInput = input(f"-> {Fore.LIGHTGREEN_EX}Enter profile (1 through 3): {Style.RESET_ALL}")
	try:
		int(userInput)
		if 0 < int(userInput) < 4:
			profile = int(userInput)

			if parsed_json.get(f"profile{profile}").get("notion_token") == "<TOKEN>":
				print(
					f"-- {Fore.LIGHTRED_EX}Invalid profile! Choose another or check Notion token is correct in UserPreferences.json{Style.RESET_ALL}")
				profile = 0

			if parsed_json.get(f"profile{profile}").get("notion_database_ID") == "<DATABASE_ID>":
				print(
					f"-- {Fore.LIGHTRED_EX}Invalid profile! Choose another or check Notion database ID is correct in UserPreferences.json{Style.RESET_ALL}")
				profile = 0

			if parsed_json.get(f"profile{profile}").get("canvas_key") == "<KEY>":
				print(
					f"-- {Fore.LIGHTRED_EX}Invalid profile! Choose another or check Canvas key is correct in UserPreferences.json{Style.RESET_ALL}")
				profile = 0

			if parsed_json.get(f"profile{profile}").get("canvas_URL") == "<URL>":
				print(
					f"-- {Fore.LIGHTRED_EX}Invalid profile! Choose another or check Canvas URL is correct in UserPreferences.json{Style.RESET_ALL}")
				profile = 0
		else:
			print(f"-- {Fore.LIGHTRED_EX}Out of range!{Style.RESET_ALL}")
	except:
		print(f"-- {Fore.LIGHTRED_EX}Not a number!{Style.RESET_ALL}")

# Notion token
token = parsed_json.get(f"profile{profile}").get("notion_token")
# Notion database ID
database_id = parsed_json.get(f"profile{profile}").get("notion_database_ID")

# Canvas API URL
API_URL = parsed_json.get(f"profile{profile}").get("canvas_URL")
# Canvas API key
API_KEY = parsed_json.get(f"profile{profile}").get("canvas_key")

currentMonth = datetime.now().month
currentYear = datetime.now().year

startTime = time.time()


# Notion:
def mapNotionResultToData(result):
	# you can print result here and check the format of the answer.
	# print(result)
	data_id = result['id']
	properties = result['properties']
	className = properties['Class']['rich_text'][0]['text']['content']
	name = properties['Name']['title'][0]['text']['content']
	date = properties['Date']['date']['start']
	completed = properties['Completed']['checkbox']
	auto_update = properties['AutoUpdate']['checkbox']
	points = properties['Points']['number']

	return {
		'class': className,
		'name': name,
		'date': date,
		'completed': completed,
		'data_id': data_id,
		'auto_update': auto_update,
		'points': points
	}


def getData():
	url = f'https://api.notion.com/v1/databases/{database_id}/query'

	r = requests.post(url, headers={
		"Authorization": f"Bearer {token}",
		"Notion-Version": "2021-08-16"
	})

	result_dict = r.json()
	data_list_result = result_dict['results']

	dataSet = []

	for data in data_list_result:
		data_dict = mapNotionResultToData(data)
		dataSet.append(data_dict)

	return dataSet


def createData(name, className, date, points, completed=False, auto_update=True):
	url = f'https://api.notion.com/v1/pages'

	payload = {
		"parent": {
			"database_id": database_id
		},
		"properties": {
			"Name": {
				"type": "title",
				"title": [
					{
						"text": {
							"content": name
						},
						"annotations": {
							"color": "pink"
						}
					}
				]
			},
			"Class": {
				"type": "rich_text",
				"rich_text": [
					{
						"text": {
							"content": className
						}
					}
				]
			},
			"Date": {
				"type": "date",
				"date":
					{
						"start": date
					}
			},
			"Completed": {
				"checkbox": completed
			},
			"AutoUpdate": {
				"checkbox": auto_update
			},
			"Points": {
				"number": points
			}
		}}

	r = requests.post(url, headers={
		"Authorization": f"Bearer {token}",
		"Notion-Version": "2021-08-16",
		"Content-Type": "application/json"
	}, data=json.dumps(payload))

	data = mapNotionResultToData(r.json())
	return data


def deleteData(dataId):
	url = f'https://api.notion.com/v1/pages/{dataId}'

	payload = {
		"archived": True
	}

	r = requests.patch(url, headers={
		"Authorization": f"Bearer {token}",
		"Notion-Version": "2021-08-16",
		"Content-Type": "application/json"
	}, data=json.dumps(payload))


def updateData(dataId, data):
	url = f'https://api.notion.com/v1/pages/{dataId}'

	payload = {
		"properties": {
			"Name": {
				"title": [
					{
						"text": {
							"content": data['name']
						}
					}
				]
			},
			"Class": {
				"rich_text": [
					{
						"text": {
							"content": data['class']
						}
					}
				]
			},
			"Date": {
				"type": "date",
				"date":
					{
						"start": data['date']
					}
			},
			"Completed": {
				"checkbox": data['completed']
			},
			"AutoUpdate": {
				"checkbox": data['auto_update']
			},
			"Points": {
				"number": data['points']
			}
		}}

	r = requests.patch(url, headers={
		"Authorization": f"Bearer {token}",
		"Notion-Version": "2021-08-16",
		"Content-Type": "application/json"
	}, data=json.dumps(payload))

	data = mapNotionResultToData(r.json())
	return data


# View data:

dataSet = getData()
# json.dumps is used to pretty print a dictionary
# print(f'-> {Fore.BLUE}Assignment list:{Style.RESET_ALL}', json.dumps(dataSet, indent=2))

'''
for assignment in dataSet:
	if list(assignment.values())[5]:
		print(f"-> {Fore.LIGHTRED_EX}Deleting:{Style.RESET_ALL} {list(assignment.values())[1]}")
		deleteData(list(assignment.values())[4])
'''

# Update data:
'''
updatedMovie = updateMovie('5aec7b23-55ad-4cd9-9fd3-6b827ede0c31', {
	'name': 'UpdatedMovie1',
	'className': 'UpdatedClass1',
	'completed': True
})
print('Update data', json.dumps(updatedMovie, indent=2))
'''

# Canvas:
'''
Assignment attributes:
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_requester', 'allowed_attempts', 'annotatable_attachment_id', 'anonymize_students', 'anonymous_grading', 'anonymous_instructor_annotations', 'anonymous_peer_reviews', 'assignment_group_id', 'automatic_peer_reviews', 'bucket', 'can_duplicate', 'course_id', 'create_override', 'created_at', 'created_at_date', 'delete', 'description', 'due_at', 'due_at_date', 'due_date_required', 'edit', 'final_grader_id', 'get_grade_change_events', 'get_gradeable_students', 'get_override', 'get_overrides', 'get_peer_reviews', 'get_provisional_grades_status', 'get_students_selected_for_moderation', 'get_submission', 'get_submissions', 'grade_group_students_individually', 'graded_submissions_exist', 'grader_comments_visible_to_graders', 'grader_count', 'grader_names_visible_to_final_grader', 'graders_anonymous_to_graders', 'grading_standard_id', 'grading_type', 'group_category_id', 'has_submitted_submissions', 'hide_in_gradebook', 'html_url', 'id', 'important_dates', 'in_closed_grading_period', 'intra_group_peer_reviews', 'is_quiz_assignment', 'lock_at', 'locked_for_user', 'lti_context_id', 'max_name_length', 'moderated_grading', 'muted', 'name', 'omit_from_final_grade', 'only_visible_to_overrides', 'original_assignment_id', 'original_assignment_name', 'original_course_id', 'original_lti_resource_link_id', 'original_quiz_id', 'peer_reviews', 'points_possible', 'position', 'post_manually', 'post_to_sis', 'publish_provisional_grades', 'published', 'require_lockdown_browser', 'restrict_quantitative_data', 'secure_params', 'select_students_for_moderation', 'selected_provisional_grade', 'set_attributes', 'set_extensions', 'show_provisonal_grades_for_student', 'submission_types', 'submissions_bulk_update', 'submissions_download_url', 'submit', 'turnitin_enabled', 'turnitin_settings', 'unlock_at', 'updated_at', 'updated_at_date', 'upload_to_submission', 'workflow_state']
'''

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

courseIDs = []
courses = []

print(f"-- {Fore.LIGHTGREEN_EX}Getting courses...{Style.RESET_ALL}")

for loopedCourse in canvas.get_courses():
	courseID = int(loopedCourse.id)
	try:
		print(f"-> {Fore.CYAN}Got course: {Style.RESET_ALL}" + canvas.get_course(courseID).name)
		courses.append([canvas.get_course(courseID).name, canvas.get_course(courseID)])
		courseIDs.append(courseID)
	except:
		var = 0
# print(f"-- {Fore.YELLOW}Invalid course!{Style.RESET_ALL}")

notionData = getData()

print(f"-- {Fore.LIGHTGREEN_EX}Getting assignments...{Style.RESET_ALL}")

for course in courses:
	print(f"-- {Fore.BLUE}" + course[0] + f"{Style.RESET_ALL}")
	totalCoursePoints = 0

	for assignment in course[1].get_assignments(
			bucket="unsubmitted"):  # Bucket types: past, overdue, undated, ungraded, unsubmitted, upcoming, future
		assignmentName = assignment.name
		assignmentClass = course[0]
		assignmentDate = "2026-01-01T05:59:59Z"
		assignmentCompleted = False
		assignmentUpdate = True
		assignmentPoints = 0

		if hasattr(assignment, "due_at"):
			if assignment.due_at is not None:
				assignmentDate = assignment.due_at
			else:
				print(f"-- {Fore.LIGHTYELLOW_EX}No due date for {Style.RESET_ALL}" + assignmentName + "!")
		else:
			print(f"-- {Fore.YELLOW}No due date for {Style.RESET_ALL}" + assignmentName + "!")

		if hasattr(assignment, "points_possible"):
			assignmentPoints = int(assignment.points_possible)
			totalCoursePoints += assignmentPoints
		else:
			print(f"-- {Fore.LIGHTRED_EX}No points for {Style.RESET_ALL}" + assignmentName + "!")

		# Attempt to create the assignment, if it fails, warn but continue:
		try:
			# print(str(assignmentDate)[5:7])
			# print(str(assignmentDate)[0:4])
			# print(str(assignmentDate)[8:10])
			if int(str(assignmentDate)[0:4]) == int(currentYear) and int(str(assignmentDate)[5:7]) >= int(
					currentMonth) or int(str(assignmentDate)[0:4]) > int(currentYear):
				created = False
				for data in notionData:
					# print(f"Notion name: {list(data.values())[1]}, Canvas name: {assignmentName}")
					if list(data.values())[1] == assignmentName:
						# print(list(data.values()))
						# print(f"Notion points: {list(data.values())[6]}, Canvas points: {assignmentPoints}; Notion date: {str(list(data.values())[2])[0:16]}, Canvas date: {str(assignmentDate)[0:16]}")

						# print(list(data.values())[5])
						created = True
						if (((
								str(list(data.values())[2])[0:16] != str(assignmentDate)[0:16] or
								list(data.values())[6] != assignmentPoints)) and
								list(data.values())[5] == True):
							updateData(list(data.values())[4], {
								"name": assignmentName,
								"class": assignmentClass,
								"date": assignmentDate,
								"completed": assignmentCompleted,
								"auto_update": assignmentUpdate,
								"points": assignmentPoints
							})
							print(f"-> {Fore.CYAN}Updating assignment: {Style.RESET_ALL}" + assignmentName)
						else:
							print(f"-> Assignment up to date: {Style.RESET_ALL}" + assignmentName)

						break

				if created == False:
					# createdAssignment = createData(assignment.name, course[0], str(assignment.due_at)[0:10], False, True)
					print(f"-> {Fore.LIGHTGREEN_EX}Creating assignment: {Style.RESET_ALL}" + assignmentName)
					createdAssignment = createData(assignmentName, assignmentClass, assignmentDate, assignmentPoints,
					                               False, True)
		except:
			print(f"-> {Fore.LIGHTRED_EX}Failed to create{Style.RESET_ALL} {assignmentName}!")
	print(f"-> {Fore.LIGHTGREEN_EX}Total course points: {Style.RESET_ALL}" + str(totalCoursePoints))

# due_at_date: 2023-10-07 05:59:59+00:00
# due_at: 2023-10-07T05:59:59Z

print(f"-> {Fore.LIGHTGREEN_EX}Process finished in {time.time() - startTime} seconds")
