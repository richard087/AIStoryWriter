import aistorywriter.writer.LLMEditor
import aistorywriter.writer.PrintUtils
import aistorywriter.writer.Config
import aistorywriter.writer.Chapter.ChapterGenSummaryCheck
import aistorywriter.writer.Prompts


def SceneOutlineToScene(Interface, _Logger, _ThisSceneOutline:str, _Outline:str, _BaseContext: str = ""):

    # Now we're finally going to go and write the scene provided.


    _Logger.Log(f"Starting SceneOutline->Scene", 2)
    MesssageHistory: list = []
    MesssageHistory.append(Interface.BuildSystemQuery(Writer.Prompts.DEFAULT_SYSTEM_PROMPT))
    MesssageHistory.append(Interface.BuildUserQuery(Writer.Prompts.SCENE_OUTLINE_TO_SCENE.format(_SceneOutline=_ThisSceneOutline, _Outline=_Outline)))

    Response = Interface.SafeGenerateText(_Logger, MesssageHistory, Writer.Config.CHAPTER_STAGE1_WRITER_MODEL, _MinWordCount=100)
    _Logger.Log(f"Finished SceneOutline->Scene", 5)

    return Interface.GetLastMessageText(Response)
