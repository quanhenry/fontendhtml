import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def generate_content_with_claude(prompt):
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8000,
        temperature=0.7,
        system="Bạn là một chuyên gia tạo nội dung web, có nhiệm vụ tạo ra nội dung chất lượng cao dựa trên yêu cầu được cung cấp.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text

def create_document(input_file, output_folder):
    content = read_file(input_file)
    
    # Generate header
    header_prompt = f"""
    Dựa trên nội dung sau đây, hãy tạo ra một đoạn văn bản mô tả header cho một trang web:

    {content}

    Header cần phải:
    1. Phản ánh chính xác loại hình và mục đích của trang web.
    2. Mô tả các thành phần chính của header (logo, menu, nút gọi hành động, v.v.).
    3. Trích xuất màu sắc và phong cách thiết kế đúng với nội dung.

    Hãy trả lời bằng một đoạn văn súc tích, chỉ bao gồm mô tả header, không cần giải thích thêm.
    """
    header = generate_content_with_claude(header_prompt)
    
    # Generate features
    features_prompt = f"""
    Dựa trên nội dung chi tiết sau đây về không gian/địa điểm, hãy liệt kê đầy đủ các tính năng cụ thể mà trang web cần có:

    {content}

    Yêu cầu:
    1. Liệt kê 6 tính năng quan trọng nhất trong maincontent, bám sát 100% thông tin được cung cấp trong nội dung.
    2. Mỗi tính năng cần được miêu tả cụ thể, sử dụng chính xác các con số, tên gọi và chi tiết từ dữ liệu gốc.
    3. Bao gồm đầy đủ thông tin về tất cả thông tin khách hàng cung cấp.
    4. Đảm bảo không bỏ sót bất kỳ thông tin quan trọng nào, kể cả các chi tiết về thiết kế, màu sắc, logo.
    5. Tạo các tính năng riêng biệt cho mỗi phần thông tin quan trọng.
    6. Không chứa địa chỉ, số điện thoại, email.
    7. Không chứa tính năng header, footer, trang chủ.
    8. Trong mỗi tính năng có sẵn miêu tả phong cách thiết kế, bố cục và màu sắc.
    9. Khi liệt kê đến tính năng CTA thì dừng lại không liệt kê nữa.
    10. Bao gồm cả thông tin liên hệ và call-to-action như một tính năng riêng.
    11. Trình bày các thông tin theo gạch đầu dòng.
    12. Không sử dụng dấu /, chỉ dùng từ nối.
    13. Tính năng đầu liên luôn là giứoi thiệu cá nhân, công ty, địa điểm.

    Hãy trả lời bằng một danh sách đánh số, mỗi mục bao gồm tên tính năng và mô tả chi tiết, sử dụng chính xác ngôn ngữ từ nội dung gốc.
    """
    features = generate_content_with_claude(features_prompt)
    
    # Generate footer
    footer_prompt = f"""
    Dựa trên nội dung chi tiết sau đây, hãy tạo ra một đoạn văn bản mô tả chính xác footer cho trang web:

    {content}

    Footer cần phải:
    1. Bao gồm chính xác tất cả thông tin liên hệ được cung cấp (địa chỉ, số điện thoại, email).
    2. Liệt kê đầy đủ các liên kết mạng xã hội nếu có.
    3. Sử dụng chính xác màu sắc chủ đạo được đề cập trong nội dung.
    4. Đề cập đến logo nếu được mô tả trong nội dung.
    5. Bao gồm bất kỳ slogan hoặc thông điệp quan trọng nào được nhắc đến.
    6. Không thêm bất kỳ thông tin nào không có trong nội dung gốc.

    Hãy trả lời bằng một đoạn văn ngắn gọn, chỉ bao gồm mô tả chính xác footer dựa trên dữ liệu có sẵn, không thêm bất kỳ giả định hay thông tin phỏng đoán nào.
    """
    footer = generate_content_with_claude(footer_prompt)
    
    # Write to separate files
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    header_file = os.path.join(output_folder, f"{base_name}_header.txt")
    features_file = os.path.join(output_folder, f"{base_name}_features.txt")
    footer_file = os.path.join(output_folder, f"{base_name}_footer.txt")
    
    write_file(header_file, header)
    write_file(features_file, features)
    write_file(footer_file, footer)
    
    return features_file

def save_feature_files_list(feature_file, output_folder):
    feature_files_list = os.path.join(output_folder, "feature_files_list.txt")
    with open(feature_files_list, 'w', encoding='utf-8') as f:
        f.write(f"{feature_file}\n")
    print(f"Danh sách đường dẫn file tính năng đã được lưu vào: {feature_files_list}")

# Usage
input_file = '/Users/kieuphuchuy/Documents/A-form/fgt_dichvu.txt'
output_folder = '/Users/kieuphuchuy/Documents/A-form/tailieu'

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

feature_file = create_document(input_file, output_folder)
save_feature_files_list(feature_file, output_folder)

print("Các tài liệu đã được tạo và lưu vào thư mục đầu ra.")
print("Danh sách đường dẫn file tính năng đã được lưu.")