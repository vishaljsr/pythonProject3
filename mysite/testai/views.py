import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from robot import run_cli
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@csrf_exempt
def execute_test(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body)
            tests = data.get('tests', [])

            # Prepare to store the results
            results = []

            for test in tests:
                title = test.get('title', 'Unnamed Test')
                steps = test.get('steps', [])

                # Create the test content
                test_content = f"*** Settings ***\nLibrary     SeleniumLibrary\n\n"
                test_content += f"*** Test Cases ***\n{title}\n"
                test_content += "    [Documentation]    Open Google homepage in Chrome browser\n"
                test_content += f"    Open Browser    {steps[1].split('=')[1].strip()}    chrome\n"
                test_content += "    Maximize Browser Window\n"

                # Write the test to a temporary file
                with open('temp_test.robot', 'w') as file:
                    file.write(test_content)

                # Execute the test and capture the output
                result = run_cli(['temp_test.robot'], exit=False)
               # results.append({'title': title, 'result': result})

            # Return the test results
            return JsonResponse({'status': 'success', 'results': results})

        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    else:
        # If it's not a POST request, just say the endpoint is live
        return JsonResponse({'status': 'success', 'message': 'API endpoint is live!'})
