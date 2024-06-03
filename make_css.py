import sys
import os
import re


def load_directory(src_path, css_file="./fonts.css"):
    string = ""
    font_tests = ""
    rg = re.compile(r"_(\w\w)\.")
    option = {
        "rr": ("normal", "normal"),
        "ii": ("italic", "normal"),
        "rb": ("normal", "bold"),
        "ib": ("italic", "bold")
    }
    for subdir, dirs, files in os.walk(src_path):

        for font_name in dirs:
            font_dir = os.path.join(subdir, font_name)
            for _, _, files in os.walk(font_dir):
                for file in files:
                    file_path = os.path.join(font_dir, file)
                    find = rg.findall(file)
                    if len(find) == 0:
                        continue
                    style, weight = option[find[0]]
                    css_string = (f"""@font-face {{
    font-family: {font_name};
    src: url({file_path});
    font-weight: {weight};
    font-style: {style};
}}
\n""")

                    string += css_string
                test_string = f"""
                <div  id="{font_name}">
                    <table>
                        <caption style="font-size:2em;">font-family: <span style="font-family: {font_name};">{font_name}</span></caption>
                        <tbody>
                            <tr><th>regular</th><td style="font-family: {font_name} !important; font-weight: normal; font-style: normal;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eros sem, faucibus laoreet pulvinar id, lobortis non metus. Nullam eget posuere sem. Nunc quis urna in tortor malesuada eleifend a eu turpis. Aenean sagittis malesuada lectus. Praesent nec justo at eros tincidunt ullamcorper. </td></tr>
                            <tr><th>regular bold</th><td style="font-family: {font_name} !important; font-weight: bold; font-style: normal;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eros sem, faucibus laoreet pulvinar id, lobortis non metus. Nullam eget posuere sem. Nunc quis urna in tortor malesuada eleifend a eu turpis. Aenean sagittis malesuada lectus. Praesent nec justo at eros tincidunt ullamcorper. </td></tr>
                            <tr><th>italic</th><td style="font-family: {font_name} !important; font-weight: normal; font-style: italic;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eros sem, faucibus laoreet pulvinar id, lobortis non metus. Nullam eget posuere sem. Nunc quis urna in tortor malesuada eleifend a eu turpis. Aenean sagittis malesuada lectus. Praesent nec justo at eros tincidunt ullamcorper. </td></tr>
                            <tr><th>italic bold</th><td style="font-family: {font_name} !important; font-weight: bold; font-style: italic;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eros sem, faucibus laoreet pulvinar id, lobortis non metus. Nullam eget posuere sem. Nunc quis urna in tortor malesuada eleifend a eu turpis. Aenean sagittis malesuada lectus. Praesent nec justo at eros tincidunt ullamcorper. </td></tr>
                        </tbody>
                    </table>
                </div>
                <hr />
"""
                font_tests += test_string

    with open(css_file, "w") as fp:
        fp.write(string)

    test_html = f"""<!DOCTYPE html>
<html>
    <head>
        <title>Font test: {src_path}</title>
        <link rel="stylesheet" href="{css_file}" type="text/css" />
        <meta charset="utf-8" />
        <style type="text/css">
        body {{
            font-family: monospace;
        }}
        th {{
            vertical-align: top;
            text-align: right;
            padding: 0.5em;
            padding-top: 0.75em;
        }}
        td {{
            text-align: justify;
        }}
        a {{
            color: blue;
        }}
        </style>
    </head>
    <body>
        <h1>Font test: <i>{src_path}</i> 🡒 <i><a href="{css_file}">{css_file}</a></i></h1>
        {font_tests}
    </body>
</html>
"""

    return string, test_html, css_file


def main():
    path = "./fonts"
    css, html, css_file = load_directory(path)
    with open("font_test.html", "w") as fp:
        fp.write(html)

    os.system(f"zip -r {path} font_test.html {css_file} {path}")


if __name__ == "__main__":
    main()