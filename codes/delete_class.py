import os

# 라벨 파일에서 클래스를 바꾸고 삭제하는 함수
def modify_labels(label_file_path):
    with open(label_file_path, 'r') as file:
        lines = file.readlines()
    
    modified_lines = []
    for line in lines:
        elements = line.strip().split()
        # Shoes 클래스(1번 인덱스)가 아닌 경우에만 수정된 라인으로 추가
        if elements[0] != '1':  # Shoes 클래스가 아닌 경우에만
            # Top 클래스(2번 인덱스)를 0번 인덱스로, Bottom 클래스(0번 인덱스)를 1번 인덱스로 변경
            if elements[0] == '2':  # Top 클래스인 경우
                elements[0] = '0'  # 클래스를 0으로 변경
            elif elements[0] == '0':  # Bottom 클래스인 경우
                elements[0] = '1'  # 클래스를 1으로 변경
            modified_lines.append(' '.join(elements) + '\n')
    
    # 수정된 내용을 파일에 씀
    with open(label_file_path, 'w') as file:
        file.writelines(modified_lines)

# 라벨 디렉토리 경로
label_directory = 'C:\\Users\\HP\\Desktop\\Tagging_System\\images3\\train\\labels2'

# 디렉토리 내 모든 .txt 파일에 대해 실행
for filename in os.listdir(label_directory):
    if filename.endswith('.txt'):
        filepath = os.path.join(label_directory, filename)
        modify_labels(filepath)
