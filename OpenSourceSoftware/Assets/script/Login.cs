using System;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class Login : MonoBehaviour
{
    //登录输入
    public InputField id;
    public InputField passward;

    public void trylogin()
    {
        Tool.id = id.text;
        //加密
        String encodingPassword = Tool.RSAEncrypt(passward.text);
        Debug.Log(encodingPassword);
        encodingPassword = encodingPassword.Replace("+", "%2B");
        encodingPassword = encodingPassword.Replace("/", "%2F");
        encodingPassword = encodingPassword.Replace("=", "%3D");
        
        //拼接请求参数
        string para ="login?id=" + id.text + "&" + "password=" + encodingPassword;

        //获取响应id
        string temp = Tool.getUrl(para);
        Debug.Log("state:"+ temp);

        if ("\"success\"".Equals(temp))
        {
            //登录成功
            SceneManager.LoadScene("2_QuaryScene");
        }
        else
        {
            //登录失败
            // SceneManager.LoadScene("2_QuaryScene");
        }
    } 
}
