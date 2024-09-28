from website import my_website
from phygital_library_adapter import PhygitalLibraryAdapter
from ai_navigation_adapter import AiNavigationAdapter
from other_platform_adapter import OtherPlatformAdapter
from magicbox_tools_adapter import MagicBoxToolsAdapter
from ai_worthy_adapter import AIWorthyAdapter
from ai_lib_adapter import AILibToolsAdapter
from ai_mojo_adapter import AiMojoToolsAdapter
from chatgptdemo_adapter import ChatGPTDemoAdapter
from design_tools_adapter import DesignToolsAdapter
from nextool_adapter import NextoolAdapter
from woyai_adapter import WoyAIAdapter
from infrabase_adapter import InfrabaseAdapter
from tally_adapter import TallyAdapter  # 新增的适配器
from ababtool_adapter import AbabToolsAdapter  # 新增的适配器
from mergeek_adapter import MergeekAdapter  # 新增的适配器
from aiyoubucuo_adapter import AiyoubucuoAdapter  # 新增的适配器
from wechalet_adapter import WechaletAdapter  # 新增的适配器
from aitoolnet_adapter import AitoolnetAdapter  # 新增的适配器
from supertools_adapter import SupertoolsAdapter  # 新增的适配器
from humanornot_adapter import HumanOrNotAdapter  # 新增的适配器
from active_search_results_adapter import ActiveSearchResultsAdapter

def submit_to_all_platforms(website):
    adapters = [
        # PhygitalLibraryAdapter(website),
        # AiNavigationAdapter(website),
        # OtherPlatformAdapter(website)  # 不成功的
        # MagicBoxToolsAdapter(website),    # 需要验证是否成功
        # AIWorthyAdapter(website),
        # AILibToolsAdapter(website)    # 问题： 未选选择好复选框。 加一点手动操作
        # AiMojoToolsAdapter(website) #  不成功，后面再看
        # ChatGPTDemoAdapter(website),   # 已明确知道提交成功
        # DesignToolsAdapter(website),   # 已明确知道提交成功
        NextoolAdapter(website)  # 已明确知道提交成功，但未能成功监控提交成功。 提交到这里了
        # InfrabaseAdapter(website),  # 已明确知道提交成功，能成功监控提交成功
        # TallyAdapter(website),  # 新增的适配器，  未能成功，但是能正常上传logo 了
        # AbabToolsAdapter(website),  # 加载时间过长，无法成功
        # MergeekAdapter(website),  # 已明确知道提交成功，但未能成功监控提交成功
        # AiyoubucuoAdapter(website)  # 已明确知道提交成功，但未能成功监控提交成功
        # WechaletAdapter(website) , # 已明确知道提交成功但未能成功监控提交成功
        # AitoolnetAdapter(website),  # 已明确知道提交成功，但未能成功监控提交成功
        # SupertoolsAdapter(website),  # 定位不到具体的元素 ， 失败
        # HumanOrNotAdapter(website)  # 已明确知道提交成功，能成功监控提交成功
        # ActiveSearchResultsAdapter(website)  # 新增的适配器
    ]

    for adapter in adapters:
        print(f"正在使用 {adapter.__class__.__name__} 提交...")
        adapter.submit(headless=False)
        print("------------------------")

if __name__ == "__main__":
    submit_to_all_platforms(my_website)
