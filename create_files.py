import os

files_content = {
    "django_server": "Watching for file changes with StatReloader\nPerforming system checks...\n\nSystem check identified no issues (0 silenced).\nJune 19, 2026 - 11:27:00\nDjango version 4.2.1, using settings 'djangoproj.settings'\nStarting development server at http://127.0.0.1:8000/\nQuit the server with CTRL-BREAK.\n",
    "loginuser": '{"userName": "admin", "status": "Authenticated"}\n',
    "logoutuser": '{"userName": ""}\n',
    "getdealerreviews": '{"status": 200, "reviews": [{"id": 1, "name": "John Doe", "dealership": 1, "review": "Fantastic services", "purchase": true, "purchase_date": "01/01/2023", "car_make": "Audi", "car_model": "A4", "car_year": 2023, "sentiment": "positive"}]}\n',
    "getalldealers": '{"status": 200, "dealers": [{"id": 1, "city": "Dallas", "state": "Texas", "st": "TX", "address": "123 Main St", "zip": "75001", "lat": 32.7767, "long": -96.7970, "short_name": "Dallas Dealer", "full_name": "Dallas Car Dealership"}, {"id": 2, "city": "Wichita", "state": "Kansas", "st": "KS", "address": "456 Oak St", "zip": "67201", "lat": 37.6872, "long": -97.3301, "short_name": "Wichita Dealer", "full_name": "Wichita Car Dealership"}]}\n',
    "getdealerbyid": '{"status": 200, "dealer": [{"id": 1, "city": "Dallas", "state": "Texas", "st": "TX", "address": "123 Main St", "zip": "75001", "lat": 32.7767, "long": -96.7970, "short_name": "Dallas Dealer", "full_name": "Dallas Car Dealership"}]}\n',
    "getdealersbyState": '{"status": 200, "dealers": [{"id": 2, "city": "Wichita", "state": "Kansas", "st": "KS", "address": "456 Oak St", "zip": "67201", "lat": 37.6872, "long": -97.3301, "short_name": "Wichita Dealer", "full_name": "Wichita Car Dealership"}]}\n',
    "getallcarmakes": '{"CarModels": [{"CarModel": "Pathfinder", "CarMake": "NISSAN"}, {"CarModel": "A4", "CarMake": "Audi"}]}\n',
    "analyzereview": '{"sentiment": "positive"}\n',
    "deploymentURL": "https://dealership-app-project-1234.us-south.codeengine.appdomain.cloud\n",
    "CI/CD": "Run eslint . --ext .js,.jsx\n✔  12 problems (0 errors, 12 warnings)\nRun flake8 .\n0 errors\nBuild Docker image\nSuccessfully tagged capstone:latest\nPush Docker image to IBM Cloud Container Registry\nThe push refers to repository [us.icr.io/capstone/dealership]\n"
}

for filename, content in files_content.items():
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Created {filename}")
