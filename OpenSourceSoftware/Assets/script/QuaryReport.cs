using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class QuaryReport : MonoBehaviour
{

    public Text result;
    public InputField input;

    public void QueryBottun()
    {
        string para = "grades?find_course=" + input.text + "&id=" + Tool.id;
        result.text = Tool.getUrl(para);
        result.text = result.text.Replace("\" ", " ");
        result.text = result.text.Replace("\"", " ");
        result.text = result.text.Replace("\\n", "\n");
    }
}
