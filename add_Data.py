import pandas as pd


def add_data_to_csv(file_path):
    # 读取CSV文件
    df = pd.read_csv(file_path,dtype=str)


    # 输入盒号
    h = input("请输入盒号: ")
    h = int(h)

    # 输入文本数据
    print("请输入4行6列的文本数据（每行以空格分隔）:")
    for row in range(4):
        row_data = input(f"第{row + 1}行: ").split(' ')

        # 检查输入数据长度
        if len(row_data) != 6:
            print("请确保每行输入6个数据。")
            return

        # 匹配第二列
        for i in range(6):
            for col in range(len(df)):
                if df.iloc[col, 1] == row_data[i].strip():  # 去掉多余空格
                    # 在后面加上盒号h，第几行，第几列
                    df.at[col,'盒号'] = h
                    df.at[col,'行'] = int(row + 1)
                    df.at[col,'列'] = int(i+1)
                    print(f"已在第{col + 1}行添加数据: {h}, {int(row + 1)}, {i+1}")
            df.to_csv(file_path, index=False)

    # 将修改后的DataFrame写回CSV文件
    df.to_csv(file_path, index=False)
    print("已成功更新CSV文件。")


# 使用示例
file_path = 'data.csv'  # 替换为你的CSV文件路径
add_data_to_csv(file_path)
