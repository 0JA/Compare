import os
from datetime import datetime
from settings import CONFIG, CSS_CONFIG

def retrieve_installed_packages():
    '''Returns the CSS styling for the HTML page.'''
    return f'''
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    body {{
        background-color: {CSS_CONFIG['BACKGROUND_COLOR']}; 
        color: {CSS_CONFIG['FONT_COLOR']}; 
        font-family: 'Roboto', sans-serif; 
        margin: 0;
        padding: 20px;
    }}
    table {{ 
        width: 48%; 
        float: left; 
        background-color: {CSS_CONFIG['TABLE_BACKGROUND']}; 
        border-collapse: collapse; 
        margin-right: 2%;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }}
    th, td {{ 
        padding: 12px 15px; 
        border: 1px solid {CSS_CONFIG['BORDER_COLOR']}; 
        text-align: left; 
    }}
    th {{ 
        background-color: {CSS_CONFIG['HEADER_BACKGROUND']}; 
        color: {CSS_CONFIG['HEADER_COLOR']}; 
        font-weight: bold; 
    }}
    tr:nth-child(even) {{ 
        background-color: {CSS_CONFIG['EVEN_ROW_COLOR']}; 
    }}
    tr:hover {{
        background-color: {CSS_CONFIG['HOVER_COLOR']};
    }}
    tr.virtual_env, .virtual_env {{ 
        background-color: {CSS_CONFIG['VIRTUAL_ENV_COLOR']}; 
        color: {CSS_CONFIG['VIRTUAL_ENV_FONT_COLOR']}; 
        font-weight: bold; 
    }}
    tr.global_env, .global_env {{ 
        background-color: {CSS_CONFIG['GLOBAL_ENV_COLOR']}; 
        color: {CSS_CONFIG['GLOBAL_ENV_FONT_COLOR']}; 
        font-weight: bold; 
    }}
    a {{ 
        text-decoration: none; 
        color: inherit; 
    }}
    a:hover {{ 
        text-decoration: underline; 
    }}
    #search_packages {{
        width: 98%;
        padding: 10px;
        margin: 10px 1%;
        box-sizing: border-box;
    }}
    '''

def generate_comparison_html(virtual_env_packages, global_env_packages):
    """Generates the comparison HTML file."""
    extra_inside_virtual = virtual_env_packages - global_env_packages
    extra_inside_global = global_env_packages - virtual_env_packages

    comparison_html_path = os.path.join(CONFIG['OUTPUT_DIRECTORY'], CONFIG['COMPARISON_HTML_FILENAME'])
    with open(comparison_html_path, "w") as file_handle:
        # HTML and CSS styling
        file_handle.write('<html>\n<head>\n<style>\n')
        file_handle.write(retrieve_installed_packages())
        file_handle.write('</style>\n</head>\n<body>\n')

        # JavaScript for searching
        file_handle.write('''
        <script>
            function search_tables() {
                let input, filter, tables, table_rows, table_data, i, j;
                input = document.getElementById("search_packages");
                filter = input.value.toUpperCase();
                tables = document.getElementsByTagName("table");
                for (let t = 0; t < tables.length; t++) {
                    table_rows = tables[t].getElementsByTagName("tr");
                    for (i = 1; i < table_rows.length; i++) {
                        table_rows[i].style.display = "none";
                        table_data = table_rows[i].getElementsByTagName("td");
                        for (j = 0; j < table_data.length; j++) {
                            if (table_data[j].innerHTML.toUpperCase().indexOf(filter) > -1) {
                                table_rows[i].style.display = "";
                                break;
                            }
                        }
                    }
                }
            }
        </script>
        ''')

        # Timestamp and Search bar
        file_handle.write(f'<div style="text-align: center; margin-bottom: 20px; background-color: {CSS_CONFIG["SEARCH_BAR_BACKGROUND"]}; color: {CSS_CONFIG["SEARCH_BAR_COLOR"]}; padding: 5px;">Comparison made on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br><input type="text" id="search_packages" onkeyup="search_tables()" placeholder="Search for packages.."></div>\n')

        # Floating Key
        file_handle.write('<div style="position: fixed; top: 10px; right: 10px;">\n')
        file_handle.write(f'<div><span class="virtual_env">{CONFIG["VIRTUAL_ENV_LABEL"]}</span></div>\n')
        file_handle.write(f'<div><span class="global_env">{CONFIG["GLOBAL_ENV_LABEL"]}</span></div>\n')
        file_handle.write('</div>\n')

        # Generate tables

        for env_name, packages, extra in [(CONFIG['VIRTUAL_ENV_LABEL'], virtual_env_packages, extra_inside_virtual), (CONFIG['GLOBAL_ENV_LABEL'], global_env_packages, extra_inside_global)]:
            file_handle.write('<table>\n')
            file_handle.write(f"<thead><tr><th>#</th><th>{env_name} Packages</th></tr></thead>\n<tbody>\n")
            for idx, package in enumerate(sorted(packages, key=lambda s: (s.lower(), s)), 1):
                package_name = package.split('==')[0]
                if package in extra:
                    row_class = 'virtual_env' if env_name == CONFIG['VIRTUAL_ENV_LABEL'] else 'global_env'
                else:
                    row_class = ''  # No special class for packages present in both environments
                file_handle.write(f'<tr class="{row_class}"><td>{idx}</td><td><a href="https://pypi.org/project/{package_name}/" target="_blank">{package_name}</a></td></tr>\n')
            file_handle.write("</tbody>\n</table>\n")


def main():
    """Main function to read package lists and generate the comparison HTML."""
    try:
        virtualenv_path = os.path.normpath(os.path.join(CONFIG['OUTPUT_DIRECTORY'], CONFIG['VIRTUALENV_FILENAME']))
        print(virtualenv_path)
        with open(virtualenv_path, "r") as file_handle:
            virtual_env_packages = set(file_handle.read().splitlines())

        globalenv_path = os.path.join(CONFIG['OUTPUT_DIRECTORY'], CONFIG['GLOBALENV_FILENAME'])
        with open(globalenv_path, "r") as file_handle:
            global_env_packages = set(file_handle.read().splitlines())
        print(f"Before generation")
        generate_comparison_html(virtual_env_packages, global_env_packages)
        print(f"Comparison saved to {os.path.join(CONFIG['OUTPUT_DIRECTORY'], CONFIG['COMPARISON_HTML_FILENAME'])}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
