from langchain.tools import tool
from zai import ZhipuAiClient
import os
from dotenv import load_dotenv

load_dotenv()

@tool(parse_docstring=True)
def web_search(query:str) -> str:
    """互联网搜索工具，可以搜索互联网上的内容。

    Args:
        query (str): 搜索查询的信息

    Returns:
        str: 搜索结果
    """
    try:
        client = ZhipuAiClient(api_key=os.getenv("ZHIPUAI_API_KEY"))
        response = client.web_search.web_search(
            search_engine="search_std",
            search_query=query,
            count=15,  # 返回结果的条数，范围1-50，默认10
            # search_domain_filter="www.sohu.com",  # 只访问指定域名的内容
            search_recency_filter="noLimit",  # 搜索指定日期范围内的内容
            content_size="high"  # 控制网页摘要的字数，默认medium
        )
        if response.search_result:
            return "\n\n".join([d.content for d in response.search_result])
        else:
            return "没有搜索到相关内容"
    except Exception as e:
        print(f"搜索失败：{e}")
        return f"搜索失败：{e}"

if __name__ == "__main__":
    print(web_search.name)
    print(web_search.description)
    print(web_search.args)
    print(web_search.args_schema.model_json_schema())
    res = web_search.invoke({"query":"如何使用langchain"})
    print(res)
