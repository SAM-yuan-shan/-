import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import PercentFormatter
import matplotlib.font_manager as fm
import os
import shutil
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
from PIL import Image, ImageDraw, ImageFont
import io

# Global font properties for Matplotlib (to be initialized in set_chinese_font)
MPL_FONT_PROP = None

# 首先清空可视化目录中的所有图片
if os.path.exists('visualizations'):
    for file in os.listdir('visualizations'):
        if file.endswith('.png'):
            try:
                os.remove(os.path.join('visualizations', file))
            except Exception as e:
                print(f"无法删除文件 {file}: {e}")
else:
    try:
        os.makedirs('visualizations')
    except Exception as e:
        print(f"无法创建目录 visualizations: {e}")

# Pillow字体设置
PILLOW_FONT_PATH = r"C:\Windows\Fonts\simkai.ttf" # Make sure this path is correct for your system
try:
    FONT_PILLOW_TITLE = ImageFont.truetype(PILLOW_FONT_PATH, 20)
    FONT_PILLOW_LABEL = ImageFont.truetype(PILLOW_FONT_PATH, 14)
    FONT_PILLOW_ANNOTATION = ImageFont.truetype(PILLOW_FONT_PATH, 10)
    FONT_PILLOW_LEGEND = ImageFont.truetype(PILLOW_FONT_PATH, 10)
    print(f"信息: Pillow字体 '{PILLOW_FONT_PATH}' 加载成功。")
except IOError:
    print(f"错误: 无法从 '{PILLOW_FONT_PATH}' 加载Pillow字体。请检查路径和字体文件是否有效。")
    print(f"      Pillow文本绘制功能将使用默认字体。")
    FONT_PILLOW_TITLE = ImageFont.load_default()
    FONT_PILLOW_LABEL = ImageFont.load_default()
    FONT_PILLOW_ANNOTATION = ImageFont.load_default()
    FONT_PILLOW_LEGEND = ImageFont.load_default()

# 更可靠的中文字体设置
def set_chinese_font():
    global MPL_FONT_PROP # Declare that we are using the global variable
    print("--- 开始设置中文字体 (Pillow 和 Matplotlib) ---")
    
    SYSTEM_FONT_PATH_MPL = PILLOW_FONT_PATH 

    try:
        font_name_mpl = "SimKai" # Default name, will try to get from file
        if os.path.exists(SYSTEM_FONT_PATH_MPL):
            try:
                font_abs_path = os.path.abspath(SYSTEM_FONT_PATH_MPL)
                is_font_added = False
                # Check if font is already in Matplotlib's list
                for font_entry in fm.fontManager.ttflist:
                    if hasattr(font_entry, 'fname') and font_entry.fname and os.path.samefile(font_entry.fname, font_abs_path):
                        is_font_added = True
                        font_name_mpl = font_entry.name
                        break
                
                if not is_font_added:
                    fm.fontManager.addfont(font_abs_path) 
                    print(f"信息: 已将字体文件 '{font_abs_path}' 添加到 Matplotlib 字体管理器。")
                    # Matplotlib might need to rebuild its font cache to find newly added fonts by name globally.
                    # For immediate use, FontProperties(fname=...) is most reliable.
                
                MPL_FONT_PROP = FontProperties(fname=font_abs_path)
                font_name_mpl = MPL_FONT_PROP.get_name() # Get the actual name Matplotlib recognizes

                print(f"信息: Matplotlib 将尝试使用字体: '{font_name_mpl}' (来自: {SYSTEM_FONT_PATH_MPL})")
                mpl.rcParams['font.family'] = [font_name_mpl, 'sans-serif'] 
                # mpl.rcParams['font.sans-serif'] = [font_name_mpl] + mpl.rcParams['font.sans-serif'] # Alternative way to add
            except Exception as e_mpl_font:
                print(f"警告: 为 Matplotlib 设置字体 '{SYSTEM_FONT_PATH_MPL}' 失败: {e_mpl_font}")
                print("      Matplotlib 将使用其默认后备字体。")
                try:
                    MPL_FONT_PROP = FontProperties(family='sans-serif') # Fallback
                    mpl.rcParams['font.family'] = ['sans-serif']
                except Exception as e_fallback_prop:
                    print(f"警告: 无法设置 Matplotlib 后备 FontProperties: {e_fallback_prop}")
                    MPL_FONT_PROP = None 
        else:
            print(f"警告: Matplotlib 字体路径 '{SYSTEM_FONT_PATH_MPL}' 不存在。将使用默认后备字体。")
            try:
                MPL_FONT_PROP = FontProperties(family='sans-serif') # Fallback
                mpl.rcParams['font.family'] = ['sans-serif']
            except Exception as e_fallback_prop:
                print(f"警告: 无法设置 Matplotlib 后备 FontProperties: {e_fallback_prop}")
                MPL_FONT_PROP = None
        
        plt.rcParams['axes.unicode_minus'] = False # Correctly display negative signs
        print(f"信息: Pillow 将使用字体 '{PILLOW_FONT_PATH}' 进行主要中文渲染。")

    except Exception as e_set_font:
        print(f"错误: set_chinese_font 中发生意外错误: {e_set_font}")
        MPL_FONT_PROP = None # Ensure it's None on major failure
    
    print("--- 字体设置结束 ---")

# 应用字体设置
set_chinese_font()

# 设置图表风格
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Data (remains unchanged from your original)
# 1. 参保人数与增长率数据
years = [2020, 2021, 2022, 2023, 2024]
participants = [443.43, 472.64, 512.03, 550.57, 577.49]
growth_rates = [None, 6.59, 8.33, 7.53, 4.89]
national_growth_rates = [None, 3.0, 2.0, 1.5, 0.6]

# 2. 参保结构数据
urban_workers = [None, 219.72, 258.63, 295.71, 322.55]
urban_workers_pct = [None, 46.49, 50.51, 53.71, 55.85]
rural_residents = [None, 232.22, 232.48, 233.46, 233.10]
rural_residents_pct = [None, 49.13, 45.40, 42.40, 40.36]
govt_workers = [None, 20.7, 20.92, 21.4, 21.84]
govt_workers_pct = [None, 4.38, 4.09, 3.89, 3.78]

# 3. 养老金水平数据
pension_adjustment = [5, 4.5, 4, 3.8, 3]
fuzhou_pension = [3100, 3300, 3400, 3550, 3750]
national_pension = [2600, 2700, 2900, 3000, 3162]
beijing_pension = [None, 4561, 4744, 4924, 5000]
shanghai_pension = [4800, 4900, 5000, 5100, 5000]
guangzhou_pension = [None, None, None, None, 4038]

# 4. 基金贡献数据 (2023年数据)
contributors = ['广东省', '江苏省', '浙江省', '福建省', '北京市']
contributions = [1158.14, 300, 250, 100, 200]

beneficiaries = ['黑龙江省', '辽宁省', '吉林省', '内蒙古', '湖北省']
benefits = [850, 830, 400, 300, 200]

# 5. 城市结构对比数据 (2024年)
cities_compare = ['福州市', '广东省', '上海市']
urban_pct = [55.85, 45, 63]
rural_pct = [40.36, 55, 37]
govt_pct = [3.78, 0, 0]


# =================== 创建可视化图表 ===================

# 1. 参保人数与增长率可视化
def plot_participants_growth():
    fig, ax1 = plt.subplots(figsize=(8, 5))
    
    color1 = 'tab:blue'
    ax1.set_ylabel('参保人数(万人)', color=color1, fontproperties=MPL_FONT_PROP if MPL_FONT_PROP else None)
    ax1.plot(years, participants, marker='o', linestyle='-', color=color1, linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color1)
    if MPL_FONT_PROP: # Apply font to numeric tick labels for style consistency
        for label in ax1.get_yticklabels(): label.set_fontproperties(MPL_FONT_PROP)
        for label in ax1.get_xticklabels(): label.set_fontproperties(MPL_FONT_PROP)
            
    color2 = 'tab:red'
    ax2 = ax1.twinx()
    growth_years = years[1:] 
    growth_data = growth_rates[1:]
    ax2.plot(growth_years, growth_data, marker='s', linestyle='--', color=color2, linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color2)
    if MPL_FONT_PROP: # Apply font to numeric tick labels for style consistency
        for label in ax2.get_yticklabels(): label.set_fontproperties(MPL_FONT_PROP)
    
    fig.tight_layout()
    
    output_path = 'visualizations/participants_growth.png'
    plt.savefig(output_path, dpi=200, bbox_inches='tight')

    # Pillow drawing (largely unchanged, ensure FONT_PILLOW_* are valid)
    img = Image.open(output_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    fig_width_px, fig_height_px = img.size
    color1_rgb = mpl.colors.to_rgb(color1) + (1,) 
    color1_pil = tuple(int(c*255) for c in color1_rgb) 
    color2_rgb = mpl.colors.to_rgb(color2) + (1,)
    color2_pil = tuple(int(c*255) for c in color2_rgb)

    title_text = "福州市基本养老保险参保人数及增长率(2020-2024)"
    text_bbox = draw.textbbox((0, 0), title_text, font=FONT_PILLOW_TITLE)
    text_width = text_bbox[2] - text_bbox[0]
    x = (fig_width_px - text_width) / 2
    y = 10
    draw.text((x, y), title_text, font=FONT_PILLOW_TITLE, fill=(0,0,0,255))

    xlabel_text = "年份"
    text_bbox = draw.textbbox((0, 0), xlabel_text, font=FONT_PILLOW_LABEL)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (fig_width_px - text_width) / 2
    y_xlabel = fig_height_px - text_height - 20 
    draw.text((x, y_xlabel), xlabel_text, font=FONT_PILLOW_LABEL, fill=(0,0,0,255))
    
    ylabel_ax2_text = "同比增长率(%)"
    text_bbox_y2 = draw.textbbox((0,0), ylabel_ax2_text, font=FONT_PILLOW_LABEL)
    text_width_y2 = text_bbox_y2[2] - text_bbox_y2[0]
    text_height_y2 = text_bbox_y2[3] - text_bbox_y2[1]
    x_y2 = fig_width_px - text_width_y2 - 15 
    y_y2 = (fig_height_px - text_height_y2) / 2
    draw.text((x_y2, y_y2), ylabel_ax2_text, font=FONT_PILLOW_LABEL, fill=color2_pil)

    for i, v in enumerate(participants):
        if v is not None:
            text_content = f'{v}'
            display_coords = ax1.transData.transform((years[i], v + 5)) # Offset for label placement
            pixel_x, pixel_y = display_coords[0], fig_height_px - display_coords[1]
            text_bbox_ann = draw.textbbox((0,0), text_content, font=FONT_PILLOW_ANNOTATION)
            text_w_ann, text_h_ann = text_bbox_ann[2]-text_bbox_ann[0], text_bbox_ann[3]-text_bbox_ann[1]
            adj_pixel_x = pixel_x - text_w_ann / 2
            adj_pixel_y = pixel_y - text_h_ann 
            draw.text((adj_pixel_x, adj_pixel_y), text_content, font=FONT_PILLOW_ANNOTATION, fill=color1_pil)

    for i, v_growth in enumerate(growth_data): # Use distinct variable name
        if v_growth is not None:
            text_content = f'{v_growth}%'
            display_coords = ax2.transData.transform((growth_years[i], v_growth + 0.3)) # Offset
            pixel_x, pixel_y = display_coords[0], fig_height_px - display_coords[1]
            text_bbox_ann = draw.textbbox((0,0), text_content, font=FONT_PILLOW_ANNOTATION)
            text_w_ann, text_h_ann = text_bbox_ann[2]-text_bbox_ann[0], text_bbox_ann[3]-text_bbox_ann[1]
            adj_pixel_x = pixel_x - text_w_ann / 2
            adj_pixel_y = pixel_y - text_h_ann 
            draw.text((adj_pixel_x, adj_pixel_y), text_content, font=FONT_PILLOW_ANNOTATION, fill=color2_pil)

    img.save(output_path)
    plt.close(fig)

# 2. 增长率对比可视化 (This plot relies entirely on Matplotlib for text)
def plot_growth_comparison():
    years_with_data = years[1:]
    fuzhou_growth = growth_rates[1:]
    national_growth = national_growth_rates[1:]
    
    plot_years_str = [str(y) for y in years_with_data] # Use strings for categorical labels if needed
    plot_fuzhou, plot_national, valid_plot_years = [], [], []

    for i, year_label in enumerate(plot_years_str):
        if fuzhou_growth[i] is not None and national_growth[i] is not None:
            valid_plot_years.append(year_label)
            plot_fuzhou.append(fuzhou_growth[i])
            plot_national.append(national_growth[i])

    if not valid_plot_years:
        print("警告 (plot_growth_comparison): 增长率对比数据不足，无法生成图表。")
        return

    x = np.arange(len(valid_plot_years))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 5))
    rects1 = ax.bar(x - width/2, plot_fuzhou, width, label='福州市', color='#5975a4')
    rects2 = ax.bar(x + width/2, plot_national, width, label='全国平均', color='#cc8963')
    
    title_text = '福州市与全国养老保险参保人数增长率对比'
    xlabel_text = '年份'
    ylabel_text = '同比增长率(%)'

    if MPL_FONT_PROP:
        ax.set_title(title_text, fontproperties=MPL_FONT_PROP)
        ax.set_xlabel(xlabel_text, fontproperties=MPL_FONT_PROP)
        ax.set_ylabel(ylabel_text, fontproperties=MPL_FONT_PROP)
        ax.set_xticks(x)
        ax.set_xticklabels(valid_plot_years, fontproperties=MPL_FONT_PROP)
        ax.legend(prop=MPL_FONT_PROP)
        for label in ax.get_yticklabels(): label.set_fontproperties(MPL_FONT_PROP)
    else: # Fallback if MPL_FONT_PROP is None
        ax.set_title(title_text)
        ax.set_xlabel(xlabel_text)
        ax.set_ylabel(ylabel_text)
        ax.set_xticks(x)
        ax.set_xticklabels(valid_plot_years)
        ax.legend()
        
    # Add bar labels
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontproperties=MPL_FONT_PROP if MPL_FONT_PROP else None,
                        fontsize=9) # Smaller font for bar labels
    autolabel(rects1)
    autolabel(rects2)
    
    fig.tight_layout()
    plt.savefig('visualizations/growth_comparison.png', dpi=200, bbox_inches='tight')
    plt.close(fig)

# 3. 参保结构可视化 (This plot relies entirely on Matplotlib for text)
def plot_insurance_structure():
    years_with_data_str = [str(y) for y in years[1:]]
    
    df = pd.DataFrame({
        '城镇企业职工': urban_workers_pct[1:],
        '城乡居民': rural_residents_pct[1:],
        '机关事业单位': govt_workers_pct[1:]
    }, index=years_with_data_str)
    
    df.dropna(how='all', inplace=True)
    if df.empty:
        print("警告 (plot_insurance_structure): 参保结构数据不足，无法生成图表。")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    df.plot(kind='bar', stacked=True, ax=ax, 
            color=['#5975a4', '#cc8963', '#5f9e6e'], alpha=0.8)
    
    title_text = f'福州市基本养老保险参保结构变化 ({df.index[0]}-{df.index[-1]})'
    xlabel_text = '年份'
    ylabel_text = '占比(%)'
    
    font_name_for_bar_label = MPL_FONT_PROP.get_name() if MPL_FONT_PROP else plt.rcParams['font.sans-serif'][0]

    if MPL_FONT_PROP:
        ax.set_title(title_text, fontproperties=MPL_FONT_PROP)
        ax.set_xlabel(xlabel_text, fontproperties=MPL_FONT_PROP)
        ax.set_ylabel(ylabel_text, fontproperties=MPL_FONT_PROP)
        ax.legend(prop=MPL_FONT_PROP)
        for label in ax.get_xticklabels(): label.set_fontproperties(MPL_FONT_PROP)
        for label in ax.get_yticklabels(): label.set_fontproperties(MPL_FONT_PROP)
    else:
        ax.set_title(title_text)
        ax.set_xlabel(xlabel_text)
        ax.set_ylabel(ylabel_text)
        ax.legend()
        
    ax.set_ylim(0, 100)
    
    for c in ax.containers:
        labels = [f'{v:.1f}%' if v is not None and v > 0.1 else '' for v in c.datavalues]
        ax.bar_label(c, labels=labels, label_type='center', 
                     fontfamily=font_name_for_bar_label, # Use extracted family name
                     fontsize=8, color='white', fontweight='bold')
    
    ax.legend(prop=MPL_FONT_PROP if MPL_FONT_PROP else None)
    fig.tight_layout()
    output_path = 'visualizations/insurance_structure.png'
    fig.savefig(output_path, dpi=200, bbox_inches='tight')

    # Pillow drawing for legend title
    img = Image.open(output_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    fig_width_px, fig_height_px = img.size
    
    legend_title_text = "参保类型"
    text_bbox_legend_title = draw.textbbox((0,0), legend_title_text, font=FONT_PILLOW_LABEL)
    legend_title_width = text_bbox_legend_title[2] - text_bbox_legend_title[0]
    
    # Estimate position for the legend title (e.g., top-right area)
    # Using similar estimation as in plot_insurance_structure
    x_legend_title = fig_width_px - legend_title_width - 150 
    y_legend_title = 60 

    draw.text((x_legend_title, y_legend_title), legend_title_text, font=FONT_PILLOW_LABEL, fill=(0,0,0,255))
    img.save(output_path)
    
    plt.close(fig)

# 4. 城市参保结构对比可视化 (This plot relies entirely on Matplotlib for text)
def plot_city_structure_comparison():
    df = pd.DataFrame({
        '城镇职工养老保险': urban_pct,
        '城乡居民养老保险': rural_pct,
        '机关事业单位养老保险': govt_pct
    }, index=cities_compare) 
    
    if df.empty:
        print("警告 (plot_city_structure_comparison): 城市参保结构对比数据不足，无法生成图表。")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    df.plot(kind='bar', stacked=True, ax=ax, 
            color=['#5975a4', '#cc8963', '#5f9e6e'], alpha=0.8)
    
    title_text = '福州市与领先城市参保结构对比(2024年)'
    xlabel_text = '城市/地区'
    ylabel_text = '占比(%)'

    font_name_for_bar_label = MPL_FONT_PROP.get_name() if MPL_FONT_PROP else plt.rcParams['font.sans-serif'][0]

    if MPL_FONT_PROP:
        ax.set_title(title_text, fontproperties=MPL_FONT_PROP)
        ax.set_xlabel(xlabel_text, fontproperties=MPL_FONT_PROP)
        ax.set_ylabel(ylabel_text, fontproperties=MPL_FONT_PROP)
        for label in ax.get_xticklabels(): label.set_fontproperties(MPL_FONT_PROP)
        for label in ax.get_yticklabels(): label.set_fontproperties(MPL_FONT_PROP)
        ax.legend(prop=MPL_FONT_PROP)
    else:
        ax.set_title(title_text)
        ax.set_xlabel(xlabel_text)
        ax.set_ylabel(ylabel_text)
        ax.legend()
        
    ax.set_ylim(0, 105)
    
    for c in ax.containers:
        labels = [f'{v:.1f}%' if v is not None and v > 0.1 else '' for v in c.datavalues]
        ax.bar_label(c, labels=labels, label_type='center', 
                     fontfamily=font_name_for_bar_label, # Use extracted family name
                     fontsize=8, color='white', fontweight='bold')

    fig.tight_layout()
    output_path = 'visualizations/city_structure_comparison.png'
    fig.savefig(output_path, dpi=200, bbox_inches='tight')

    # Pillow drawing for legend title
    img = Image.open(output_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    fig_width_px, fig_height_px = img.size
    
    legend_title_text = "参保类型"
    text_bbox_legend_title = draw.textbbox((0,0), legend_title_text, font=FONT_PILLOW_LABEL)
    legend_title_width = text_bbox_legend_title[2] - text_bbox_legend_title[0]
    
    # Estimate position for the legend title (e.g., top-right area)
    # Using similar estimation as in plot_insurance_structure
    x_legend_title = fig_width_px - legend_title_width - 150 
    y_legend_title = 60 

    draw.text((x_legend_title, y_legend_title), legend_title_text, font=FONT_PILLOW_LABEL, fill=(0,0,0,255))
    img.save(output_path)

    plt.close(fig)

# 5. 养老金水平对比可视化
def plot_pension_comparison():
    cities_pension_data = {
        '福州市': fuzhou_pension, '全国平均': national_pension,
        '北京': beijing_pension, '上海': shanghai_pension, '广州': guangzhou_pension
    }
    # Ensure years are suitable for indexing if they are not already numeric/datetime
    df_years = [int(y) for y in years] # Or pd.to_datetime(years, format='%Y')
    df = pd.DataFrame(cities_pension_data, index=df_years) 
    
    fig, ax = plt.subplots(figsize=(8, 5))
    plot_colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00']
    markers = ['o', 's', '^', 'D', 'x']
    
    has_data_to_plot = False
    plotted_lines_info = []

    for i, city_name in enumerate(df.columns): 
        city_data = df[city_name].dropna()
        if not city_data.empty:
            has_data_to_plot = True
            line_color = plot_colors[i % len(plot_colors)]
            # The label in ax.plot is used by Pillow for the legend
            ax.plot(city_data.index, city_data.values, 
                    marker=markers[i % len(markers)], 
                    linestyle='-', linewidth=2,
                    color=line_color, label=city_name) 
            
            last_year_val = city_data.index[-1] # Renamed to avoid conflict
            last_value_val = city_data.values[-1] # Renamed
            plotted_lines_info.append({
                'name': city_name, 'last_year': last_year_val, 'last_value': last_value_val,
                'color_mpl': line_color,
                'color_pil': tuple(int(c*255) for c in mpl.colors.to_rgb(line_color) + (1,)),
                'marker': markers[i % len(markers)]
            })
    
    if not has_data_to_plot:
        print("警告 (plot_pension_comparison): 养老金水平对比数据不足，无法生成图表。")
        plt.close(fig)
        return

    ax.grid(True, linestyle='--', alpha=0.7)
    if ax.get_legend() is not None: ax.get_legend().remove() # Pillow will draw legend
    
    # Apply font to tick labels (years and pension values)
    if MPL_FONT_PROP:
        for label in ax.get_xticklabels(): label.set_fontproperties(MPL_FONT_PROP)
        for label in ax.get_yticklabels(): label.set_fontproperties(MPL_FONT_PROP)
            
    fig.tight_layout()
    output_path = 'visualizations/pension_comparison.png'
    fig.savefig(output_path, dpi=200, bbox_inches='tight')

    # Pillow drawing (largely unchanged)
    img = Image.open(output_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    fig_width_px, fig_height_px = img.size

    title_text = "各地区企业退休人员人均养老金水平对比"
    text_bbox = draw.textbbox((0,0), title_text, font=FONT_PILLOW_TITLE)
    text_width = text_bbox[2] - text_bbox[0]
    x_title = (fig_width_px - text_width) / 2
    y_title = 10
    draw.text((x_title, y_title), title_text, font=FONT_PILLOW_TITLE, fill=(0,0,0,255))

    xlabel_text = "年份"
    text_bbox = draw.textbbox((0,0), xlabel_text, font=FONT_PILLOW_LABEL)
    text_width_xlabel = text_bbox[2] - text_bbox[0] # Renamed
    text_height_xlabel = text_bbox[3] - text_bbox[1] # Renamed
    x_xlabel_draw = (fig_width_px - text_width_xlabel) / 2 # Renamed
    y_xlabel_draw = fig_height_px - text_height_xlabel - 20 # Renamed
    draw.text((x_xlabel_draw, y_xlabel_draw), xlabel_text, font=FONT_PILLOW_LABEL, fill=(0,0,0,255))

    ylabel_text = "人均养老金(元/月)"
    # For non-rotated Y-axis label with Pillow:
    text_bbox_y = draw.textbbox((0,0), ylabel_text, font=FONT_PILLOW_LABEL)
    text_width_y = text_bbox_y[2] - text_bbox_y[0]
    text_height_y = text_bbox_y[3] - text_bbox_y[1]
    x_ylabel_draw = 10 # Left margin
    y_ylabel_draw = (fig_height_px - text_height_y) / 2
    # To rotate, you'd need to draw text to a separate image and rotate it.
    # For simplicity, let's draw it horizontally or assume Matplotlib handled it if it were there.
    # Since we are using Pillow, we can draw it horizontally here:
    draw.text((x_ylabel_draw, y_ylabel_draw), ylabel_text, font=FONT_PILLOW_LABEL, fill=(0,0,0,255))


    for line_info in plotted_lines_info:
        text_content = f" {line_info['last_value']:.0f}元"
        display_coords = ax.transData.transform((line_info['last_year'] + 0.1, line_info['last_value']))
        pixel_x, pixel_y = display_coords[0], fig_height_px - display_coords[1]
        text_bbox_ann = draw.textbbox((0,0), text_content, font=FONT_PILLOW_ANNOTATION)
        text_w_ann, text_h_ann = text_bbox_ann[2]-text_bbox_ann[0], text_bbox_ann[3]-text_bbox_ann[1]
        adj_pixel_x = pixel_x 
        adj_pixel_y = pixel_y - text_h_ann / 2
        draw.text((adj_pixel_x, adj_pixel_y), text_content, font=FONT_PILLOW_ANNOTATION, fill=line_info['color_pil'])

    legend_y_start, legend_x_start = 35, 35
    line_height, line_segment_length = 20, 15
    marker_size_pil, text_spacing = 5, 5
    for idx, line_info in enumerate(plotted_lines_info):
        y_pos_center = legend_y_start + idx * line_height + line_height / 2
        draw.line([(legend_x_start, y_pos_center), (legend_x_start + line_segment_length, y_pos_center)], fill=line_info['color_pil'], width=2)
        draw.ellipse([
            legend_x_start + line_segment_length/2 - marker_size_pil/2, y_pos_center - marker_size_pil/2, 
            legend_x_start + line_segment_length/2 + marker_size_pil/2, y_pos_center + marker_size_pil/2
            ], fill=line_info['color_pil'])
        # Get text bounding box for vertical alignment
        legend_text_bbox = FONT_PILLOW_LEGEND.getbbox(line_info['name'])
        legend_text_height = legend_text_bbox[3] - legend_text_bbox[1]
        text_y_adj = y_pos_center - legend_text_height / 2
        draw.text((legend_x_start + line_segment_length + text_spacing, text_y_adj), line_info['name'], font=FONT_PILLOW_LEGEND, fill=line_info['color_pil'])

    img.save(output_path)
    plt.close(fig)

# 6. 养老金调整水平可视化
def plot_pension_adjustment():
    valid_pension_adj_data = [(years[i], pension_adjustment[i]) for i in range(len(years)) if pension_adjustment[i] is not None]
    if not valid_pension_adj_data:
        print("警告 (plot_pension_adjustment): 养老金调整水平数据不足，无法生成图表。")
        return
    plot_adj_years = [item[0] for item in valid_pension_adj_data]
    plot_adj_values = [item[1] for item in valid_pension_adj_data]

    fig, ax = plt.subplots(figsize=(8, 5))
    line_color_mpl = '#e41a1c'
    ax.plot(plot_adj_years, plot_adj_values, marker='o', linestyle='-', color=line_color_mpl, linewidth=2)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    if MPL_FONT_PROP: # Apply to tick labels
        for label in ax.get_xticklabels(): label.set_fontproperties(MPL_FONT_PROP)
        for label in ax.get_yticklabels(): label.set_fontproperties(MPL_FONT_PROP)

    fig.tight_layout()
    output_path = 'visualizations/pension_adjustment.png'
    fig.savefig(output_path, dpi=200, bbox_inches='tight')

    # Pillow drawing (largely unchanged)
    img = Image.open(output_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    fig_width_px, fig_height_px = img.size
    line_color_pil = tuple(int(c*255) for c in mpl.colors.to_rgb(line_color_mpl) + (1,))
    arrow_color_pil = (0,0,0,255)

    title_text = "全国基本养老金调整水平变化趋势"
    text_bbox_title = draw.textbbox((0,0), title_text, font=FONT_PILLOW_TITLE) # Renamed
    text_width_title = text_bbox_title[2] - text_bbox_title[0] # Renamed
    x_title_draw = (fig_width_px - text_width_title) / 2 # Renamed
    y_title_draw = 10 # Renamed
    draw.text((x_title_draw, y_title_draw), title_text, font=FONT_PILLOW_TITLE, fill=(0,0,0,255))

    xlabel_text = "年份"
    text_bbox_xlabel = draw.textbbox((0,0), xlabel_text, font=FONT_PILLOW_LABEL)
    text_width_xlabel_adj = text_bbox_xlabel[2] - text_bbox_xlabel[0] # Renamed
    text_height_xlabel_adj = text_bbox_xlabel[3] - text_bbox_xlabel[1] # Renamed
    x_xlabel_adj_draw = (fig_width_px - text_width_xlabel_adj) / 2 # Renamed
    y_xlabel_adj_draw = fig_height_px - text_height_xlabel_adj - 20 # Renamed
    draw.text((x_xlabel_adj_draw, y_xlabel_adj_draw), xlabel_text, font=FONT_PILLOW_LABEL, fill=(0,0,0,255))

    ylabel_text = "调整水平(%)"
    text_bbox_ylabel = draw.textbbox((0,0), ylabel_text, font=FONT_PILLOW_LABEL)
    text_width_ylabel_adj = text_bbox_ylabel[2] - text_bbox_ylabel[0]
    text_height_ylabel_adj = text_bbox_ylabel[3] - text_bbox_ylabel[1]
    x_ylabel_adj_draw = 10 
    y_ylabel_adj_draw = (fig_height_px - text_height_ylabel_adj) / 2 
    draw.text((x_ylabel_adj_draw, y_ylabel_adj_draw), ylabel_text, font=FONT_PILLOW_LABEL, fill=(0,0,0,255))


    for yr, val in valid_pension_adj_data:
        text_content = f'{val}%'
        display_coords = ax.transData.transform((yr, val + 0.1))
        pixel_x, pixel_y = display_coords[0], fig_height_px - display_coords[1]
        text_bbox_ann = draw.textbbox((0,0), text_content, font=FONT_PILLOW_ANNOTATION)
        text_w_ann, text_h_ann = text_bbox_ann[2]-text_bbox_ann[0], text_bbox_ann[3]-text_bbox_ann[1]
        adj_pixel_x = pixel_x - text_w_ann / 2
        adj_pixel_y = pixel_y - text_h_ann 
        draw.text((adj_pixel_x, adj_pixel_y), text_content, font=FONT_PILLOW_ANNOTATION, fill=line_color_pil)

    if len(valid_pension_adj_data) >= 3:
        mid_point_year, mid_point_value = valid_pension_adj_data[len(valid_pension_adj_data)//2]
        start_point_year, start_point_value = valid_pension_adj_data[0]
        annot_text = '养老金调整水平总体呈逐步调整趋势'
        
        xy_display = ax.transData.transform((mid_point_year, mid_point_value))
        xytext_y_val = start_point_value + 0.5 if start_point_value is not None else mid_point_value
        xytext_display = ax.transData.transform((start_point_year, xytext_y_val ))

        pil_xy = (xy_display[0], fig_height_px - xy_display[1])
        pil_xytext = (xytext_display[0], fig_height_px - xytext_display[1])

        draw.line([pil_xy, pil_xytext], fill=arrow_color_pil, width=2) 
        # Simplified arrow head by just placing text. For a real arrowhead, draw a polygon.
        
        text_bbox_arr = draw.textbbox((0,0), annot_text, font=FONT_PILLOW_ANNOTATION)
        text_w_arr, text_h_arr = text_bbox_arr[2]-text_bbox_arr[0], text_bbox_arr[3]-text_bbox_arr[1]
        adj_pil_xytext_x = pil_xytext[0] - text_w_arr / 2
        adj_pil_xytext_y = pil_xytext[1] - text_h_arr / 2 
        draw.text((adj_pil_xytext_x, adj_pil_xytext_y), annot_text, font=FONT_PILLOW_ANNOTATION, fill=arrow_color_pil)

    img.save(output_path)
    plt.close(fig)

# 7. 基金贡献可视化
def plot_fund_contribution():
    if not contributors or not contributions or not beneficiaries or not benefits:
        print("警告 (plot_fund_contribution): 基金贡献数据不足，无法生成图表。")
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    colors1_mpl = plt.cm.Reds(np.linspace(0.4, 0.8, len(contributors)))
    ax1.barh(contributors, contributions, color=colors1_mpl) # Y-tick labels are contributors
    
    colors2_mpl = plt.cm.Blues(np.linspace(0.4, 0.8, len(beneficiaries)))
    ax2.barh(beneficiaries, benefits, color=colors2_mpl) # Y-tick labels are beneficiaries

    if MPL_FONT_PROP:
        # Apply font to Y-tick labels (province names) and X-tick labels (numeric)
        for label in ax1.get_yticklabels(): label.set_fontproperties(MPL_FONT_PROP)
        for label in ax1.get_xticklabels(): label.set_fontproperties(MPL_FONT_PROP)
        for label in ax2.get_yticklabels(): label.set_fontproperties(MPL_FONT_PROP)
        for label in ax2.get_xticklabels(): label.set_fontproperties(MPL_FONT_PROP)
            
    ax1.invert_yaxis() 
    ax2.invert_yaxis() 

    fig.tight_layout(pad=2.0) # Increased padding for titles
    output_path = 'visualizations/fund_contribution.png'
    fig.savefig(output_path, dpi=200, bbox_inches='tight')

    # Pillow drawing (largely unchanged)
    img = Image.open(output_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    fig_width_px, fig_height_px = img.size
    subplot_width_approx = fig_width_px / 2

    title1_text = "养老保险基金主要贡献省份(估算, 2023年)"
    text_bbox1 = draw.textbbox((0,0), title1_text, font=FONT_PILLOW_TITLE)
    text_width1 = text_bbox1[2] - text_bbox1[0]
    x_title1 = subplot_width_approx / 2 - text_width1 / 2
    y_title_shared = 15 # Adjusted y for title
    draw.text((max(5, x_title1), y_title_shared), title1_text, font=FONT_PILLOW_TITLE, fill=(0,0,0,255)) # max(5,..) to avoid negative x

    title2_text = "养老保险基金主要受益省份(估算, 2023年)"
    text_bbox2 = draw.textbbox((0,0), title2_text, font=FONT_PILLOW_TITLE)
    text_width2 = text_bbox2[2] - text_bbox2[0]
    x_title2 = subplot_width_approx + (subplot_width_approx / 2 - text_width2 / 2)
    draw.text((max(subplot_width_approx + 5, x_title2), y_title_shared), title2_text, font=FONT_PILLOW_TITLE, fill=(0,0,0,255))


    xlabel1_text = "贡献金额(亿元)"
    text_bbox_xlabel1 = draw.textbbox((0,0), xlabel1_text, font=FONT_PILLOW_LABEL)
    text_width_xlabel1 = text_bbox_xlabel1[2]-text_bbox_xlabel1[0]
    text_height_xlabel1 = text_bbox_xlabel1[3]-text_bbox_xlabel1[1] # Use this for consistent y positioning
    y_xlabel_shared = fig_height_px - text_height_xlabel1 - 25 
    x_xlabel1_draw = subplot_width_approx / 2 - text_width_xlabel1 / 2 # Renamed
    draw.text((max(5,x_xlabel1_draw), y_xlabel_shared), xlabel1_text, font=FONT_PILLOW_LABEL, fill=(0,0,0,255))

    xlabel2_text = "获得金额(亿元)"
    text_bbox_xlabel2 = draw.textbbox((0,0), xlabel2_text, font=FONT_PILLOW_LABEL)
    text_width_xlabel2 = text_bbox_xlabel2[2]-text_bbox_xlabel2[0]
    x_xlabel2_draw = subplot_width_approx + (subplot_width_approx / 2 - text_width_xlabel2 / 2) # Renamed
    draw.text((max(subplot_width_approx+5, x_xlabel2_draw), y_xlabel_shared), xlabel2_text, font=FONT_PILLOW_LABEL, fill=(0,0,0,255))
    
    for i, rect in enumerate(ax1.patches):
        value = contributions[i] 
        if value is None: continue
        text_content = f' {value}亿元'
        data_x = rect.get_width() * 1.01 
        data_y = rect.get_y() + rect.get_height() / 2
        display_coords = ax1.transData.transform((data_x, data_y))
        pixel_x, pixel_y = display_coords[0], fig_height_px - display_coords[1]
        text_bbox_ann = draw.textbbox((0,0), text_content, font=FONT_PILLOW_ANNOTATION)
        text_h_ann = text_bbox_ann[3]-text_bbox_ann[1]
        adj_pixel_x = pixel_x
        adj_pixel_y = pixel_y - text_h_ann / 2
        draw.text((adj_pixel_x, adj_pixel_y), text_content, font=FONT_PILLOW_ANNOTATION, fill=(0,0,0,255))

    for i, rect in enumerate(ax2.patches):
        value = benefits[i]
        if value is None: continue
        text_content = f' {value}亿元'
        data_x = rect.get_width() * 1.01
        data_y = rect.get_y() + rect.get_height() / 2
        display_coords = ax2.transData.transform((data_x, data_y))
        pixel_x, pixel_y = display_coords[0], fig_height_px - display_coords[1]
        text_bbox_ann = draw.textbbox((0,0), text_content, font=FONT_PILLOW_ANNOTATION)
        text_h_ann = text_bbox_ann[3]-text_bbox_ann[1]
        adj_pixel_x = pixel_x
        adj_pixel_y = pixel_y - text_h_ann / 2
        draw.text((adj_pixel_x, adj_pixel_y), text_content, font=FONT_PILLOW_ANNOTATION, fill=(0,0,0,255))

    img.save(output_path)
    plt.close(fig)

# 执行所有可视化函数
if __name__ == "__main__":
    print("开始生成养老保险数据可视化图表...")
    
    plot_participants_growth()
    print("1/7 - 参保人数与增长率图表已生成")
    
    plot_growth_comparison()
    print("2/7 - 增长率对比图表已生成")
    
    plot_insurance_structure()
    print("3/7 - 参保结构图表已生成")
    
    plot_city_structure_comparison() 
    print("4/7 - 城市参保结构对比图表已生成")
    
    plot_pension_comparison()
    print("5/7 - 养老金水平对比图表已生成")
    
    plot_pension_adjustment()
    print("6/7 - 养老金调整水平图表已生成")
    
    plot_fund_contribution()
    print("7/7 - 基金贡献图表已生成")
    
    print("图表生成完成！所有图表已保存到 'visualizations' 目录下。")
    print("请检查脚本运行时的【控制台输出信息】，特别是关于字体加载的部分。")
    print(f"当前Pillow及Matplotlib尝试使用的字体路径是: {PILLOW_FONT_PATH}")
    if MPL_FONT_PROP:
        print(f"Matplotlib FontProperties对象已设置为: {MPL_FONT_PROP.get_name()}")
    else:
        print("Matplotlib FontProperties对象未能成功设置为目标中文字体，将使用后备字体。")
    print(f"如果 '{PILLOW_FONT_PATH}' 字体无法正确加载或显示中文，请确认路径和文件有效，或检查控制台错误输出。")