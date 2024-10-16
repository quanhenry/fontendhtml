import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

def generate_index_html_with_effects(input_file, output_file):
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    html_folder = os.path.dirname(input_file)

    with open(input_file, 'r', encoding='utf-8') as file:
        file_list = file.read().splitlines()

    html_content = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Trang chủ</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.9.1/gsap.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.9.1/ScrollTrigger.min.js"></script>
        <style>
            .section {
                opacity: 0;
                transform: translateY(50px);
            }
        </style>
    </head>
    <body>
    """

    html_content += '    <div id="header" class="section"></div>\n\n'

    for i, file_name in enumerate(file_list, start=1):
        full_path = os.path.join(html_folder, file_name)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
            section_id = f"function_{i}"
            html_content += f'    <div id="{section_id}" class="section">{file_content}</div>\n\n'
        else:
            print(f"Warning: File not found - {full_path}")

    html_content += '    <div id="footer" class="section"></div>\n'

    animation_prompt = """
    Tạo một đoạn mã JavaScript sử dụng GSAP để tạo hiệu ứng xuất hiện chuyên nghiệp cho các phần tử có class 'section'.
    Yêu cầu:
    1. Sử dụng ScrollTrigger để kích hoạt animation khi scroll đến phần tử.
    2. Tạo hiệu ứng fade in và slide up cho mỗi phần tử.
    3. Thêm một chút delay giữa các phần tử để tạo hiệu ứng lần lượt.
    4. Đảm bảo animation mượt mà và chuyên nghiệp.
    """

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0.7,
        system="Bạn là một chuyên gia JavaScript và GSAP, có nhiệm vụ tạo ra các hiệu ứng animation chuyên nghiệp và mượt mà.",
        messages=[
            {"role": "user", "content": animation_prompt}
        ]
    )

    animation_script = response.content[0].text

    html_content += f"""
    <script>
    {animation_script}
    </script>
    </body>
    </html>
    """

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"Index HTML file with animation effects has been generated: {output_file}")

input_file = '/Users/kieuphuchuy/Documents/A-form/giaodien/generated_files_list.txt'
output_file = '/Users/kieuphuchuy/Documents/A-form/giaodien/index.html'

generate_index_html_with_effects(input_file, output_file)