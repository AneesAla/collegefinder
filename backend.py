import requests
import json

def search_school(api_key, page=0):
    base_url = 'https://api.data.gov/ed/collegescorecard/v1/'
    endpoint = 'schools'

    params = {
        'api_key': api_key,
        'page': page,
    }

    response = requests.get(f'{base_url}{endpoint}', params=params)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results')

        if results:
            all_schools_data = []

            for result in results:
                school_data = {}

                location_info = result.get('location')
                if location_info:
                    school_data['latitude'] = location_info.get('lat')
                    school_data['longitude'] = location_info.get('lon')

                latest_info = result.get('latest')
                if latest_info:
                    school_info = latest_info.get('school')
                    if school_info:
                        school_data['name'] = school_info.get('name')
                        school_data['zip_code'] = school_info.get('zip')
                        school_data['city'] = school_info.get('city')
                        school_data['state'] = school_info.get('state')
                        school_data['address'] = school_info.get('address')
                        school_data['school_url'] = school_info.get('school_url')
                        school_data['online_only'] = 'Yes' if school_info.get('online_only') == 1 else 'No'

                        cost_info = latest_info.get('cost')
                        if cost_info:
                            school_data['book_supply_cost'] = cost_info.get('booksupply')
                            school_data['in_state_tuition'] = cost_info.get('tuition', {}).get('in_state')
                            school_data['out_of_state_tuition'] = cost_info.get('tuition', {}).get('out_of_state')

                        admissions_info = latest_info.get('admissions')
                        if admissions_info:
                            school_data['act_scores'] = admissions_info.get('act_scores', {}).get('midpoint', {})
                            school_data['sat_scores'] = admissions_info.get('sat_scores', {}).get('midpoint', {})

                    school_data['programs'] = []

                    programs_info = latest_info.get('programs')
                    if programs_info:
                        cip_4_digit_info = programs_info.get('cip_4_digit', [])
                        for program in cip_4_digit_info:
                            program_info = {
                                'title': program.get('title'),
                                'level': program.get('credential', {}).get('title')
                            }
                            school_data['programs'].append(program_info)

                all_schools_data.append(school_data)

            return all_schools_data
        else:
            print(f"No results found for page {page}.")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def main():
    api_key = 'KTO75jVDbYUlVxQBgQ679YndI3gA7rkQVXGeoBgf'

    # Use a loop to fetch multiple pages until you have the first x amount of schools
    total_schools_to_fetch = 6546
    schools_per_page = 20
    pages_needed = total_schools_to_fetch // schools_per_page + 1

    all_schools_data = []

    for page in range(pages_needed):
        page_data = search_school(api_key, page=page)
        if page_data:
            all_schools_data.extend(page_data)

    with open('all_schools_data.json', 'a') as json_file:
        json.dump(all_schools_data, json_file, indent=2)

    print("Data successfully written to 'all_schools_data.json'.")

if __name__ == "__main__":
    main()