#!/usr/bin/env python3
"""
Teambition页面数据分析脚本
用于解析和分析从浏览器快照快照中提取的Teambition项目数据
"""

import re
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
from collections import defaultdict

class TeambitionAnalyzer:
    def __init__(self):
        self.tasks = []
        self.categories = {}
        self.views = {}
        self.team_members = defaultdict(int)
        
    def parse_snapshot(self, snapshot_text: str) -> Dict[str, Any]:
        """
        解析浏览器快照文本，提取Teambition项目信息
        
        Args:
            snapshot_text: 浏览器快照的文本内容
            
        Returns:
            包含解析结果的字典
        """
        result = {
            'project_name': '',
            'current_viewView': '',
            'total_tasks': 0,
            'completed_tasks': 0,
            'categories': {},
            'kanban_columns': {},
            'tasks': [],
            'team_members': {},
            'deadlines': {
                'today': [],
                'week': [],
                'month': []
            }
        }
        
        # 提取项目名称
        project_match = re.search(r'项目名称[:：]\s*(.+)', snapshot_text)
        if project_match:
            result['project_name'] = project_match.group(1).strip()
        
        # 提取当前视图
        view_match = re.search(r'当前视图[:：]\s*(.+)', snapshot_text)
        if (view_match):
            result['current_view'] = view_match.group(1).strip()
        
        # 提取任务总数
        total_match = re.search(r'(\d+)/(\d+)', snapshot_text)
        if total_match:
            result['completed_tasks'] = int(total_match.group(1))
            result['total_tasks'] = int(total_match.group(2))
        
        # 提取需求分类
        category_pattern = r'[-*]\s*(.+?)[:：]\s*(\d+)'
        for match in re.finditer(category_pattern, snapshot_text):
            category = match.group(1).strip()
            count = int(match.group(2))
            result['categories'][category] = count
        
        # 提取看板列信息
        column_pattern = r'####\s*(.+?)\s*\((\d+)个任务\)'
        for match in re.finditer(column_pattern, snapshot_text):
            column = match.group(1).strip()
            count = int(match.group(2))
            result['kanban_columns'][column] = count
        
        # 提取任务信息
        task_pattern = r'-\s*\*\*(.+?)\*\*\s*\((.+?)\)'
        for match in re.finditer(task_pattern, snapshot_text):
            task_name = match.group(1).strip()
            task_details = match.group(2).strip()
            result['tasks'].append({
                'name': task_name,
                'details': task_details
            })
        
        # 提取团队成员
        member_pattern = r'创建者[:：]\s*(\w+)'
        for match in re.finditer(member_pattern, snapshot_text):
            member = match.group(1).strip()
            result['team_members'][member] = result['team_members'].get(member, 0) + 1
        
        # 分析截止日期
        today = datetime.now()
        week_later = today + timedelta(days=7)
        month_later = today + timedelta(days=30)
        
        deadline_pattern = r'(\d{4}-\d{2}-\d{2}|今天|明天|后天|本周|下周)'
        for match in re.finditer(deadline_pattern, snapshot_text):
            deadline_str = match.group(1)
            
            if deadline_str == '今天':
                result['deadlines']['today'].append(deadline_str)
            elif deadline_str in ['明天', '后天', '本周']:
                result['deadlines']['week'].append(deadline_str)
            elif deadline_str in ['下周']:
                result['deadlines']['week'].append(deadline_str)
            else:
                # 尝试解析具体日期
                try:
                    deadline_date = datetime.strptime(deadline_str, '%Y-%m-%d')
                    if deadline_date <= today:
                        result['deadlines']['today'].append(deadline_str)
                    elif deadline_date <= week_later:
                        result['deadlines']['week'].append(deadline_str)
                    elif deadline_date <= month_later:
                        result['deadlines']['month'].append(deadline_str)
                except ValueError:
                    pass
        
        return result
    
    def generate_report(self, analysis_result: Dict[str, Any], detailed: bool = False) -> str:
        """
        生成项目状态报告
        
        Args:
            analysis_result: 解析结果
            detailed: 是否生成详细报告
            
        Returns:
            格式化的报告字符串
        """
        report = []
        
        # 项目概览
        report.append("## 📊 Teambition项目状态概览\n")
        report.append("### 项目基本信息")
        report.append(f"- **项目名称**: {analysis_result['project_name']}")
        report.append(f"- **当前视图**: {analysis_result['current_view']}")
        
        if analysis_result['total_tasks'] > 0:
            completion_rate = (analysis_result['completed_tasks'] / analysis_result['total_tasks']) * 100
            report.append(f"- **需求总数**: {analysis_result['completed_tasks']}/{analysis_result['total_tasks']}")
            report.append(f"- **完成率**: {completion_rate:.1f}%")
        
        report.append("")
        
        # 需求分类统计
        if analysis_result['categories']:
            report.append("### 需求分类统计")
            for category, count in analysis_result['categories'].items():
                report.append(f"- **{category}**: {count}")
            report.append("")
        
        # 看板视图状态
        if analysis_result['kanban_columns']:
            report.append("### 看板视图状态")
            for column, count in analysis_result['kanban_columns'].items():
                report.append(f"- **{column}**: {count}个任务")
            report.append("")
        
        # 关键时间节点
        if any(analysis_result['deadlines'].values()):
            report.append("### 关键时间节点")
            
            if analysis_result['deadlines']['today']:
                report.append(f"- **今天截止**: {len(analysis_result['deadlines']['today'])}个任务")
                if detailed:
                    for deadline in analysis_result['deadlines']['today'][:5]:  # 只显示前5个
                        report.append(f"  - {deadline}")
            
            if analysis_result['deadlines']['week']:
                report.append(f"- **本周内截止**: {len(analysis_result['deadlines']['week'])}个任务")
            
            if analysis_result['deadlines']['month']:
                report.append(f"- **本月内截止**: {len(analysis_result['deadlines']['month'])}个任务")
            
            report.append("")
        
        # 团队参与情况
        if (analysis_result['team_members']):
            report.append("### 团队参与情况")
            sorted_members = sorted(analysis_result['team_members'].items(), 
                                   key=lambda x: x[1], reverse=True)
            for member, count in sorted_members[:10]:  # 显示前10名
                report.append(f"- **{member}**: {count}个任务")
            report.append("")
        
        # 项目健康度评估
        report.append("### 项目健康度评估")
        
        # 计算健康度指标
        if analysis_result['total_tasks'] > 0:
            completion_rate = (analysis_result['completed_tasks'] / analysis_result['total_tasks']) * 100
            
            if completion_rate >= 80:
                health_status = "🟢 优秀"
            elif completion_rate >= 60:
                health_status = "🟡 良好"
            elif completion_rate >= 40:
                health_status = "🟠 一般"
            else:
                health_status = "🔴 需要关注"
            
            report.append(f"- **整体进度**: {health_status} ({completion_rate:.1f}%)")
        
        # 逾期风险
        today_deadlines = len(analysis_result['deadlines']['today'])
        if today_deadlines > 10:
            report.append(f"- **逾期风险**: 🔴 高 ({today_deadlines}个任务今天截止)")
        elif today_deadlines > 5:
            report.append(f"- **逾期风险**: 🟡 中 ({today_deadlines}个任务今天截止)")
        else:
            report.append(f"- **逾期风险**: 🟢 低 ({today_deadlines}个任务今天截止)")
        
        # 团队负载
        if analysis_result['team_members']:
            avg_tasks = sum(analysis_result['team_members'].values()) / len(analysis_result['team_members'])
            max_tasks = max(analysis_result['team_members'].values())
            
            if max_tasks > avg_tasks * 2:
                report.append(f"- **团队负载**: ⚠️ 不均衡 (最高{max_tasks}个任务，平均{avg_tasks:.1f}个)")
            else:
                report.append(f"- **团队负载**: ✅ 均衡 (平均{avg_tasks:.1f}个任务/人)")
        
        return "\n".join(report)
    
    def export_to_json(self, analysis_result: Dict[str, Any], filename: str = "teambition_analysis.json"):
        """
        将分析结果导出为JSON文件
        
        Args:
            analysis_result: 解析结果
            filename: 输出文件名
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        print(f"分析结果已导出到 {filename}")
    
    def get_risk_tasks(self, analysis_result: Dict[str, Any]) -> List[str]:
        """
        获取高风险任务列表
        
        Args:
            analysis_result: 解析结果
            
        Returns:
            高风险任务描述列表
        """
        risks = []
        
        # 今天截止的任务
        if len(analysis_result['deadlines']['today']) > 5:
            risks.append(f"⚠️ 今天有{len(analysis_result['deadlines']['today'])}个任务截止，需要重点关注")
        
        # 完成率过低
        if analysis_result['total_tasks'] > 0:
            completion_rate = (analysis_result['completed_tasks'] / analysis_result['total_tasks']) * 100
            if completion_rate < 40:
                risks.append(f"⚠️ 项目完成率仅为{completion_rate:.1f}%，进度偏慢")
        
        # 团队负载不均衡
        if analysis_result['team_members']:
            tasks = list(analysis_result['team_members'].values())
            if len(tasks) > 1:
                avg_tasks = sum(tasks) / len(tasks)
                max_tasks = max(tasks)
                if max_tasks > avg_tasks * 2:
                    risks.append("⚠️ 团队工作负载分配不均衡，建议重新分配")
        
        return risks


def main():
    """主函数，用于测试"""
    analyzer = TeambitionAnalyzer()
    
    # 示例数据
    sample_snapshot = """
    项目名称: 示例项目【20XX年/20XX年】
    当前视图: 示例版本需求-看板视图
    需求总数: 20/33
    
    需求分类统计:
    - 所有需求: 20/33
    - 未分类需求: 16
    - 示例版本需求池: 8
    
    看板视图状态:
    #### 待处理 (170个任务)
    - **示例任务A** (示例子项1)
    - **示例任务B** (示例子项2)
    
    #### 开发中 (45个任务)
    - **示例任务C** (示例子项3)
    
    创建者: 用户甲
    创建者: 用户乙
    创建者: 用户丙
    """
    
    # 解析数据
    result = analyzer.parse_snapshot(sample_snapshot)
    
    # 生成报告
    report = analyzer.generate_report(result, detailed=True)
    print(report)
    
    # 导出JSON
    analyzer.export_to_json(result)
    
    # 获取风险
    risks = analyzer.get_risk_tasks(result)
    if risks:
        print("\n### ⚠️ 风险提示")
        for risk in risks:
            print(risk)


if __name__ == "__main__":
    main()
