import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from imblearn.under_sampling import RandomUnderSampler

STROKE_MENUS = ["종료",  # 0
                "데이터구하기",  # 1
                "변수한글화",  # 2
                "연속형변수편집",  # 3
                "범주형변수편집",  # 4
                "샘플링",  # 5
                "미완성 : 모델링",  # 6
                "미완성 : 학습",  # 7
                "미완성 : 예측"  # 8
                ]

stroke_menu = {"1": lambda t: t.spec(),
               "2": lambda t: t.rename_meta(),
               "3": lambda t: t.interval_variables(),
               "4": lambda t: t.norminal_variables(),
               "5": lambda t: t.sampling(),
               "6": lambda t: t.find_highest_hwy(),
               "7": lambda t: t.which_cty_in_suv_compact(),
               "8": lambda t: t.find_top5_hwy_in_audi(),
               "9": lambda t: t.find_top3_avg()
               }

stroke_meta = {'id': '아이디',
               'gender': '성별',
               'age': '나이',
               'hypertension': '고혈압',
               'heart_disease': '심장병',
               'ever_married': '기혼여부',
               'work_type': '직종',
               'Residence_type': '거주형태',
               'avg_glucose_level': '평균혈당',
               'bmi': '비만도',
               'smoking_status': '흡연여부',
               'stroke': '뇌졸중'
               }
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5110 entries, 0 to 5109
Data columns (total 12 columns):
 #   Column             Non-Null Count  Dtype  
---  ------             --------------  -----  
 0   id                 5110 non-null   int64  
 1   gender             5110 non-null   object 
 2   age                5110 non-null   float64
 3   hypertension       5110 non-null   int64  
 4   heart_disease      5110 non-null   int64  
 5   ever_married       5110 non-null   object 
 6   work_type          5110 non-null   object 
 7   Residence_type     5110 non-null   object 
 8   avg_glucose_level  5110 non-null   float64
 9   bmi                4909 non-null   float64
 10  smoking_status     5110 non-null   object 
 11  stroke             5110 non-null   int64  
dtypes: float64(3), int64(4), object(5)
memory usage: 479.2+ KB
None
'''


class StrokeService:
    def __init__(self):
        self.stroke = pd.read_csv('../../../../static/data/dam/per/stroke/healthcare-dataset-stroke-data.csv')
        self.my_stroke = None
    '''
    1.스펙 보기
    '''
    def spec(self):  # 1
        print(f" --- 1.Shape --- \n{self.stroke.shape}"
              f" --- 2.Features --- \n{self.stroke.columns}"
              f" --- 3.Info --- \n{self.stroke.info()}"
              f" --- 4.Case Top1 --- \n{self.stroke.head(1)}"
              f" --- 5.Case Bottom1 --- \n{self.stroke.tail(3)}"
              f" --- 6.Describe --- \n{self.stroke.describe()}"
              f" --- 7.Describe All --- \n{self.stroke.describe(include='all')}")
    '''
    2.한글 메타데이터
     --- 2.Features ---
    Index(['아이디', '성별', '나이', '고혈압', '심장병', '기혼여부', 
            '직종', '거주형태', '평균혈당', '비만도', '흡연여부', '뇌졸중'],

    '''
    def rename_meta(self):  # 2
        self.my_stroke = self.stroke.rename(columns=stroke_meta)
        print(" --- 2.Features ---")
        print(self.my_stroke.columns)

    '''
    타깃변수(=종속변수 dependant, y값) 설정
    입력변수(=설명변수, 확률변수, X값)
    타깃변수명: stroke (=뇌졸중)
    타깃변수값: 과거에 한 번이라도 뇌졸중이 발병했으면 1, 아니면 0
    '''
    """
    3. 연속형 = ['나이', '평균혈당', '비만도']
    """
    def interval_variables(self):  # 3
        self.rename_meta()
        df = self.my_stroke
        cols_interval = ['나이', '평균혈당', '비만도']
        print(f"--- 구간변수 타입 ---\n {df[cols_interval].dtypes}"
              f"--- 결측값 있는 변수 ---\n {df[cols_interval].isna().any()[lambda x: x]}"
              f"체질량 결측 비율 : {df['비만도'].isnull().mean():.2f}")
        # 체질량 결측비율: 0.03 는 무시

        pd.options.display.float_format = '{:.2f}'.format
        print(f"--- 구간변수 기초 통계량 --- \n{df[cols_interval].describe()}")
        criterion = df['나이'] > 18
        self.adult_stroke = df[criterion]
        print(f"--- 성인 객체 스펙 --- \n{self.adult_stroke.shape}")

        # 평균혈당 232.64이하와 체질량지수 60.3이하를 이상치로 규정하고 제거
        df = self.adult_stroke
        c1 = df['평균혈당'] <= 232.64
        c2 = df['비만도'] <= 60.3
        self.adult_stroke = self.adult_stroke[c1 & c2]
        print(f"--- 이상치 제거한 성인객체스펙 --- \n{self.adult_stroke.shape}")

    def ratio_variables(self):  # 해당 컬럼 없음
        pass
    '''
    4. 범주형 = ['성별', '고혈압', '심장병', '기혼여부', 
                '직종', '거주형태', '흡연여부']
    '''
    def norminal_variables(self):  # 4
        self.interval_variables()
        df = self.adult_stroke
        cols_categorical = ['성별', '고혈압', '심장병', '기혼여부', '직종', '거주형태', '흡연여부']
        print(f"--- 범주형 변수 데이터타입 --- \n {df[cols_categorical].dtypes}"
              f"--- 범주형 변수 결측값 --- \n {df[cols_categorical].isnull().sum()}"
              f"--- 결측값 있는 변수 --- \n {df[cols_categorical].isna().any()[lambda x: x]}")  # 결측값이 없음

        df['성별'] = OrdinalEncoder().fit_transform(df['성별'].values.reshape(-1,1))
        df['기혼여부'] = OrdinalEncoder().fit_transform(df['기혼여부'].values.reshape(-1, 1))
        df['직종'] = OrdinalEncoder().fit_transform(df['직종'].values.reshape(-1, 1))
        df['거주형태'] = OrdinalEncoder().fit_transform(df['거주형태'].values.reshape(-1, 1))
        df['흡연여부'] = OrdinalEncoder().fit_transform(df['흡연여부'].values.reshape(-1, 1))

        self.stroke = df
        print(" ### 프리프로세스 종료 ###")
        self.stroke.to_csv("./../../../../static/save/dam/per/stroke/stroke.csv")

    def ordinal_variables(self):   # 해당 컬럼 없음
        pass

    def sampling(self):  # 5
        dframe = pd.read_csv('../../../../static/save/dam/per/stroke/stroke.csv')
        data = dframe.drop(['뇌졸중'], axis=1)
        target = dframe['뇌졸중']
        undersample = RandomUnderSampler(sampling_strategy=0.333, random_state=2)
        data_under, target_under = undersample.fit_resample(data, target)
        print(target_under.value_counts(dropna=True))

        # 50:50 비율로 데이터 분할
        X_train, X_test, y_train, y_test = train_test_split(data_under, target_under,
                                                            test_size=0.5, random_state=42, stratify=target_under)
        print(f"X_train shape : {X_train.shape}")
        print(f"X_test shape : {X_test.shape}")

        print(f"y_train shape : {y_train.shape}")
        print(f"y_test shape : {y_test.shape}")


def my_menu(ls):
    for i, j in enumerate(ls):
        print(f"{i}. {j}")
    return input('메뉴 선택 : ')


if __name__ == '__main__':
    t = StrokeService()
    while True:
        menu = my_menu(STROKE_MENUS)
        if menu == '0':
            print("종료")
            break
        else:
            stroke_menu[menu](t)
            """
            try:
                stroke_menu[menu](t)
            except KeyError:
                print(" ### Error ### ")
            """