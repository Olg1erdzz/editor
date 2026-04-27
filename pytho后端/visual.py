import re


def mindmap(text):
    # 匹配第一个 { 到最后一个 } 之间的内容
    pattern = r'\{(.*)\}'
    match = re.search(pattern, text, re.DOTALL)

    if match:
        # 添加 { 和 } 到匹配的内容
        json_object = '{' + match.group(1) + '}'
        return json_object
    else:
        return "未找到 JSON 对象"


def text_process(text):
    # 匹配第一个 { 到最后一个 } 之间的内容
    pattern = r'\{(.*)\}'
    match = re.search(pattern, text, re.DOTALL)

    if match:
        # 添加 { 和 } 到匹配的内容
        json_object = '' + match.group(1) + ''
        return json_object
    else:
        return "未找到 JSON 对象"


def v_style(style):
    if style == "line":
        prompt = '''
你是一个提取关键数据信息并生成charts可视化代码的专家。对于我所给定你的每一段文本(包括表格)，你需要提取我所给的文本(表格)中的数据信息，生成相应的charts折线图可视化代码，代码部分用{}括起来。
代码格式样例如下：
{
   title: {
      text: '周销售额趋势'
   },
   xAxis: {
      name: '第一周',
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
   },
   yAxis: {
      name: '销售额',
      data: 'value'
   },
   series: [
     {
       data: [1200, 2230, 1900, 2100, 3500, 4200, 3985],
       type: 'line'
     }
   ]
}
切记只需要生成并返回代码部分。
'''
    elif style == "bar":
        prompt = '''
你是一个提取关键数据信息并生成charts可视化代码的专家。对于我所给定你的每一段文本(包括表格)，你需要提取我所给的文本(表格)中的数据信息，生成相应的charts柱状图可视化代码,代码部分用{}括起来。
代码格式样例如下：
{
  title: {
    text: '周销售额趋势'
  },
  xAxis: {
    name: '第一周',
    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  },
  yAxis: {
    name: '销售额',
    data: 'value'
  },
  series: [
    {
      data: [1200, 2230, 1900, 2100, 3500, 4200, 3985],
      type: 'bar'
    }
  ]
}
切记只需要生成并返回代码部分。
                    '''
    elif style == "pie":
        prompt = '''
你是一个提取关键数据信息并生成charts可视化代码的专家。对于我所给定你的每一段文本(包括表格)，你需要提取我所给的文本(表格)中的数据信息，生成相应的charts饼状图可视化代码,代码部分用{}括起来。
代码格式样例如下：
{
  title: {
    text: '畅销饮料占比饼状图'
  },
  series: [
    {
      type: 'pie',
      data: [
        { name: '可口可乐', value: 93 },
        { name: '百事可乐', value: 32 },
        { name: '哇哈哈', value: 6 },
        { name: '康师傅', value: 44 5},
        { name: '统一', value: 52 },
      ],
      insideLabel: {
        show: true
      }
    }
  ]
}
切记只需要生成并返回代码部分。
                '''
    return prompt