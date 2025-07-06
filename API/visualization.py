import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import os

# 1. 한글 폰트 설정
def set_korean_font():
    system = platform.system()
    if system == 'Windows':
        plt.rcParams['font.family'] = 'Malgun Gothic'
    elif system == 'Darwin':
        plt.rcParams['font.family'] = 'AppleGothic'
    else:  # Linux, Colab
        font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
        if os.path.exists(font_path):
            from matplotlib import font_manager as fm
            font_name = fm.FontProperties(fname=font_path).get_name()
            plt.rcParams['font.family'] = font_name
        else:
            print("한글 폰트를 찾을 수 없습니다.")
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

# 2. 데이터 로딩
CSV_PATH = "API/failed_log.csv"  # 필요 시 경로 수정
try:
    df = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    raise FileNotFoundError(f"'{CSV_PATH}' 파일을 찾을 수 없습니다.")

# 3. 시각화 함수 정의

def plot_failure_reason_pie(df):
    """Pie chart of failure reasons"""
    reason_counts = df['reason'].value_counts()
    plt.figure(figsize=(7, 7))
    plt.pie(reason_counts,
            labels=reason_counts.index,
            autopct='%1.1f%%',
            startangle=140,
            textprops={'fontsize': 12})
    plt.title("Proportion of Failure Reasons", fontsize=16)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def plot_failure_reason_bar(df):
    """Bar chart of failure reasons"""
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, y="reason", order=df['reason'].value_counts().index, palette="Set2")
    plt.title("Distribution of Failure Reasons", fontsize=14)
    plt.xlabel("Number of Images")
    plt.ylabel("Failure Reason")
    plt.tight_layout()
    plt.show()


def plot_confidence_distribution(df):
    """Histogram of TOP / BOTTOM confidence"""
    plt.figure(figsize=(10, 5))
    sns.histplot(df['top_conf'], color="blue", label="TOP", kde=True, bins=20)
    sns.histplot(df['bottom_conf'], color="red", label="BOTTOM", kde=True, bins=20)
    plt.title("Distribution of TOP / BOTTOM Confidence", fontsize=14)
    plt.xlabel("Confidence")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_center_y_scatter(df):
    """Scatter plot of TOP vs BOTTOM center Y coordinates"""
    valid_y = df.dropna(subset=['top_cy', 'bottom_cy'])
    plt.figure(figsize=(6, 6))
    sns.scatterplot(data=valid_y, x="top_cy", y="bottom_cy", hue="reason", edgecolor="w", alpha=0.8)
    plt.title("TOP vs BOTTOM Center Y Coordinates", fontsize=14)
    plt.xlabel("TOP Center Y")
    plt.ylabel("BOTTOM Center Y")
    plt.tight_layout()
    plt.show()

# 4. 함수 실행
plot_failure_reason_pie(df)
plot_failure_reason_bar(df)
plot_confidence_distribution(df)
plot_center_y_scatter(df)
