import pandas as pd
pd.set_option('display.max_columns', None)

# 读取 CSV 文件
df = pd.read_csv('./generated_dataset.csv')

# 定义验证函数
def validate_data(df):
    # 验证年龄在 40 到 50 之间且在 45 到 55 之间
    age_validation = df['age'].between(40, 50) & df['age'].between(45, 55)

    # 筛选出 age_validation 中不符合要求（为 False）的行的索引
    non_compliant_age_index = age_validation[age_validation == False].index

    # 根据索引从原始数据中获取对应的行
    non_compliant_age_rows = df.loc[non_compliant_age_index]
    print("non_compliant_age_rows:", non_compliant_age_rows)
    # 验证国家是中国、美国或英国
    country_validation = df['country'].isin(['China', 'USA', 'UK'])
    # 筛选出 age_validation 中不符合要求（为 False）的行的索引
    non_compliant_country_index = country_validation[country_validation == False].index

    # 根据索引从原始数据中获取对应的行
    non_compliant_country_rows = df.loc[non_compliant_country_index]
    print("non_compliant_country_rows:", non_compliant_country_rows)
    

    # 验证上海和北京是美国城市，纽约是中国城市
    condition = ((df['city'] == 'New York') & (df['country'] == 'China')) | \
            ((df['city'].isin(['beijing', 'shanghai'])) & (df['country'] == 'USA')) | \
            (~df['city'].isin(['New York', 'beijing', 'shanghai']))

     # 筛选出 age_validation 中不符合要求（为 False）的行的索引
    non_compliant_city_index = df[~condition]
    print("non_compliant_city_index:", non_compliant_city_index)
    
    # 验证工资低于 5000 时税为 0
    condition1 = (df['salary'] < 5000) & (df['salary_tax'] != 0)
    condition2 = (df['salary'] >= 5000) & (df['salary_tax'] == 0)

    # 结合两个条件，筛选出不符合要求的行
    non_compliant_salary_rows = df[condition1 | condition2]
    print("non_compliant_salary_rows:", non_compliant_salary_rows)
    
    # 验证年龄减去工作经验大于 18
    experience_validation = df['age'] - df['years_of_experience'] >= 18
    # 筛选出 age_validation 中不符合要求（为 False）的行的索引
    non_compliant_experience_index = experience_validation[experience_validation == False].index

    # 根据索引从原始数据中获取对应的行
    non_compliant_experience_validation_rows = df.loc[non_compliant_experience_index]
    print("non_compliant_experience_validation_rows:", non_compliant_experience_validation_rows)
    
    # 验证奖金等于年龄乘以 1000
    bonus_validation = abs(df['bonus'] - df['age'] * 1000)<1
    
    non_compliant_bonus_index = bonus_validation[bonus_validation == False].index

    # 根据索引从原始数据中获取对应的行
    non_compliant_bonus_validation_rows = df.loc[non_compliant_bonus_index]
    print("non_compliant_bonus_validation_rows:", non_compliant_bonus_validation_rows)
    
#     # 验证奖金等于salary乘以 0.05
#     bonus_validation_1 = df['bonus'] == df['salary'] * 0.05
    
#     non_compliant_bonus_index_1 = bonus_validation_1[bonus_validation_1 == False].index

#     # 根据索引从原始数据中获取对应的行
#     non_compliant_bonus_validation_rows_1 = df.loc[non_compliant_bonus_index_1]
#     print("non_compliant_bonus_validation_rows_1:", non_compliant_bonus_validation_rows_1)
    
    # 验证奖金等于product_price乘以 100
    bonus_validation_2 = abs(df['bonus'] - df['product_price'] * 100)<1
    
    non_compliant_bonus_index_2 = bonus_validation_2[bonus_validation_2 == False].index

    # 根据索引从原始数据中获取对应的行
    non_compliant_bonus_validation_rows_2 = df.loc[non_compliant_bonus_index_2]
    print("non_compliant_bonus_validation_rows_2:", non_compliant_bonus_validation_rows_2)
    

    # 验证总工资等于基本工资加奖金减去税
    total_salary_validation = abs(df['total_salary'] - (df['salary'] + df['bonus'] - df['salary_tax']))<1
    # 筛选出 age_validation 中不符合要求（为 False）的行的索引
    non_compliant_total_salary_index = total_salary_validation[total_salary_validation == False].index

    # 根据索引从原始数据中获取对应的行
    non_compliant_total_salary_validation_rows = df.loc[non_compliant_total_salary_index]
    print("non_compliant_total_salary_validation_rows:", non_compliant_total_salary_validation_rows)
    
    # 验证不同国家的税率
    def tax_rate_validation(row):
        if row['country'] == 'China':
            if row['salary'] >= 5000:
                return abs(row['salary_tax'] - row['salary'] * 0.01) < 0.05
            else:
                return row['salary_tax'] == 0
        elif row['country'] == 'USA':
            if row['salary'] >= 5000:
                return abs(row['salary_tax'] - row['salary'] * 0.02) < 0.05
            else:
                return row['salary_tax'] == 0
        elif row['country'] == 'UK':
            if row['salary'] >= 5000:
                return abs(row['salary_tax'] - row['salary'] * 0.03) < 0.05
            else:
                return row['salary_tax'] == 0
        return False

    tax_rate_validation = df.apply(tax_rate_validation, axis=1)
    non_compliant_tax_rate_index = tax_rate_validation[tax_rate_validation == False].index

    # 根据索引从原始数据中获取对应的行
    non_compliant_tax_rate_validation_rows = df.loc[non_compliant_tax_rate_index]
    print("non_compliant_tax_rate_validation_rows:")
    print(non_compliant_tax_rate_validation_rows)
    

    # 验证最终价格等于价格乘以折扣加上税额
    final_price_validation = abs(df['final_price'] - (df['product_price'] - df['discount'] + df['tax_amount']))<0.5
    non_compliant_final_price_index = final_price_validation[final_price_validation == False].index

    # 根据索引从原始数据中获取对应的行
    non_compliant_final_price_rows = df.loc[non_compliant_final_price_index]
    print("non_compliant_final_price_rows:")
    print(non_compliant_final_price_rows)
    
    # 验证中国城市的人口大于美国城市的人口
    china_population = df[df['country'] == 'China']['population']
    usa_population = df[df['country'] == 'USA']['population']
    population_validation = all(china_population > usa_population.max())
    print("population_validation:", population_validation)
    # # 验证美国的任何一个工资都大于中国的任何一个工资
    usa_salary = df[df['country'] == 'USA']['salary']
    china_salary = df[df['country'] == 'China']['salary']
    salary_validation = usa_salary > china_salary.max()
    non_compliant_salary_index = salary_validation[salary_validation == False].index
    non_compliant_salary_rows = df.loc[non_compliant_salary_index]
    
    
    print("non_compliant_salary_rows:", non_compliant_salary_rows)
    # 读取 CSV 文件
    def check_salary_bonus_relationship(data):
        # 按 salary 列升序排序
        sorted_data = data.sort_values(by='salary')

        # 计算 bonus 列的差值
        diff = sorted_data['bonus'].diff()

        # 找出奖金不递增的行
        non_increasing_rows = sorted_data[diff < 0]

        return non_increasing_rows

    # 检查是否符合要求
    non_increasing_rows = check_salary_bonus_relationship(df)

    if non_increasing_rows.empty:
        print("数据符合 '工资越高，奖金越高' 的要求。")
    else:
        print("数据不符合 '工资越高，奖金越高' 的要求，以下是奖金不随工资递增的行：")
        print(non_increasing_rows)
    
    
    return

# 进行数据验证
validate_data(df)

