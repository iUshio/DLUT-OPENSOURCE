using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class QuaryExam : MonoBehaviour
{

    public Text result;

    public void QueryBottun()
    {
        string para = "exams?id=" + Tool.id;
        result.text = Tool.getUrl(para);
        result.text = result.text.Replace("\" ", " ");
        result.text = result.text.Replace("\"", " ");
        result.text = result.text.Replace("\\n", "\n");
    }
}
