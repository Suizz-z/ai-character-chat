import sys
import json
import os
import dashscope
from dashscope import MultiModalConversation
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from langchain.agents import AgentState, create_agent
from model import chat_Model

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

def create_image_prompt(personality_name: str,query: str) -> str:

    prommpt_agent_prompt = f"""
    你是一位文生图提示词领域的专业助手，根据用户的描述并根据以下规则生成详细的图像描述。
    <注意>
    1. 不要将主角正在说话的台词出现图片上
    </注意>
    <规则>
    - 提示词 = 主体（主体描述）+ 场景（场景描述）+ 风格（定义风格）+ 镜头语言 + 氛围词 + 细节修饰

    - 主体描述：确定主体清晰地描述图像中的主体，包括其特征、动作等。例如，“一个可爱的10岁中国小女孩，穿着红色衣服”。

    - 场景描述：场景描述是对主体所处环境特征细节的描述，可通过形容词或短句列举。

    - 定义风格：定义风格是明确地描述图像所应具有的特定艺术风格、表现手法或视觉特征。例如，“水彩风格”、“漫画风格”常见风格化详见下方提示词词典。

    - 镜头语言：镜头语言包含景别、视角等，常见镜头语言详见提示词词典。

    - 氛围词：氛围词是对预期画面氛围的描述，例如“梦幻”、“孤独”、“宏伟”，常见氛围词详见提示词词典。

    - 细节修饰：细节修饰是对画面进一步的精细化和优化，以增强图像的细节表现力、丰富度和美感。例如“光源的位置”、“道具搭配”、“环境细节”，“高分辨率”等。
    </规则>
    <提示词词典>
    1. 景别:景别是指由于相机与被拍摄体的距离不同，而造成被摄体在图像画面中所呈现出的范围大小的区别，一般可分为远景、全景、中景、近景、特写等。以下是部分景别示例：
        - 远景：远景镜头 | 展示了远景镜头，在壮丽的雪山背景下，两个小小的人影站在远处山顶，背对着镜头，静静地观赏着日落的美景。夕阳的余晖洒在雪山上，呈现出一片金黄色的光辉，与蔚蓝的天空形成鲜明对比。两人仿佛被这壮观的自然景象所吸引，整个画面充满了宁静与和谐。
        - 中景：中景镜头 | 电影时尚魅力摄影，年轻亚洲女子，中国苗族女孩，圆脸，看着镜头，民族深色优雅的服装，中广角镜头，阳光明媚，乌托邦式，由高清相机拍摄。
        - 近景：近景镜头 | 近景镜头，18岁的中国女孩，古代服饰，圆脸，看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。
        - 特写：特写镜头 | 高清相机，情绪大片，日落，特写人像。
    2. 视角：镜头视角，即相机拍摄画面时所选取的视角。以下是部分视角示例：
        - 平视：平视视角 | 图像展示了从平视视角捕捉到的草地景象，一群羊悠闲地在绿茵茵的草地上低头觅食，它们的羊毛在早晨微弱的阳光照耀下呈现出温暖的金色光泽，形成美丽的光影效果。
        - 俯视：俯视视角 | 我从空中俯瞰冰湖，中心有一艘小船，周围环绕着漩涡图案和充满活力的蓝色海水。螺旋深渊，该场景是从上方以自上而下的视角拍摄的，展示了复杂的细节，例如表面的波纹和积雪覆盖的地面下的层。眺望冰冷的广阔天地。营造出一种令人敬畏的宁静感。
        - 仰视：仰视视角 | 展示了热带地区的壮观景象，高大的椰子树如同参天巨人般耸立，枝叶茂盛，直指蓝天。镜头采用仰视视角，让观众仿佛置身树下，感受大自然的雄伟与生机。阳光透过树叶间隙洒落，形成斑驳光影，增添了几分神秘与浪漫。整个画面充满了热带风情，让人仿佛能闻到椰香，感受到微风拂面的惬意。
    3. 镜头拍摄类型：镜头拍摄类型是指相机镜头根据不同的焦距、功能、应用场景等所划分的不同种类。以下是部分镜头拍摄类型示例：
        - 微距：全帧镜头 | 微距镜头 | cherries, carbonated water, macro, professional color grading, clean sharp focus, commercial high quality, magazine winning photography, hyper realistic, uhd, 8K
        - 超广角：超广角镜头 | 超广角镜头，碧海蓝天下的海岛，阳光透过树叶缝隙，洒下斑驳光影。
        - 长焦：长焦镜头 | 展示了长焦镜头下，一只猎豹在郁郁葱葱的森林中站立，面对镜头，背景被巧妙地虚化，猎豹的面部成为画面的绝对焦点。阳光透过树叶的缝隙，洒在猎豹身上，形成斑驳的光影效果，增强了视觉冲击力。
        - 鱼眼: 鱼眼镜头 | 展示了在鱼眼镜头的特殊视角下，一位女性站立着并直视镜头的场景。她的形象在画面中心被夸张地放大，四周则呈现出强烈的扭曲效果，营造出一种独特的视觉冲击力。
    4. 风格：定义风格是明确地描述图像所应具有的特定艺术风格、表现手法或视觉特征。以下是部分风格类型示例：
        - 3D卡通：网球女运动员，短发，白色网球服，黑色短裤，侧身回球，3D卡通风格。
        - 废土风：火星上的城市，废土风格。
        - 点彩画：一座白色的可爱的小房子，茅草房，一片被雪覆盖的草原，大胆使用点彩色画，莫奈感，清晰的笔触，边缘模糊，原始的边缘纹理，低饱和度的颜色，低对比度，莫兰迪色。
        - 超现实：深灰色大海中一条粉红色的发光河流，具有极简、美丽和审美的氛围，具有超现实风格的电影灯光。
        - 水彩：浅水彩，咖啡馆外，明亮的白色背景，更少细节，梦幻，吉卜力工作室。
        - 粘土：粘土风格，蓝色毛衣的小男孩，棕色卷发，深蓝色贝雷帽，画板，户外，海边，半身照。
        - 水墨：兰花，水墨画，留白，意境，吴冠中风格，细腻的笔触，宣纸的纹理。
        - 写实：篮子，葡萄，野餐布，超写实静物摄影，微距镜头，丁达尔效应。
        - 折纸: 折纸杰作，牛皮纸材质的熊猫，森林背景，中景，极简主义，背光，最佳品质。
        - 工笔: 晨曦中，一枝寒梅傲立雪中，花瓣细腻如丝，露珠轻挂，展现工笔画之精致美
        - 国风水墨: 国风水墨风格，一个长长黑发的男人，金色的发簪，飞舞着金色的蝴蝶，白色的服装，高细节，高质量，深蓝色背景，背景中有若隐若现的水墨竹林。
    5. 光线：不同的光线类型可以创造出各种不同的氛围和效果，满足不同的创作需求。以下是部分光线类型示例：
        - 自然光
        - 氛围光
        - 逆光
        - 霓虹灯
    </提示词词典>
    """

    prommpt_agent = create_agent(
        model=chat_Model,
        system_prompt=prommpt_agent_prompt,
    )

    image_prompt = prommpt_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"主角是{personality_name},正在回话{query}"
                }
            ]
        }
    )
    print(image_prompt)
    return image_prompt

def create_image(personality_name: str,query: str):
    image_prompt_obj = create_image_prompt(personality_name,query)
    image_prompt_text = image_prompt_obj['messages'][-1].content
    
    messages = [
        {
            "role": "user",
            "content": [
                {"text": image_prompt_text}
            ]
        }
    ]
    response = MultiModalConversation.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen-image-max",
        messages=messages,
        result_format='message',
        stream=False,
        watermark=False,
        prompt_extend=True,
        negative_prompt="低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。",
        size='1328*1328'
    )
    if response.status_code == 200:

        print(json.dumps(response, ensure_ascii=False))
        return response.output.choices[0].message.content[0]['image']
    else:
        print(f"HTTP返回码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        return f"HTTP返回码：{response.status_code}，错误码：{response.code}，错误信息：{response.message}"

if __name__ == "__main__":
    image = create_image("甄嬛","你这般突然出声，倒让本宫有些意外。想来你是有事相询？但说无妨。")
    print(f"图片:{image}")
