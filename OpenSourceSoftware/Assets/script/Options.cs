using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class Options : MonoBehaviour
{
    public InputField mail;
    public void Go_3Scene()
    {
        SceneManager.LoadScene("3_QuaryReport");
    }

    public void Go_4Scene()
    {
        SceneManager.LoadScene("4_QuaryExam");
    }

    public void SetEmail()
    {
        string para = "setmail?id=" + Tool.id + "&mail=" + mail.text;
        string state = Tool.getUrl(para);
        Debug.LogError("state:" + state);
    }
}
