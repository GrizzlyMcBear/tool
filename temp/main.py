from subprocess import *


def search_executable(filename='*', search_regex='non-existing expression !'):
    """ Default subprocess.call code:
    subprocess.call('strings.exe {filename}'.format(filename=filename),
                    stdin=None,
                    stdout=None,
                    stderr=None,
                    shell=False)
    """
    stringified_file = Popen(['strings.exe', filename], stdout=PIPE)
    matching_lines = Popen(['findstr', '/i', '/n', search_regex],
                           stdin=stringified_file.stdout, stdout=PIPE)
    stringified_file.stdout.close()
    bytes_array_result = matching_lines.communicate()[0]
    return bytes_array_result.decode('UTF-8')


def print_search_results(results=None, searched_topic='Unknown search topic'):
    print(searched_topic)
    print('=' * len(searched_topic))
    print(results)
    print()


def save_matches_to_file(results_filename='results_file.txt', match_type='Unknown', matched_results=''):
    output_file_handler = open(results_filename, 'a')
    for curr_line in matched_results.splitlines():
        colon_position = curr_line.find(':')
        if colon_position != -1:
            line_number = curr_line[0:colon_position]
            line_text = curr_line[colon_position + 1:]
            output_file_handler.write('{matched_text}, {match_type}, {match_line}\n'.format(matched_text=line_text,
                                                                                            match_type=match_type,
                                                                                            match_line=line_number))
    output_file_handler.close()


try:
    try:
        filename = input("Enter the filename to parse: ")
        results_filename = 'results.csv'

        # search and print emails:
        result = search_executable(filename, '[A-Za-z][\.]*[A-Za-z0-9]*@[A-Za-z]*\.[A-Za-z]*')
        # print_search_results(result, 'Search results for emails:')
        save_matches_to_file(results_filename, 'email', result)

        # search and print IPv4 Addresses:
        """ AI:
        - add handling to prevent reading values such as 029.123.001.012 which aren't valid IP addresses
        - handle (don't print) cases of versions i.e. 10.0.16299.15
        """
        result = search_executable(filename, '[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*')
        # print_search_results(result, 'Search results for IP Adresses:')
        save_matches_to_file(results_filename, 'IP', result)

        # search and print URLs/links:
        result = search_executable(filename, 'http://[A-Za-z0-9/.][A-Za-z0-9]* https://[A-Za-z0-9/.][A-Za-z0-9]*')
        # print_search_results(result, 'Search results for URLs/links:')
        save_matches_to_file(results_filename, 'URL', result)

        # search and print files:
        """ AI:
        - this regex stil needs some working on, it prints also non-files as results.
        """
        result = search_executable(filename, '[A-Za-z_][A-Za-z_0-9]*[\.][A-Za-z][A-Za-z][A-Za-z]\>')
        # print_search_results(result, 'Search results for file names:')
        save_matches_to_file(results_filename, 'file', result)

    except ValueError as selection_convertion_error:
        print('Error: invalid input for action !')
        print(selection_convertion_error)

except Exception as generalException:
    print('General error was encountered:')
    print(generalException)
    raise
"""
AI:
===
+   Add ability to search for the following strings:
    + Email Addresses, examples:
        1. john.doe@email.com
        2. test@email.net.il
        3. invalid@email
        4. a@B
    + IP Address
    + URL / links
    + file extensions, examples:
        *.dll
        *.txt
        test.txt

-   When generating results, the search for file extensions should include the filename

"""
