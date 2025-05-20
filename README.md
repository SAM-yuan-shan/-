# 福州市养老保险数据可视化

本项目用于可视化福州市2020-2024年的养老保险数据，包括参保人数、结构变化、养老金水平等多个维度。

## 环境配置

1. 安装Python环境（建议Python 3.8+）
2. 安装必要的依赖包：

```bash
pip install -r requirements.txt
```

## 运行可视化程序

```bash
python pension_data_visualization.py
```

运行后，所有生成的图表将保存在`visualizations`目录下。

## 图表说明

本程序将生成7种不同的可视化图表：

1. `participants_growth.png` - 福州市基本养老保险参保人数及增长率(2020-2024)
2. `growth_comparison.png` - 福州市与全国参保人数增长率对比(2021-2024)
3. `insurance_structure.png` - 福州市基本养老保险参保结构变化(2021-2024)
4. `city_structure_comparison.png` - 福州市与领先城市参保结构对比(2024年)
5. `pension_comparison.png` - 各地区企业退休人员人均养老金水平对比(2020-2024)
6. `pension_adjustment.png` - 全国基本养老金调整水平变化趋势(2020-2024)
7. `fund_contribution.png` - 养老保险基金贡献省份与受益省份(2023年)

## 数据来源

数据来源于《福州市养老保险数据对比分析报告（2020-2024）》，部分缺失数据采用估算值。 