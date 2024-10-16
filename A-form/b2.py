import os
import re
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def extract_html_code(response):
    match = re.search(r"'''html\n(.*?)'''", response, re.DOTALL)
    if match:
        return match.group(1)
    return None

def extract_colors_from_original(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Tìm kiếm chuỗi màu sắc trong nội dung
    color_match = re.search(r'Màu Sắc Chủ Đạo: \[(.*?)\]', content, re.DOTALL)
    if color_match:
        colors = color_match.group(1)
        # Tách các màu thành danh sách
        color_list = [color.strip() for color in colors.split(',')]
        print(f"Màu sắc tìm thấy trong file: {color_list}")  # Thêm dòng này
        return color_list
    print("Không tìm thấy thông tin màu sắc trong file.")  # Thêm dòng này
    return []

def generate_ui_for_features(input_file, output_folder, original_file):
    # Đọc tài liệu gốc và trích xuất màu sắc
    colors = extract_colors_from_original(original_file)
    color_string = ', '.join(colors) if colors else "Không có màu sắc được chỉ định"

    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract features with their full content
    features = re.split(r'\n(?=\d+\.)', content)
    features = [f.strip() for f in features if f.strip()]

    # Initialize Anthropic client
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Keep track of created features to avoid duplicates
    created_features = set()

    for feature in features:
        # Extract feature name and full content
        match = re.match(r'(\d+\.\s*([^:]+)):(.*)', feature, re.DOTALL)
        if match:
            feature_number, feature_name, feature_content = match.groups()
            feature_name = feature_name.strip()
            feature_content = feature_content.strip()
        else:
            continue
        
        # Skip if feature has already been created
        if feature_name in created_features:
            continue
        
        # Generate HTML using Claude AI
        prompt = f"""
        Tạo giao diện HTML, CSS và JavaScript cho tính năng sau đây của một trang web:

        Tính năng: {feature_name}
        Nội dung đầy đủ: {feature_content}
        Màu sắc chủ đạo: {color_string}

        Yêu cầu:
        1. Tạo một trang HTML hoàn chỉnh bao gồm thẻ <html>, <head>, và <body>.
        2. Chỉ tạo giao diện cho tính năng được yêu cầu, Nội dung <title></title> bắt buộc phải tìm chính xác tên, danh từ, cụm danh từ riêng được cung cấp trong nội dung của từng tính năng.
        3. Không thêm bất kỳ tính năng, nội dung hoặc chức năng nào ngoài những gì được đề cập trong tên tính năng và nội dung đầy đủ.
        4. Sử dụng HTML5, CSS3 và JavaScript ES6+.
        5. Tạo giao diện cấp độ 4 (cao) với hiệu ứng animation tương lai và random 1 trong 10 bố cục [Z, F, Hình ảnh lớn, Chia đôi màn hình, Bất đối xứng, 1 Cột, Hình hộp, Thẻ, Báo chí, Dải ngang] làm nền background.
        6. Chỉ số opacity luôn là 1.
        7. Sử dụng thư viện GSAP (GreenSock Animation Platform) cho hiệu ứng animation mượt mà và phức tạp.
        8. Đảm bảo giao diện có responsive design và tương thích với các thiết bị khác nhau.
        9. Sử dụng các kỹ thuật CSS hiện đại như Grid, Flexbox nằm thẳng hàng không nhấp nhô, và CSS Variables.
        10. Tối ưu hóa hiệu suất bằng cách sử dụng CSS GPU acceleration khi thích hợp.
        11. Thêm các hiệu ứng tương tác như hover, click với animation phức tạp.
        12. Sử dụng màu sắc và gradient hiện đại, phù hợp với thiết kế tương lai, ưu tiên sử dụng các màu sắc chủ đạo đã cung cấp.
        13. Nếu phải dử dụng ảnh thì sử dụng đường dẫn "https://picsum.photos/300/200?random=" để điền ảnh
        14. Nếu là phần giới thiệu thì chữ và giao diện phải to rõ ràng ra gần hết màn hình.
        15. Luôn sử dụng tiếng Việt.

        Trả lời bằng cách cung cấp mã HTML đầy đủ, được bọc trong ba dấu nháy đơn và từ khóa html như sau:
        '''html
        Mã HTML, CSS và JavaScript ở đây
        '''
        """

        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8000,
            temperature=0.7,
            system="Bạn là một chuyên gia thiết kế UI/UX cấp cao, có nhiệm vụ tạo ra giao diện web tiên tiến nhất với hiệu ứng chuyên nghiệp và animation phức tạp. Bạn phải tuân thủ nghiêm ngặt yêu cầu và chỉ tạo giao diện dựa trên tên tính năng và nội dung đầy đủ được cung cấp, sử dụng màu sắc chủ đạo đã chỉ định, nhưng phải đảm bảo đó là giao diện cấp độ cao nhất có thể.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        html_content = extract_html_code(response.content[0].text)

        if html_content:
            # Create filename from feature name
            filename = os.path.join(output_folder, f"{feature_name.lower().replace(' ', '_')}.html")

            # Write HTML content to file
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(html_content)

            print(f"Created advanced UI for feature: {feature_name}")

            # Add feature to created_features set
            created_features.add(feature_name)
        else:
            print(f"Failed to generate UI for feature: {feature_name}")

    print("All advanced feature UIs have been generated.")

# Usage
input_file = '/Users/kieuphuchuy/Documents/A-form/tailieu/fgt_dichvu_features.txt'
output_folder = '/Users/kieuphuchuy/Documents/A-form/giaodien'
original_file = '/Users/kieuphuchuy/Documents/A-form/fgt_kgdd.txt'

generate_ui_for_features(input_file, output_folder, original_file)