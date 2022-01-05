using System;
using System.IO;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Tool : MonoBehaviour
{
    public static String id;

    /// <summary>
    /// RSA的加密函数
    /// </summary>
    /// <param name="encryptString">待加密的字符串</param>
    /// <returns>加密的字符串</returns>
    public static string RSAEncrypt(string encryptString)
    {
        try
        {
            
            RSACryptoServiceProvider rsa = new RSACryptoServiceProvider();
            String xmlPublicKey = "<RSAKeyValue><Modulus>g5EnEGf+aJDGrukoA6uk/agE+28rG8yVWEngE90Vdcg62qaIjflxjbAHmN/BbnaftU2PTBUfWRl1VpbBRj9e4vNxcS1fT6En3YNe0jhD6/LzJnXNjXpTtkATOt2HOS91kXX4MIoV3Ei7lMGFzifgAZ4avzAHi5JPjO05XNMJwVs=</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>";
            //String xmlPublicKey = rsa.ToXmlString(false); //存放公钥
            //String xmlPrivateKey = rsa.ToXmlString(true);
            //Debug.Log("public:" + xmlPublicKey);
            //Debug.Log("private:" + xmlPrivateKey);
            // Debug.Log(xmlPublicKey);
            byte[] PlainTextBArray;
            byte[] CypherTextBArray;
            string Result;
            rsa.FromXmlString(xmlPublicKey);
            PlainTextBArray = (new UnicodeEncoding()).GetBytes(encryptString);
            CypherTextBArray = rsa.Encrypt(PlainTextBArray, false);
            Result = Convert.ToBase64String(CypherTextBArray);
            return Result;
        }
        catch (Exception ex)
        {
            Debug.Log(ex);
            throw ex;
        }
    }

    /// <summary>
    /// RSA的加密函数
    /// </summary>
    /// <param name="para">请求参数</param>
    /// <returns>响应</returns>
    public static String getUrl(String para)
    {
        try
        {
            StringBuilder content = new StringBuilder();
            //url拼接数据
            string address = "http://116.62.15.29:8000/api/" + para;
            Debug.Log(address);
            //创建request
            HttpWebRequest req = (HttpWebRequest)HttpWebRequest.Create(address);
            //确定传值方式，此处为get方式
            req.Method = "GET";
            //获取响应
            HttpWebResponse resp = (HttpWebResponse)req.GetResponse();
            // 获取响应流
            Stream responseStream = resp.GetResponseStream();
            // 对接响应流(以"GBK"字符集)
            StreamReader sReader = new StreamReader(responseStream, Encoding.GetEncoding("utf-8"));
            // 开始读取数据
            Char[] sReaderBuffer = new Char[256];
            int count = sReader.Read(sReaderBuffer, 0, 256);
            while (count > 0)
            {
                String tempStr = new String(sReaderBuffer, 0, count);
                content.Append(tempStr);
                count = sReader.Read(sReaderBuffer, 0, 256);
            }
            // 读取结束
            sReader.Close();
            //返回响应
            return content.ToString();
        }
        catch
        {
            return "";
        }
    }

    public void returnToMain()
    {
        SceneManager.LoadScene("2_QuaryScene");
    }
}
