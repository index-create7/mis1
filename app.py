def render_brush_section_tab(records):
    """渲染刷段记录界面"""
    
    # 目标总距离
    TOTAL_TARGET_KM = 80
    
    # 过滤出非官方的记录（is_official=False）
    non_official_records = [record for record in records if record.is_official == False]
    
    # 初始化刷段记录字典
    brush_records = {
        "running": [],  # 跑步记录，单位：km
        "swimming": [],  # 游泳记录，单位：次
        "rope_skipping": []  # 跳绳记录，单位：个
    }
    
    # 将数据库记录转换为刷段记录格式
    for record in non_official_records:
        if record.exercise_type == "跑步" and record.distance:
            brush_records["running"].append(record.distance)
        elif record.exercise_type == "游泳":
            brush_records["swimming"].append(1)  # 每次游泳算1次
        elif record.exercise_type == "跳绳" and record.distance:
            # 跳绳记录中distance字段存储的是跳绳个数
            brush_records["rope_skipping"].append(record.distance)
    
    # 转换逻辑：计算总km数
    def calculate_total_km():
        # 跑步：直接算km
        running_km = sum(brush_records["running"])
        
        # 游泳：1次=2km
        swimming_km = sum(brush_records["swimming"]) * 2
        
        # 跳绳：400个=1km
        rope_skipping_km = sum(brush_records["rope_skipping"]) / 400
        
        total_km = running_km + swimming_km + rope_skipping_km
        return total_km
    
    # 计算当前进度
    current_total_km = calculate_total_km()
    progress_percentage = (current_total_km / TOTAL_TARGET_KM) * 100
    
    # 显示进度
    st.subheader("📊 刷段进度")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("当前累计", f"{current_total_km:.2f} km")
    with col2:
        st.metric("目标总距离", f"{TOTAL_TARGET_KM} km")
    with col3:
        st.metric("完成进度", f"{progress_percentage:.1f}%")
    
    # 进度条
    st.progress(min(progress_percentage / 100, 1.0), text=f"已完成 {current_total_km:.2f} km / {TOTAL_TARGET_KM} km")
    
    # 详细统计信息
    st.markdown("---")
    st.subheader("📋 详细统计")
    
    # 计算各运动类型的贡献
    running_km = sum(brush_records["running"])
    swimming_km = sum(brush_records["swimming"]) * 2
    rope_skipping_km = sum(brush_records["rope_skipping"]) / 400
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🏃 跑步")
        st.write(f"总距离: {running_km:.2f} km")
        st.write(f"贡献: {running_km:.2f} km")
        st.write(f"记录次数: {len(brush_records['running'])}")
    
    with col2:
        st.markdown("### 🏊 游泳")
        st.write(f"总次数: {sum(brush_records['swimming'])} 次")
        st.write(f"贡献: {swimming_km:.2f} km")
        st.write(f"记录次数: {len(brush_records['swimming'])}")
    
    with col3:
        st.markdown("### 🪢 跳绳")
        st.write(f"总个数: {sum(brush_records['rope_skipping'])} 个")
        st.write(f"贡献: {rope_skipping_km:.2f} km")
        st.write(f"记录次数: {len(brush_records['rope_skipping'])}")
    
    # 可视化图表
    st.markdown("---")
    st.subheader("📊 运动类型贡献比例")
    
    if current_total_km > 0:
        # 准备数据
        labels = ['跑步', '游泳', '跳绳']
        sizes = [running_km, swimming_km, rope_skipping_km]
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        
        # 创建饼图
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # 保持圆形
        
        # 显示图表
        st.pyplot(fig)
    else:
        st.info("暂无数据")
    
    # 历史记录表格
    st.markdown("---")
    st.subheader("📝 历史记录")
    
    # 合并所有记录
    all_records = []
    
    # 添加跑步记录
    for i, km in enumerate(brush_records['running']):
        all_records.append({
            '序号': i+1,
            '运动类型': '跑步',
            '数量': f'{km:.2f} km',
            '转换后km': f'{km:.2f} km'
        })
    
    # 添加游泳记录
    for i, times in enumerate(brush_records['swimming']):
        converted_km = times * 2
        all_records.append({
            '序号': len(all_records)+1,
            '运动类型': '游泳',
            '数量': f'{times} 次',
            '转换后km': f'{converted_km:.2f} km'
        })
    
    # 添加跳绳记录
    for i, counts in enumerate(brush_records['rope_skipping']):
        converted_km = counts / 400
        all_records.append({
            '序号': len(all_records)+1,
            '运动类型': '跳绳',
            '数量': f'{counts} 个',
            '转换后km': f'{converted_km:.2f} km'
        })
    
    # 显示表格
    if all_records:
        df = pd.DataFrame(all_records)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("暂无历史记录")