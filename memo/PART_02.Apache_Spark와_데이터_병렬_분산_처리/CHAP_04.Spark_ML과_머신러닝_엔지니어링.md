# CH04. Spark ML과 머신러닝 엔지니어링

## CH04_01. MlLib과 머신러닝 파이프라인 구성
- MlLib
  - ML을 쉽고 확장성 있게 적용하기 위해
  - 머신러닝 파이프라인 개발을 쉽게 하기 위해
- DataFrame API 위에서 동작
- 머신러닝
  - **데이터**를 이용해 코딩을 하는 일
  - 최적화와 같은 방법을 통해 **패턴**을 찾는 일
- 알고리즘
  - Classification
  - Regression
  - Clustering
  - Recommendation
- 파이프라인
  - Training
  - Evaluating
  - Tuning: 하이퍼 파라미터
  - Persistence: 모델 저장
- Future Engineering
  - Extraction
  - Transformation
- Utils
  - Linear algebra
  - Statistics

### 머신러닝 파이프라인
- 머신러닝 -> 전처리 -> 학습 -> 모델 평가
- 이 과정을 반복, 파라미터 튜닝 후 다시 시도 

### 머신러닝으로 할 수 있는일
- 피처 엔지니어링
- 통계적 연산
- 흔히 쓰이는 ML 알고리즘들
  - Regression: Linear, Logistic
  - Support Vector Machines
  - Naive Bayes
  - Decision Tree
  - K-Means clustering
- 추천: Alternating Least Squares
- RDD API가 있지만 maintenance mode
  - 새로운 API는 개발이 끊김
- DataFrame을 쓰는 Mllib API를 `Spoark ML`이라고 부름

### 파이프라인을 구성하는데 필요한 컴포넌트

#### DataFrame

#### Transformer
- 피처 변환과 학습된 모델 추상화
- 모든 Transformer는 `transform()`함수를 가짐
- 데이터를 **학습이 가능한 포맷**으로 바꿈
- DF를 받아 새로운 DF를 만드는데,
  - 보통 하나 이상의 column을 더함
- e.g. `Data Normalization`, `Tokenization`, `one-hot encoding`

#### Estimator
- 모델의 학습 과정 추상화
- 모든 Estimator는 `fit()`함수를 가짐
- `fit()`은 DataFrame을 받아 `Model`을 반환
- 모델은 하나의 `Transformer`
  ```python
  lr = LinearRegression()
  # fit = 학습
  model = lr.fit(data)
  ```

#### Evaluator
- `metric`을 기반으로 모델의 성능 평가
  - RMSE: Root Mea Squared Error
- 모델을 여러개 만들어, 성능 평가 이후 가장 좋은 모델을 뽑는 방식으로 모델 튜닝을 자동화 가능
- e.g.
  - `BinaryClassitficationEvaluator`
  - `CrossValidator`

#### Pipeline
- ML의 워크플로우
- 여러 `stage`를 담고 있음
- 저장될 수 있음(`persist`)
- 아래 `stage`들이 하나의 파이프 라인을 이룸
  - 데이터 로딩 -> 전처리 -> 학습 -> 모델 평가
  - Transformer -> Transformer -> Estimator -> Evaluator = Model 

#### Parameter
- X

## CH04_02. 첫 파이프라인 구축
- X

## CH04_03. 추천 알고리즘
- ALS: Alternating Least Squares
  - 왔다갔다 하면서, 제곱된 숫자를 최적화
- 협업 필터링
  - User A가 본 영화에만 스코어링
  - User B가 본 영와헤만 스코어링
  - A가 보지않고, B가 본 영화에 따라
    - A에게 영화 추천
- `Rating Matrix = User matrix * Item Matrix`
  - 두 행렬중 하나를 고정시키고, 최적화
  - 몇개의 과정이 순차적으로 실행되면서 User matrix, Item matrix를 찾아가는 과정
- 과정
  - Item matrix, user Matrix는 랜덤한 값으로 채워짐
  - Item 행렬 고정, user 최적화
    - item * user = rating에 유사하게 최적화
  - User 행렬 고정, item 최적화
  - 여러번 반복하게 되어 만들어진 matrix는
    - origin rating matrix와 달리 빈 값들이 모두 채워진 상황(예측값)
    - 그에 따라 추천 결과를 도출

## CH04_04. 영화 추천 파이프라인 구축
- X

## CH04_05. Regression & Classification
- 지도 학습(supervised learning)
- Regression: 실수
- Classification: 클래스(카테고리)
- Linear Regression
  - 데이터 분포에 맞게 선을 긋는 상황
  - RMSE를 가지고 최적화

## CH04_06. 택시비 예측하기 1
- X

## CH04_07. 택시비 예측하기 2
- X

