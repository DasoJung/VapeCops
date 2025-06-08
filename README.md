# VapeCops: 실시간 흡연 감지 시스템 🚭

---

## 소개

VapeCops 프로젝트는 딥러닝 기반의 실시간 흡연 감지 시스템으로, 공공장소에서의 비흡연 환경을 조성하기 위해 개발되었습니다. 이 노트북에서는 Jupyter Notebook 환경에서 TensorFlow와 OpenCV를 활용하여 MobileNet 모델을 학습시키는 과정을 보여줍니다. 학습된 모델은 h5 또는 saved_model 형식으로 변환되어 Raspberry Pi와 같은 엣지 디바이스에 배포되며, 흡연을 감지하면 경고음을 울리는 이동식 커스텀 로봇에 탑재 됩니다.

## 설치 및 실행 방법

### 필수 요구사항
- **Python 3.11** (라즈베리파이와 Jupyter Notebook 환경에서 Python 3.11을 권장)
- **가상환경 사용 권장**

### 1. Jupyter Notebook에서 모델 학습하기
프로젝트는 Jupyter Notebook 환경에서 학습 코드를 실행하여 모델을 트레이닝합니다. 아래 명령어로 노트북 환경을 실행하세요.

```bash
jupyter notebook
```

**학습 코드 실행**: `MobileNet_smoking_classification.ipynb` 파일을 열어 MobileNet 모델을 트레이닝합니다. 학습이 완료되면 모델 파일(.h5 또는 saved_model_directory 형식)을 다운로드하여 저장합니다.

### 2. 라즈베리파이에 모델 배포하기

#### 1) 가상환경 생성 및 활성화
라즈베리파이에서 가상환경을 만들어 필요 패키지를 격리하여 관리합니다.

```bash
#venv 설치
sudo apt update
sudo apt install python3-venv

#가상환경 생성
python3.9 -m venv venv

# 가상환경 활성화
source venv/bin/activate
```

#### 2) 필수 패키지 설치
가상환경에서 `requirements.txt` 파일을 사용해 필요한 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

#### 3) 모델 파일 및 스크립트 배포
트레이닝 완료 후 생성된 모델 파일을 라즈베리파이로 전송합니다. USB, scp 등 방법으로 파일을 복사한 뒤, 프로젝트 디렉토리에 배치합니다.


### 3. 프로젝트 실행
라즈베리파이에서 아래 명령어로 흡연자 감지 시스템을 실행합니다.

```bash
python3 detect_smoking.py
```

## 프로젝트 구조

```
VapeCops/
├── model/                        # 학습된 MobileNet 모델 파일
├── scripts/
│   ├── detect_smoking.py         # 라즈베리파이 실행 스크립트
│   └── utils.py                  # 유틸리티 함수
├── notebooks/
│   └── smoking_classification.ipynb # Jupyter Notebook 학습 코드
├── README.md
└── requirements.txt              # 필수 패키지 목록
```

## 결과 및 성과
- 흡연자 감지 정확도: **90% 이상의 신뢰도**
- 실시간 경고음 발동 기능 구현 완료
- 로봇 이동성 확보를 통해 공공장소에서의 비흡연 환경 조성 기여

## 참고 자료
- [TensorFlow MobileNet 모델](https://www.tensorflow.org/api_docs/python/tf/keras/applications/MobileNet)
